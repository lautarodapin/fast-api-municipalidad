from typing import Optional
from pydantic import BaseModel, AnyHttpUrl, validator
from datetime import datetime
import re

class VariableEconomica(BaseModel):
    titulo: Optional[str] = None
    link: Optional[str] = None
    fecha: datetime
    valor: float
    serie: Optional[str] = None

    @validator('fecha', pre=True, always=True)
    def parse_datetime(cls, v, values, **kwargs):
        if isinstance(v, str):
            if re.compile(r'\d{1,2}/\d{1,2}/\d{1,4}').search(v):
                return datetime.strptime(v.strip(), "%d/%m/%Y")
        return v

    @validator('valor', pre=True, always=True)
    def parse_valor_to_float(cls, v, **kwargs):
        if isinstance(v, str):
            v = v.strip().replace('.', '')
            if v.isdigit():
                return float(v.replace('.', ''))
        return v