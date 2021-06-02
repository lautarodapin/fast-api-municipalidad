import requests
import httpx
from typing import List, Optional
from bs4 import BeautifulSoup
from schemas import Ordenanza
from datetime import datetime
# In [5]: response = requests.post("http://www.portalwebvillamercedes.gob.ar/ord/index.php", data=dict(textobuscar=
#    ...: 2021))

base_url = "http://www.portalwebvillamercedes.gob.ar/ord"
url = f"{base_url}/index.php"
AÑO = 2021

html_text = requests.post(url, data=dict(textobuscar=AÑO)).text
soup = BeautifulSoup(html_text, "html.parser")

async def get_all_ordenanzas() -> Optional[List[Ordenanza]]:
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=dict(textobuscar=" "))
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
                    archivo=f'{base_url}{cells[4].find("a").get("href")[1:]}')
            )
        return ordenanzas


async def get_ordenanzas_por_año(year: int) -> Optional[List[Ordenanza]]:
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=dict(textobuscar=year))
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
                    archivo=f'{base_url}{cells[4].find("a").get("href")[1:]}')
            )
        return ordenanzas


async def get_ordenanzas_desde(year_from: int) -> Optional[List[Ordenanza]]:
    ordenanzas : List[Ordenanza] = []
    async with httpx.AsyncClient() as client:
        for year in range(year_from, datetime.now().year):
            response = await client.post(url, data=dict(textobuscar=year))
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

async def get_ordenanza_por_numero(numero: int) -> Optional[Ordenanza]:
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=dict(textobuscar=numero))
        html_text = response.read()
        soup = BeautifulSoup(html_text, "html.parser")
        ordenanza: Ordenanza
        for row in soup.find_all("tr"):
            cells = row.find_all("td")
            if not cells: continue
            return Ordenanza(
                    año=cells[0].text, 
                    numero=cells[1].text, 
                    titulo=cells[2].text, 
                    extracto=cells[3].text, 
                    archivo=f'{base_url}{cells[4].find("a").get("href")[1:]}'
                )