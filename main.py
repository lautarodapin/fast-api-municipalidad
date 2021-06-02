from typing import List
from fastapi import FastAPI, Query, Path
from schemas import Ordenanza
from datetime import datetime
import scrap
app = FastAPI()

@app.get("/ordenanzas/all", response_model=List[Ordenanza])
async def get_all_ordenanzas():
    return await scrap.get_all_ordenanzas()

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