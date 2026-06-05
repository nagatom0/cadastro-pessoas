from pydantic import BaseModel, Field


class GenerateLoginRequest(BaseModel):
    fullName: str = Field(min_length=1)


class GenerateLoginResponse(BaseModel):
    login: str