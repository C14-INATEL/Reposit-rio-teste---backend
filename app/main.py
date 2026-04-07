"""API Principal da Calculadora com endpoints para operações e histórico."""

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .models.operation import Base

# Importar o router dos controllers
from .controllers.operation_controller import router as operation_router

# Configuração do banco de dados SQLite para development/testes
DATABASE_URL = "sqlite:///./calculadora.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Instância da aplicação FastAPI
app = FastAPI(
    title="Calculadora com Histórico",
    description="API educacional para ensinar testes unitários e com mock",
    version="1.0.0"
)

# Registrar os routers (controllers)
app.include_router(operation_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
