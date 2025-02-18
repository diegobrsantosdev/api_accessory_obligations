from pydantic import BaseModel

# Schema para criação de empresa

class EmpresaCreate(BaseModel):
    id: int
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefone: str

    class Config:
        json_schema_extra = {  # Substituiu schema_extra
            "example": {
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste, 123",
                "email": "contato@empresateste.com",
                "telefone": "11999999999"
            }
        }

# Schema para resposta de empresa
class Empresa(BaseModel):
    id: int
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefone: str

    class Config:
        from_attributes = True  # Substituiu orm_mode
        json_schema_extra = {  # Substituiu schema_extra
            "example": {
                "id": 1,
                "nome": "Empresa Teste",
                "cnpj": "12345678901234",
                "endereco": "Rua Teste, 123",
                "email": "contato@empresateste.com",
                "telefone": "11999999999"
            }
        }

# Schema para criação de obrigação acessória
class ObrigacaoAcessoriaCreate(BaseModel):
    nome: str
    periodicidade: str  # "mensal", "trimestral", "anual"
    empresa_id: int

    class Config:
        json_schema_extra = {  # Substituiu schema_extra
            "example": {
                "nome": "Declaração de Imposto de Renda",
                "periodicidade": "anual",
                "empresa_id": 1
            }
        }

# Schema para resposta de obrigação acessória
class ObrigacaoAcessoria(BaseModel):
    id: int
    nome: str
    periodicidade: str
    empresa_id: int

    class Config:
        from_attributes = True  # Substituiu orm_mode
        json_schema_extra = {  # Substituiu schema_extra
            "example": {
                "id": 1,
                "nome": "Declaração de Imposto de Renda",
                "periodicidade": "anual",
                "empresa_id": 1
            }
        }