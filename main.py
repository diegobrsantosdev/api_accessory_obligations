from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from models import Empresa, ObrigacaoAcessoria
from schemas import EmpresaCreate, Empresa, ObrigacaoAcessoriaCreate, ObrigacaoAcessoria
from database import SessionLocal, engine, Base

app = FastAPI()

# Função para obter a sessão do banco de dados


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota POST /empresas/ - Criar uma nova empresa


@app.post("/empresas/", response_model=Empresa)
def criar_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = Empresa(**empresa.model_dump())
    db.add(db_empresa)
    try:
        db.commit()
        db.refresh(db_empresa)
        return db_empresa
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar empresa.")

# Rota GET /empresas/ - Listar todas as empresas


@app.get("/empresas/", response_model=List[Empresa])
def listar_empresas(db: Session = Depends(get_db)):
    empresas = db.query(Empresa).all()
    if not empresas:
        raise HTTPException(status_code=404, detail="Nenhuma empresa cadastrada.")
    return empresas

# Rota GET /empresas/{empresa_id} - Obter uma empresa específica


@app.get("/empresas/{empresa_id}", response_model=Empresa)
def obter_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    return empresa


# Rota PUT /empresas/{empresa_id} - Atualizar uma empresa


@app.put("/empresas/{empresa_id}", response_model=Empresa)
def atualizar_empresa(empresa_id: int, empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    for key, value in empresa.model_dump().items():
        setattr(db_empresa, key, value)
    try:
        db.commit()
        db.refresh(db_empresa)
        return db_empresa
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro ao atualizar empresa.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar empresa.")

# Rota DELETE /empresas/{empresa_id} - Excluir uma empresa


@app.delete("/empresas/{empresa_id}")
def excluir_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    try:
        db.delete(empresa)
        db.commit()
        return {"message": "Empresa excluída com sucesso."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Empresa possui vínculos e não pode ser excluída.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao excluir empresa.")


# Rotas para ObrigacaoAcessoria

@app.post("/empresas/{empresa_id}/obrigacoes/", response_model=ObrigacaoAcessoria)
def criar_obrigacao(empresa_id: int, obrigacao: ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    # Verifica se a empresa existe
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")

    # Cria a obrigação acessória
    db_obrigacao = ObrigacaoAcessoria(**obrigacao.model_dump(), empresa_id=empresa_id)
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao


@app.get("/empresas/{empresa_id}/obrigacoes/", response_model=list[ObrigacaoAcessoria])
def listar_obrigacoes(empresa_id: int, db: Session = Depends(get_db)):
    # Verifica se a empresa existe
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")

    # Retorna todas as obrigações da empresa
    return db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.empresa_id == empresa_id).all()


@app.get("/empresas/{empresa_id}/obrigacoes/{obrigacao_id}", response_model=ObrigacaoAcessoria)
def obter_obrigacao(empresa_id: int, obrigacao_id: int, db: Session = Depends(get_db)):
    # Verifica se a empresa existe
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")

    # Retorna a obrigação específica
    db_obrigacao = db.query(ObrigacaoAcessoria).filter(
        ObrigacaoAcessoria.id == obrigacao_id,
        ObrigacaoAcessoria.empresa_id == empresa_id
    ).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação acessória não encontrada.")
    return db_obrigacao


@app.put("/empresas/{empresa_id}/obrigacoes/{obrigacao_id}", response_model=ObrigacaoAcessoria)
def atualizar_obrigacao(empresa_id: int, obrigacao_id: int, obrigacao: ObrigacaoAcessoriaCreate,
                        db: Session = Depends(get_db)):
    # Verifica se a empresa existe
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")

    # Verifica se a obrigação existe
    db_obrigacao = db.query(ObrigacaoAcessoria).filter(
        ObrigacaoAcessoria.id == obrigacao_id,
        ObrigacaoAcessoria.empresa_id == empresa_id
    ).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação acessória não encontrada.")

    # Atualiza os dados da obrigação
    for key, value in obrigacao.model_dump().items():
        setattr(db_obrigacao, key, value)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao


@app.delete("/empresas/{empresa_id}/obrigacoes/{obrigacao_id}")
def excluir_obrigacao(empresa_id: int, obrigacao_id: int, db: Session = Depends(get_db)):
    # Verifica se a empresa existe
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")

    # Verifica se a obrigação existe
    db_obrigacao = db.query(ObrigacaoAcessoria).filter(
        ObrigacaoAcessoria.id == obrigacao_id,
        ObrigacaoAcessoria.empresa_id == empresa_id
    ).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação acessória não encontrada.")

    # Exclui a obrigação
    db.delete(db_obrigacao)
    db.commit()
    return {"message": "Obrigação acessória excluída com sucesso"}
