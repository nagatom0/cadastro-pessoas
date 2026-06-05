from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.login import GenerateLoginRequest, GenerateLoginResponse
from app.domain.login_generator import generate_logins
from app.repositories.login_repository import createLogin, delete_login

router = APIRouter()


@router.post("/logins/generate", response_model=GenerateLoginResponse)
def generate_login(req: GenerateLoginRequest, db: Session = Depends(get_db)):
    for cand in generate_logins(req.fullName):
        if createLogin(db, cand):
            return {"login": cand}
    raise HTTPException(status_code=409, detail="Não foi possível gerar um login único para esse nome")

@router.delete("/logins/{login}", status_code=204)
def deletar_login(login: str, db: Session = Depends(get_db)):
    delete_login(db,login)