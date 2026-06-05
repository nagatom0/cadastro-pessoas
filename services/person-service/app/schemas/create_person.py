from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
from datetime import date, datetime

from uuid import UUID
from datetime import date
import re


class CreatePersonRequest(BaseModel):
    fullName: str = Field(min_length=1)
    cpf: str = Field(min_length=1)
    email: EmailStr
    birthday: date
    cep: str = Field(min_length=1)
    address: str = Field(min_length=1)
    number: str = Field(min_length=1)
    state: str = Field(min_length=1)
    city: str = Field(min_length=1)
    neighborhood: str = Field(min_length=1)

    @field_validator('cep')
    @classmethod
    def validate_cep(cls, v: str) -> str:
        digits = re.sub(r'\D', '', v)
        if digits:
            return digits

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        digits = re.sub(r'\D', '', v)
        if len(digits) != 11 or len(set(digits)) == 1:
            raise ValueError('CPF inválido')
        
        s = sum(int(digits[i]) * (10 - i) for i in range(9))
        if (s * 10 % 11) % 10 != int(digits[9]):
            raise ValueError('CPF inválido')
        
        s = sum(int(digits[i]) * (11 - i) for i in range(10))
        if (s * 10 % 11) % 10 != int(digits[10]):
            raise ValueError('CPF inválido')
        return digits
    
    @field_validator('fullName')
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        v = v.strip()                    
        v = re.sub(r'\s+', ' ', v)
        
        if not v:
            raise ValueError('Nome não pode ser vazio')
        
        if not re.fullmatch(r'[A-Za-z ]+', v):
            raise ValueError('Nome deve conter apenas letras A-Z e espaços (sem acentos)')
        
        if len(v.split()) < 2:                         
            raise ValueError('Informe nome e sobrenome')

        return v

    @field_validator('birthday')
    @classmethod
    def validate_birthday(cls, v: date) -> date:
        if v > date.today():
            raise ValueError('Data de nascimento não pode ser futura')
        
        return v



class CreatePersonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    login: str
    fullName: str
    cpf: str
    email: str
    birthday: date
    cep: str
    address: str
    number: str
    state: str
    city: str
    neighborhood: str
