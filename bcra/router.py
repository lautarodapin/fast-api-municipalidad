from typing import List
from fastapi.param_functions import Depends, Query
from bcra.schemas import VariableEconomica
from fastapi import APIRouter
from utils import get_client, AsyncClient
from datetime import datetime, date, timedelta
from . import scrap
router = APIRouter(prefix="/bcra")

@router.get("/variables-economicas", response_model=List[VariableEconomica])
async def get_variables_economicas(
    q: str = Query(None, description="Busqueda"),
    client: AsyncClient = Depends(get_client),
):
    variables = await scrap.get_principales_variables(client)
    if not q: return variables
    return list(filter(lambda var: any([word.lower() in var.titulo for word in q.split(' ')]), variables))


@router.get("/variables-economicas/{serie}", response_model=List[VariableEconomica])
async def get_variable_serie_desde_hasta(
    serie: str = "246",
    fecha_desde: date = Query((datetime.now() - timedelta(days=30)).date()),
    fecha_hasta: date = Query(datetime.now().date()),
    client: AsyncClient = Depends(get_client),
):
    return await scrap.get_variable_by_serie_from_to(client, serie, fecha_desde, fecha_hasta)
