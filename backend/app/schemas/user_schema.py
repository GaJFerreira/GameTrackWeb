from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    """
    Define os dados que SÃO ENVIADOS pelo usuário no formulário.
    """
    email: EmailStr
    # Na arquitetura final, não passamos a senha aqui para evitar expor hashs
    # Mas para o teste de criação, vamos mantê-lo:
    password: str
    steam_id: str  # Mudamos para STR, pois SteamIDs são grandes (64bit)


class UserCreate(UserBase):
    """ Schema usado para criar um novo usuário (dados de entrada). """
    # Não pedimos o ID na criação.
    pass


class User(UserBase):
    """
    Schema usado para ler os dados de um usuário DEPOIS de salvo no banco.
    """
    id: str  # O ID do Firebase (UID), que é sempre uma string

    class Config:
        # Correção do erro de digitação: from_attributes
        from_attributes = True