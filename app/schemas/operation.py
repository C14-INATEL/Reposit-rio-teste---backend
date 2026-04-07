"""Schemas para serialização/desserialização de dados dos endpoints."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OperationRequest(BaseModel):
    """Schema para requisição de operações simples (soma, subtração, multiplicação, divisão)."""
    operando_a: float
    operando_b: float


class MediaPonderadaRequest(BaseModel):
    """Schema para calculo de média ponderada."""
    valores: list[float]
    pesos: list[float]


class DescontoRequest(BaseModel):
    """Schema para calculo de desconto."""
    valor_original: float
    percentual_desconto: float


class OperationResponse(BaseModel):
    """Schema para resposta de operação."""
    id: int
    tipo_operacao: str
    operando_a: Optional[float] = None
    operando_b: Optional[float] = None
    resultado: float
    data_operacao: datetime
    
    class Config:
        from_attributes = True  # Para SQLAlchemy models


class HistoricoResponse(BaseModel):
    """Schema para listar histórico de operações."""
    total: int
    operacoes: list[OperationResponse]
