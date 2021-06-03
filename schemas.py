from pydantic  import BaseModel, AnyHttpUrl

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