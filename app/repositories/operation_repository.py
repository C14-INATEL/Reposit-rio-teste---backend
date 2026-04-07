"""Repository para operações com banco de dados."""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from datetime import datetime
from ..models.operation import Operation


class OperationRepository:
    """Repository para gerenciar operações no banco de dados."""
    
    @staticmethod
    def criar_operacao(
        db: Session,
        tipo_operacao: str,
        resultado: float,
        operando_a: Optional[float] = None,
        operando_b: Optional[float] = None,
        parametros: Optional[str] = None
    ) -> Operation:
        """
        Cria uma nova operação no banco de dados.
        
        Args:
            db: Sessão do SQLAlchemy
            tipo_operacao: Tipo de operação realizada
            resultado: Resultado da operação
            operando_a: Primeiro operando (opcional)
            operando_b: Segundo operando (opcional)
            parametros: Parâmetros adicionais em JSON (opcional)
            
        Returns:
            A operação criada
        """
        operacao = Operation(
            tipo_operacao=tipo_operacao,
            operando_a=operando_a,
            operando_b=operando_b,
            resultado=resultado,
            parametros=parametros,
            data_operacao=datetime.utcnow()
        )
        db.add(operacao)
        db.commit()
        db.refresh(operacao)
        return operacao
    
    @staticmethod
    def obter_historico(
        db: Session,
        limite: int = 100,
        offset: int = 0,
        tipo_operacao: Optional[str] = None
    ) -> tuple[int, list[Operation]]:
        """
        Obtém o histórico de operações com paginação e filtro opcional.
        
        Args:
            db: Sessão do SQLAlchemy
            limite: Máximo de resultados
            offset: Quantidade de registros a pular
            tipo_operacao: Filtrar por tipo de operação (opcional)
            
        Returns:
            Tupla (total_de_operacões, lista_de_operacões)
        """
        query = db.query(Operation)
        
        if tipo_operacao:
            query = query.filter(Operation.tipo_operacao == tipo_operacao)
        
        total = query.count()
        operacoes = query.order_by(desc(Operation.data_operacao)).offset(offset).limit(limite).all()
        
        return total, operacoes
    
    @staticmethod
    def limpar_historico(db: Session) -> int:
        """
        Limpa todo o histórico de operações.
        
        Returns:
            Número de operações deletadas
        """
        quantidade = db.query(Operation).delete()
        db.commit()
        return quantidade
