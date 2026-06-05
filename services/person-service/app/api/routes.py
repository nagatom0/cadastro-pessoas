from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import os
import httpx
from app.clients.login_service_client import (
gerar_login, LoginServiceError, LoginServiceUnavailableError, delete_login
)
from app.db.session import get_db
from app.schemas.create_person import CreatePersonRequest, CreatePersonResponse
from app.schemas.search_cep import SearchCepResponse
from app.repositories.persons_repository import createPerson
from app.clients.viacep_client import search_cep, CepInvalidoError,CepNaoEncontradoError, ViaCepUnavailableError

router = APIRouter()

@router.post("/person", response_model=CreatePersonResponse)
async def create_person(payload: CreatePersonRequest, db: Session = Depends(get_db)):
    try:
        login = await gerar_login(payload.fullName)
    except LoginServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except LoginServiceUnavailableError:
        raise HTTPException(status_code=503, detail="login-service indisponível")
    try:
        person = createPerson(db, payload, login)
    except IntegrityError:
        await delete_login(login)
        raise HTTPException(status_code=409, detail="CPF, e-mail ou login já cadastrado")
    return person

@router.get("/cep/{cep}", response_model=SearchCepResponse)
async def consultar_cep(cep: str):
    try:
        address = await search_cep(cep)
    except CepInvalidoError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except CepNaoEncontradoError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ViaCepUnavailableError:
        raise HTTPException(status_code=503, detail="ViaCEP indisponível")

    return {
        "cep": address.get("cep"),
        "city": address.get("city"),
        "state": address.get("state"),
        "neighborhood": address.get("neighborhood"),
        "address": address.get("address"),
    }