from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.models import CreateLogin


def createLogin(db: Session, login: str) -> bool:
    try:
        db.add(CreateLogin(login=login))
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False

def delete_login(db: Session, login: str) -> None:
    """Remove um login reservado. Idempotente: não erra se não existir."""
    obj = db.get(CreateLogin, login)
    if obj:
        db.delete(obj)
        db.commit()