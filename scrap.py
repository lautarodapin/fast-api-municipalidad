from bs4.element import ResultSet
import requests
import httpx
from typing import List, Optional
from bs4 import BeautifulSoup
from schemas import Ordenanza, Carta
from datetime import datetime
# In [5]: response = requests.post("http://www.portalwebvillamercedes.gob.ar/ord/index.php", data=dict(textobuscar=
#    ...: 2021))
DEFAULT_TIMEOUT = 60
base_url = "http://www.portalwebvillamercedes.gob.ar/ord"
url = f"{base_url}/index.php"
AÑO = 2021

html_text = requests.post(url, data=dict(textobuscar=AÑO)).text
soup = BeautifulSoup(html_text, "html.parser")

async def get_all_ordenanzas() -> Optional[List[Ordenanza]]:
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
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
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
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
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
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
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
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


async def get_presidente_honorable_consejo_deliberante() -> Optional[Carta]:
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        base_url = "http://www.hcdvillamercedes.gob.ar"
        response = await client.get(f"{base_url}/index.php/autoridades/presidencia")
        soup = BeautifulSoup(response.read(), 'html.parser')
        article: ResultSet = soup.find_all(attrs={"class":"article-intro clearfix", "itemprop":"articleBody"})
        imagen = base_url + article[0].find("h1").find("img").get("src")
        cargo = article[0].find("h2").text
        cargo_hcd, _, periodo= list(map(str.strip, list(map(lambda x: x.text, article[0].find_all("p")[:3]))))
        biografia = " ".join(list(filter(None, map(lambda x: x.strip(), article[0].find("div", attrs={"class":"gs"}).text.split('\n')))))
        return Carta(imagen=imagen, cargo=cargo, cargo_hcd=cargo_hcd, biografia=biografia, periodo=periodo)