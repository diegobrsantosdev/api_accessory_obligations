from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import DATABASE_URL  # Alterado para importar diretamente de settings


# Criando o engine de conexão com o banco de dados PostgreSQL
engine = create_engine(DATABASE_URL)

# Criando a sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
Base = declarative_base()
