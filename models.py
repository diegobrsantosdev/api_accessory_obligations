from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata

class Empresa(Base):
    __tablename__ = "Empresa"  # Nome da tabela no singular

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=True)
    cnpj = Column(String, nullable=True)
    endereco = Column(String, nullable=True)
    email = Column(String, nullable=True)
    telefone = Column(String, nullable=True)

#     # # Relacionamento com ObrigacaoAcessoria
#     # obrigacoes = relationship("ObrigacaoAcessoria", back_populates="empresa")


class ObrigacaoAcessoria(Base):
    __tablename__ = "obrigacao_acessoria"  # Nome da tabela no singular

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    periodicidade = Column(String, nullable=False)  # "mensal", "trimestral", "anual"
    # empresa_id = Column(Integer, ForeignKey("empresa.id"))  # Chave estrangeira

    # # Relacionamento com Empresa
    # empresa = relationship("Empresa", back_populates="obrigacoes")