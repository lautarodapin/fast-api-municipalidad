from pydantic  import BaseModel

class Ordenanza(BaseModel):
    año: int
    numero: str
    titulo: str
    extracto: str
    archivo: str