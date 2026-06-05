import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, func, Column, Date

class Base(DeclarativeBase):
    pass

class CreatePerson(Base):
    __tablename__ = "persons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fullName = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    birthday = Column(Date, nullable=False)
    cep = Column(String, nullable=False)
    address = Column(String, nullable=False)
    number = Column(String, nullable=False)
    state = Column(String, nullable=False)
    city = Column(String, nullable=False)
    neighborhood = Column(String, nullable=False)
    login = Column(String(7), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())