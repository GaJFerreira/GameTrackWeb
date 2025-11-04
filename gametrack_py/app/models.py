from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    jogos = relationship("Jogo", back_populates="owner", cascade="all,delete")
    metas = relationship("Meta", back_populates="owner", cascade="all,delete")

class Jogo(Base):
    __tablename__ = "jogos"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, nullable=False)
    plataforma = Column(String, nullable=True)
    horas_jogadas = Column(Integer, default=0)
    status = Column(String, default="Backlog")  # Backlog, Jogando, Concluido
    owner_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    owner = relationship("Usuario", back_populates="jogos")
    metas = relationship("Meta", back_populates="jogo", cascade="all,delete")

class Meta(Base):
    __tablename__ = "metas"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    concluida = Column(Boolean, default=False)
    data_limite = Column(Date, nullable=True)
    jogo_id = Column(Integer, ForeignKey("jogos.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    jogo = relationship("Jogo", back_populates="metas")
    owner = relationship("Usuario", back_populates="metas")
