"""Controller para operações da calculadora."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from ..schemas.operation import (
    OperationRequest,
    OperationResponse,
    MediaPonderadaRequest,
    DescontoRequest,
    HistoricoResponse
)
from ..repositories.operation_repository import OperationRepository
from ..services.calculate import Calculator

# Criar router para os endpoints
router = APIRouter(prefix="/api", tags=["Operações"])

# Instância da calculadora
calculator = Calculator()


def get_db():
    """Dependency para obter sessão do banco de dados."""
    from ..main import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===================== OPERAÇÕES BÁSICAS =====================

@router.post("/soma", response_model=OperationResponse)
def soma(request: OperationRequest, db: Session = Depends(get_db)):
    """Realiza uma soma entre dois números e salva no histórico."""
    resultado = calculator.soma(request.operando_a, request.operando_b)
    operacao = OperationRepository.criar_operacao(
        db=db,
        tipo_operacao="soma",
        operando_a=request.operando_a,
        operando_b=request.operando_b,
        resultado=resultado
    )
    return operacao


@router.post("/subtrai", response_model=OperationResponse)
def subtrai(request: OperationRequest, db: Session = Depends(get_db)):
    """Realiza uma subtração entre dois números e salva no histórico."""
    resultado = calculator.subtrai(request.operando_a, request.operando_b)
    operacao = OperationRepository.criar_operacao(
        db=db,
        tipo_operacao="subtrai",
        operando_a=request.operando_a,
        operando_b=request.operando_b,
        resultado=resultado
    )
    return operacao


@router.post("/multiplica", response_model=OperationResponse)
def multiplica(request: OperationRequest, db: Session = Depends(get_db)):
    """Realiza uma multiplicação entre dois números e salva no histórico."""
    resultado = calculator.multiplica(request.operando_a, request.operando_b)
    operacao = OperationRepository.criar_operacao(
        db=db,
        tipo_operacao="multiplica",
        operando_a=request.operando_a,
        operando_b=request.operando_b,
        resultado=resultado
    )
    return operacao


@router.post("/divide", response_model=OperationResponse)
def divide(request: OperationRequest, db: Session = Depends(get_db)):
    """Realiza uma divisão entre dois números e salva no histórico."""
    try:
        resultado = calculator.divide(request.operando_a, request.operando_b)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    operacao = OperationRepository.criar_operacao(
        db=db,
        tipo_operacao="divide",
        operando_a=request.operando_a,
        operando_b=request.operando_b,
        resultado=resultado
    )
    return operacao


# ===================== OPERAÇÕES COMPLEXAS =====================

@router.post("/media-ponderada", response_model=OperationResponse)
def media_ponderada(request: MediaPonderadaRequest, db: Session = Depends(get_db)):
    """
    Calcula a média ponderada de valores.
    
    EXCELENTE para ensinar testes com MOCK porque internamente
    chama soma e divide - que podem ser mockadas!
    """
    try:
        resultado = calculator.calcular_media_ponderada(request.valores, request.pesos)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Salva no histórico com parâmetros em JSON
    parametros = json.dumps({
        "valores": request.valores,
        "pesos": request.pesos
    })
    
    operacao = OperationRepository.criar_operacao(
        db=db,
        tipo_operacao="media_ponderada",
        resultado=resultado,
        parametros=parametros
    )
    return operacao


@router.post("/desconto", response_model=OperationResponse)
def desconto(request: DescontoRequest, db: Session = Depends(get_db)):
    """
    Calcula um valor com desconto percentual aplicado.
    
    Também ótimo para testes com MOCK porque usa multiplica e subtrai.
    """
    try:
        resultado = calculator.calcular_desconto(request.valor_original, request.percentual_desconto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    parametros = json.dumps({
        "valor_original": request.valor_original,
        "percentual_desconto": request.percentual_desconto
    })
    
    operacao = OperationRepository.criar_operacao(
        db=db,
        tipo_operacao="desconto",
        resultado=resultado,
        parametros=parametros
    )
    return operacao


# ===================== ENDPOINTS DE HISTÓRICO =====================

@router.get("/historico", response_model=HistoricoResponse)
def obter_historico(
    skip: int = 0,
    limit: int = 100,
    tipo: str = None,
    db: Session = Depends(get_db)
):
    """
    Obtém o histórico de operações com paginação e filtro opcional.
    
    Query parameters:
    - skip: Número de registros a pular (default: 0)
    - limit: Número máximo de registros (default: 100)
    - tipo: Filtrar por tipo de operação (opcional)
    """
    total, operacoes = OperationRepository.obter_historico(
        db=db,
        limite=limit,
        offset=skip,
        tipo_operacao=tipo
    )
    return {"total": total, "operacoes": operacoes}


@router.get("/historico/tipos")
def tipos_operacoes(db: Session = Depends(get_db)):
    """Retorna uma lista de todos os tipos de operações já realizadas."""
    from ..models.operation import Operation
    tipos = db.query(Operation.tipo_operacao).distinct().all()
    return {"tipos": [t[0] for t in tipos]}


@router.delete("/historico")
def limpar_historico(db: Session = Depends(get_db)):
    """Limpa todo o histórico de operações."""
    quantidade = OperationRepository.limpar_historico(db)
    return {"mensagem": f"Histórico limpo. {quantidade} operações deletadas."}


# ===================== HEALTH CHECK =====================

@router.get("/health")
def health_check():
    """Verifica se a API está funcionando."""
    return {"status": "ok", "mensagem": "API de Calculadora está rodando!"}
