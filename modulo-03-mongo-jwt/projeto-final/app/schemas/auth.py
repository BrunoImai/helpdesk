"""Contratos de autenticação."""

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AgenteOut(BaseModel):
    """Atendente como é devolvido pela API (nunca expõe o hash da senha)."""

    model_config = ConfigDict(from_attributes=True)

    id: PydanticObjectId
    nome: str
    email: EmailStr
    ativo: bool
