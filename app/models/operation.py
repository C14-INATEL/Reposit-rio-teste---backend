"""Model para guardar o histórico de operações da calculadora."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Operation(Base):
    """Model que representa uma operação realizada na calculadora."""
    
    __tablename__ = "operations"
    
    id: int = Column(Integer, primary_key=True, index=True)
    tipo_operacao: str = Column(String, index=True)  # "soma", "subtrai", "multiplica", "divide", "media_ponderada", "desconto"
    operando_a: Optional[float] = Column(Float, nullable=True)  # Primeiro operando
    operando_b: Optional[float] = Column(Float, nullable=True)  # Segundo operando
    parametros: Optional[str] = Column(String, nullable=True)  # JSON com parâmetros adicionais (para operações complexas)
    resultado: float = Column(Float)  # Resultado da operação
    data_operacao: datetime = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"Operation(id={self.id}, operacao={self.tipo_operacao}, resultado={self.resultado})"
