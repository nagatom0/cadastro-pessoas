from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.create_person import CreatePersonRequest, CreatePersonResponse
from app.db.models import CreatePerson


def createPerson(db: Session, payload: CreatePersonRequest, login: str) -> CreatePersonResponse:
    try:
        person = CreatePerson(
            fullName=payload.fullName,
            cpf=payload.cpf,
            email=payload.email,
            birthday=payload.birthday,
            cep=payload.cep,
            address=payload.address,
            number = payload.number,
            state = payload.state,
            city = payload.city,
            neighborhood = payload.neighborhood,
            login=login,                 
            )
        db.add(person)
        db.commit()
        db.refresh(person)
        return person
    except IntegrityError:
        db.rollback()
        raise