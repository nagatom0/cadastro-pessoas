from pydantic import BaseModel
from datetime import date, datetime

from uuid import UUID
from datetime import date

class SearchCepResponse(BaseModel):
    cep: str
    address: str
    state: str
    city: str
    neighborhood: str
