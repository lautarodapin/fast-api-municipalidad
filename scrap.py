from bs4.element import ResultSet
# import requests
# import httpx
from httpx import AsyncClient
from typing import List, Optional
from bs4 import BeautifulSoup
from schemas import Consejal, OrdenDia, Ordenanza, Carta
from datetime import datetime
import re

# In [5]: response = requests.post("http://www.portalwebvillamercedes.gob.ar/ord/index.php", data=dict(textobuscar=
#    ...: 2021))
DEFAULT_TIMEOUT = 60

MESES = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}

async def get_all_ordenanzas(client: AsyncClient) -> List[Ordenanza]:
    base_url = "http://www.portalwebvillamercedes.gob.ar/ord"
    response = await client.post(f"{base_url}/index.php", data=dict(textobuscar=" "))
    html_text = response.read()
    soup = BeautifulSoup(html_text, "html.parser")
    ordenanzas : List[Ordenanza] = []
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if not cells: continue
        ordenanzas.append(
            Ordenanza(
                año=cells[0].text, 
                numero=cells[1].text, 
                titulo=cells[2].text, 
                extracto=cells[3].text, 
                archivo=f'{base_url}{cells[4].find("a").get("href")[1:]}',
            )
        )
    return ordenanzas


async def get_ordenanzas_por_año(client: AsyncClient, year: int) -> List[Ordenanza]:
    base_url = "http://www.portalwebvillamercedes.gob.ar/ord"
    response = await client.post(f"{base_url}/index.php", data=dict(textobuscar=year))
    html_text = response.read()
    soup = BeautifulSoup(html_text, "html.parser")
    ordenanzas : List[Ordenanza] = []
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if not cells: continue
        ordenanzas.append(
            Ordenanza(
                año=cells[0].text, 
                numero=cells[1].text, 
                titulo=cells[2].text, 
                extracto=cells[3].text, 
                archivo=f'{base_url}{cells[4].find("a").get("href")[1:]}',
            )
        )
    return ordenanzas


async def get_ordenanzas_desde(client: AsyncClient, year_from: int) -> List[Ordenanza]:
    base_url = "http://www.portalwebvillamercedes.gob.ar/ord"
    ordenanzas : List[Ordenanza] = []
    for year in range(year_from, datetime.now().year):
        response = await client.post(f"{base_url}/index.php", data=dict(textobuscar=year))
        html_text = response.read()
        soup = BeautifulSoup(html_text, "html.parser")
        for row in soup.find_all("tr"):
            cells = row.find_all("td")
            if not cells: continue
            ordenanza = Ordenanza(
                año=cells[0].text, 
                numero=cells[1].text, 
                titulo=cells[2].text, 
                extracto=cells[3].text, 
                archivo=f'{base_url}{cells[4].find("a").get("href")[1:]}'
            )
            if ordenanza in ordenanzas: continue
            ordenanzas.append(ordenanza)
    return ordenanzas

async def get_ordenanza_por_numero(client: AsyncClient, numero: int) -> Ordenanza:
    base_url = "http://www.portalwebvillamercedes.gob.ar/ord"
    response = await client.post(f"{base_url}/index.php", data=dict(textobuscar=numero))
    html_text = response.read()
    soup = BeautifulSoup(html_text, "html.parser")
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if not cells: continue
        break
    return Ordenanza(
        año=cells[0].text, 
        numero=cells[1].text, 
        titulo=cells[2].text, 
        extracto=cells[3].text, 
        archivo=f'{base_url}{cells[4].find("a").get("href")[1:]}'
    )


async def get_presidente_honorable_consejo_deliberante(client: AsyncClient) -> Carta:
    base_url = "http://www.hcdvillamercedes.gob.ar"
    response = await client.get(f"{base_url}/index.php/autoridades/presidencia")
    soup = BeautifulSoup(response.read(), 'html.parser')
    article: ResultSet = soup.find_all(attrs={"class":"article-intro clearfix", "itemprop":"articleBody"})
    imagen = base_url + article[0].find("h1").find("img").get("src")
    cargo = article[0].find("h2").text
    cargo_hcd, _, periodo= list(map(str.strip, list(map(lambda x: x.text, article[0].find_all("p")[:3]))))
    biografia = " ".join(list(filter(None, map(lambda x: x.strip(), article[0].find("div", attrs={"class":"gs"}).text.split('\n')))))
    return Carta(imagen=imagen, cargo=cargo, cargo_hcd=cargo_hcd, biografia=biografia, periodo=periodo)


async def get_consejales(client: AsyncClient) -> List[Consejal]:
    consejales: List[Consejal] = []
    base_url = "http://www.hcdvillamercedes.gob.ar"
    response = await client.get(f"{base_url}/index.php/concejales")
    soup = BeautifulSoup(response.read(), 'html.parser')
    cards: ResultSet = soup.find_all('div', attrs={"class":"contentpaneopen clearfix"})
    for card in cards:
        title = card.find("h2", attrs={"class":"article-title"})
        a_tag = title.find('a')
        if a_tag:
            url = a_tag.get("href")
        nombre = title.text.strip()
        if not nombre: continue
        section = card.find("section", attrs={"class":"article-intro clearfix"})
        if not section: continue
        parrafos = section.find_all("p")
        if not parrafos or len(parrafos) < 2: continue
        bloque, periodo = list(map(lambda x: x.text.strip(), parrafos))[:2]
        consejales.append(Consejal(
            nombre=nombre.strip().lower(),
            bloque=bloque.strip().lower(),
            periodo=periodo.strip().lower(),
            url=f"{base_url}{url}",
        ))
    return consejales


async def get_ordenes_dia(client: AsyncClient, limit: int = 10, start: int = 1) -> List[OrdenDia]:
    ordenes : List[OrdenDia] = []
    base_url = "http://www.hcdvillamercedes.gob.ar"
    for offset in range(start, limit + 1):
        response = await client.get(f"{base_url}/index.php/orden-del-dia?limit=1&start={offset}")
        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find("article")
        if not article: continue
        header = article.find("header")
        if not header: continue
        dia, mes = re.compile(r'\w+ \w+ \w+ \w+ (\d{1,2}) \w+ (\w+)').search(header.text).groups()
        if not dia and not mes: continue
        a_tag = header.find("a")
        if not a_tag: continue
        url = a_tag.get("href")
        id = re.compile(r'/index\.php/orden-del-dia/(\d{1,4})').search(url).groups()
        section = article.find("section")
        if not section: continue
        parrafos = section.find_all("p")
        if not parrafos and len(parrafos) < 4: continue
        img_tag = parrafos[0].find('img')
        if not img_tag: continue
        img = img_tag.get("src")
        codigo = parrafos[1].text.strip().lower()
        texto = "\n".join(list(map(lambda x: x.text.strip(), parrafos[2:]))).strip()
        if not img and not codigo and not texto: continue
        ordenes.append(
            OrdenDia(
                id=int(id[0]),
                codigo=codigo,
                texto=texto,
                dia=int(dia),
                mes=int(MESES[mes.strip().lower()]),
                url=f"{base_url}{url}",
                img=f"{base_url}{img}",
            )
        )
    return ordenes

async def get_orden_dia(client: AsyncClient, id: int) -> Optional[OrdenDia]:
    ordenes = await get_ordenes_dia(client)
    orden = list(filter(lambda orden: orden.id == id, ordenes))
    return orden[0] if orden else None
