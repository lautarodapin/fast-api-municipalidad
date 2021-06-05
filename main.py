from typing import List
from fastapi import FastAPI, Query, Path, Depends
from schemas import Carta, Consejal, OrdenDia, Ordenanza
from datetime import datetime
import scrap
from httpx import AsyncClient

app = FastAPI()

def get_client():
    client = AsyncClient(timeout=60)
    try:
        yield client
    finally:
        del client


@app.get("/ordenanzas/all", response_model=List[Ordenanza])
async def get_all_ordenanzas(
    client: AsyncClient = Depends(get_client),
    q: str = Query(None, description="Query string search"),
):
    ordenanzas = await scrap.get_all_ordenanzas(client)
    results: List[Ordenanza] = []
    if q:
        filtro = filter(
            lambda ordenanza: any([
                any([word.lower().strip() in prop.lower().strip() for prop in [ordenanza.titulo, ordenanza.extracto, ordenanza.numero, str(ordenanza.año)]])
                for word in q.split(" ")
            ]), 
            ordenanzas,
        )
        results += list(filtro)
    else: results = ordenanzas
    return results
    

@app.get("/ordenanzas", response_model=List[Ordenanza])
async def get_ordenanzas(
    year: int = Query(datetime.now().year, gt=1999),
    client: AsyncClient = Depends(get_client),
    ):
    return await scrap.get_ordenanzas_por_año(client, year)

@app.get("/ordenanzas/desde", response_model=List[Ordenanza])
async def get_ordenanzas_desde(
    desde: int = Query(datetime.now().year - 1, gt=1999, description="Año desde el cual buscar"),
    client: AsyncClient = Depends(get_client),
):
    return await scrap.get_ordenanzas_desde(client, desde)

@app.get("/ordenanza/{id}", response_model=Ordenanza)
async def get_ordenanza_por_id(id: int = Path(..., description="Numero de ordenanza"), client: AsyncClient = Depends(get_client)):
    return await scrap.get_ordenanza_por_numero(client, id)


@app.get("/hcd/presidente", response_model=Carta)
async def get_presidente_hcd(client: AsyncClient = Depends(get_client),):
    return await scrap.get_presidente_honorable_consejo_deliberante(client)


@app.get("/hcd/consejales", response_model=List[Consejal])
async def get_consejales(
    nombre: str = Query(None),
    bloque: str = Query(None),
    client: AsyncClient = Depends(get_client),
):
    consejales = await scrap.get_consejales(client)
    results : List[Consejal] = []
    if not bloque and not nombre: results = consejales
    if nombre:
        results += list(filter(lambda consejal: nombre.strip().lower() in consejal.nombre.strip().lower(), consejales))
    if bloque:
        results += list(filter(lambda consejal: bloque.strip().lower() in consejal.bloque.strip().lower(), consejales))

    return results


@app.get("/hcd/ordenes-del-dia", response_model=List[OrdenDia])
async def get_ordenes_del_dia(client: AsyncClient = Depends(get_client),):
    return await scrap.get_ordenes_dia(client)

@app.get("/hcd/ordenes-del-dia/{id}", response_model=OrdenDia)
async def get_orden_del_dia(id: int, client: AsyncClient = Depends(get_client),):
    return await scrap.get_orden_dia(client, id)