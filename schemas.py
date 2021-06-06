from typing import Any, List, Optional
from pydantic  import BaseModel, AnyHttpUrl, validator
from datetime import datetime
import re
class Ordenanza(BaseModel):
    año: int
    numero: str
    titulo: str
    extracto: str
    archivo: AnyHttpUrl


class Carta(BaseModel):
    imagen: AnyHttpUrl
    cargo: str
    cargo_hcd: str
    periodo: str
    biografia: str

class Consejal(BaseModel):
    nombre: str
    bloque: str
    periodo: str
    url: AnyHttpUrl

class OrdenDia(BaseModel):
    id: int
    url: AnyHttpUrl
    dia: int
    mes: int
    img: AnyHttpUrl
    codigo: str
    texto: str


class FacebookPost(BaseModel):
    post_id: str
    count_declaracion_dias: Optional[int]
    count_proyecto_comunicacion: Optional[int]
    text: str
    post_text: str
    time: datetime
    post_url: AnyHttpUrl
    user_id: str
    username: str
    user_url: AnyHttpUrl
    shared_text: str = ""
    image: Optional[AnyHttpUrl] = ""
    images: Optional[List[AnyHttpUrl]] = []
    images_description: Optional[List[str]] = []


    @validator('count_declaracion_dias', pre=True, always=True)
    def contar_proyectos_de_declaracion(cls, v, values, **kwargs):
        post_text = values["post_text"]
        s = " ".join(list(map(
                lambda x: x.strip().lower().replace('.', ' ').replace('#', ''), 
                filter(lambda x: x ,post_text.split('\n'))
        )))
        coincidencias = re.compile(r'\bproyecto de comunicaci.n|\bd.a [\w ]+').findall(s)
        counter = 0
        for coincidencia in coincidencias:
            if re.compile(r'd.a').search(coincidencia):
                counter += 1

        return counter

    @validator('count_proyecto_comunicacion', pre=True, always=True)
    def contar_proyectos_de_comunicacion(cls, v, values, **kwargs):
        post_text = values["post_text"]
        s = " ".join(list(map(
                lambda x: x.strip().lower().replace('.', ' ').replace('#', ''), 
                filter(lambda x: x ,post_text.split('\n'))
        )))
        coincidencias = re.compile(r'\bproyecto de comunicaci.n|\bd.a [\w ]+').findall(s)
        counter = 0
        for coincidencia in coincidencias:
            if re.compile(r'comunicaci.n').search(coincidencia):
                counter += 1

        return counter