from typing import List
from fastapi import FastAPI, Query, Path, Depends
from schemas import Carta, Consejal, OrdenDia, Ordenanza
from datetime import datetime
import scrap
import httpx

app = FastAPI()

def get_client():
    with httpx.AsyncClient(timeout=60) as client:
        yield client



@app.get("/ordenanzas/all", response_model=List[Ordenanza])
async def get_all_ordenanzas(client: httpx.AsyncClient = Depends(get_client)):
    return await scrap.get_all_ordenanzas(client)

@app.get("/", response_model=List[Ordenanza])
async def get_ordenanzas(
    year: int = Query(datetime.now().year, gt=1999),
    ):
    return await scrap.get_ordenanzas_por_año(year)

@app.get("/ordenanzas", response_model=List[Ordenanza])
async def get_ordenanzas_desde(
    desde: int = Query(datetime.now().year - 1, gt=1999, description="Año desde el cual buscar"),
):
    return await scrap.get_ordenanzas_desde(desde)

@app.get("/ordenanza/{id}", response_model=Ordenanza)
async def get_ordenanza(id: int = Path(..., description="Numero de ordenanza")):
    return await scrap.get_ordenanza_por_numero(id)


@app.get("/hcd/presidente", response_model=Carta)
async def get_presidente_hcd():
    return await scrap.get_presidente_honorable_consejo_deliberante()


@app.get("/hcd/consejales", response_model=List[Consejal])
async def get_consejales(
    nombre: str = Query(None),
    bloque: str = Query(None),
):
    consejales = await scrap.get_consejales()
    results : List[Consejal] = []
    if not bloque and not nombre: results = consejales
    if nombre:
        results += list(filter(lambda consejal: nombre.strip().lower() in consejal.nombre.strip().lower(), consejales))
    if bloque:
        results += list(filter(lambda consejal: bloque.strip().lower() in consejal.bloque.strip().lower(), consejales))

    return results


@app.get("/hcd/ordenes-del-dia", response_model=List[OrdenDia])
async def get_ordenes_del_dia():
    return await scrap.get_ordenes_dia()

@app.get("/hcd/ordenes-del-dia/{id}", response_model=OrdenDia)
async def get_orden_del_dia(id: int):
    return await scrap.get_orden_dia(id)