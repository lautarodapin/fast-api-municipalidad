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