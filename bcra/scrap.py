from typing import List
from httpx import AsyncClient
from bs4 import BeautifulSoup
import pandas as pd
from .schemas import VariableEconomica
from datetime import datetime, date
import re

async def get_principales_variables(client: AsyncClient) -> List[VariableEconomica]:
    base_url = "http://www.bcra.gov.ar"
    url = f"{base_url}/PublicacionesEstadisticas/Principales_variables.asp"
    response = await client.get(url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    table = soup.find("table", attrs={"class": "table"})
    columnas = ["titulo", "fecha", "valor", "link", "serie"]
    rows = table.find_all("tr")
    table = []
    for row in rows:
        if row.text:
            cells = row.find_all("td")
            if len(cells) < 3: continue
            if not all(list(map(lambda x: x.text, cells))): continue
            titulo = cells[0].text.strip()
            fecha = datetime.strptime(cells[1].text, "%d/%m/%Y") 
            valor = float(cells[2].text.replace('.', '').replace(',', '.'))
            link = base_url+ cells[0].find('a').get('href').strip().replace('\xa0', ' ')
            serie = re.compile(r'serie=(\d{1,6})').search(link).group(1) if re.compile(r'serie=(\d{1,6})').search(link) else None
            table.append([titulo, fecha, valor, link, serie])
    df = pd.DataFrame(table, columns=columnas)
    return list(map(lambda row: VariableEconomica(**dict(row[1])), df.iterrows()))



async def get_variable_by_serie_from_to(
    client: AsyncClient,
    serie: str,
    fecha_desde: date,
    fecha_hasta: date,
    ):
    base_url = "http://www.bcra.gov.ar"
    url = f"{base_url}/PublicacionesEstadisticas/Principales_variables_datos.asp"
    response = await client.post(url, data={
        "fecha_desde": fecha_desde.strftime("%Y-%m-%d"),
        "fecha_hasta": fecha_hasta.strftime("%Y-%m-%d"),
        "primeravez": "1",
        "serie": serie,
    })
    soup = BeautifulSoup(response.read(), "html.parser")
    table = soup.find_all("tbody")
    return [
        VariableEconomica(fecha=tds[0].text, valor=tds[1].text) 
        for row in table if (tds:=row.find_all('td'))
    ]