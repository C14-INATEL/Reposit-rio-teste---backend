# 🧪 Guia Completo: Pytest em Python

Pytest é o framework de testes mais popular em Python. Ele é simples, poderoso e extensível.

---

## 📋 Índice

1. [Instalação](#instalação)
2. [Conceitos Básicos](#conceitos-básicos)
3. [Principais Funções](#principais-funções)
4. [Fixtures](#fixtures)
5. [Assertions](#assertions)
6. [Plugins Úteis](#plugins-úteis)
7. [Exemplos Práticos](#exemplos-práticos)

---

## Instalação

```bash
pip install pytest
pip install pytest-cov  # Para relatório de cobertura
```

---

## Conceitos Básicos

### O que é Pytest?
Um framework que facilita escrever testes em Python. Você escreve funções `test_*()` e o pytest as executa automaticamente.

```python
# Arquivo: test_calculator.py

def test_soma_simples():
    assert 2 + 2 == 4

def test_soma_negativa():
    assert -5 + 3 == -2
```

Executar testes:
```bash
pytest                          # Executa todos os testes
pytest test_calculator.py       # Executa um arquivo
pytest test_calculator.py::test_soma_simples  # Um teste específico
pytest -v                       # Modo verbose (mostra detalhes)
pytest -s                       # Mostra prints
pytest --cov                    # Cobertura de código
```

---

## Principais Funções

### 1️⃣ **assert**
A base de tudo. Valida se uma condição é verdadeira.

```python
def test_numeros():
    assert 5 > 3          # ✅ Passa
    assert 5 < 3          # ❌ Falha - AssertionError
    
def test_strings():
    assert "hello" == "hello"  # ✅
    assert "hello" != "world"  # ✅
```

### 2️⃣ **pytest.raises()**
Valida que uma exceção é lançada.

```python
import pytest

def dividir(a, b):
    if b == 0:
        raise ValueError("Não pode dividir por zero!")
    return a / b

def test_divisao_por_zero():
    with pytest.raises(ValueError):
        dividir(10, 0)  # ✅ Lança exceção como esperado

def test_divisao_por_zero_mensagem():
    with pytest.raises(ValueError, match="Não pode"):
        dividir(10, 0)  # ✅ Valida também a mensagem
```

### 3️⃣ **pytest.approx()**
Compara números decimais com tolerância (muito útil para floats!).

```python
def test_divisao_resultado_decimal():
    resultado = 10 / 3  # 3.333333...
    
    # ❌ Falha porque 3.333333... != 3.333
    # assert resultado == 3.333
    
    # ✅ Passa com tolerância
    assert resultado == pytest.approx(3.333, rel=1e-3)
```

### 4️⃣ **pytest.mark.parametrize()**
Executa o mesmo teste com valores diferentes (muito eficiente!).

```python
import pytest

@pytest.mark.parametrize("entrada,esperado", [
    (2 + 2, 4),
    (10 - 5, 5),
    (3 * 3, 9),
    (20 / 4, 5),
])
def test_operacoes(entrada, esperado):
    assert entrada == esperado
```

Pytest executa o teste 4 vezes, uma para cada conjunto de valores.

### 5️⃣ **pytest.mark.skip()**
Pula um teste (por enquanto).

```python
@pytest.mark.skip(reason="Ainda não implementado")
def test_feature_nova():
    pass
```

### 6️⃣ **pytest.mark.xfail()**
Marca um teste que se ESPERA que falhe (fail esperado).

```python
@pytest.mark.xfail(reason="Bug conhecido no código")
def test_divisao_inteira():
    assert 5 / 2 == 2.5  # Falha, mas é esperado
```

### 7️⃣ **pytest.mark.slow()**
Marca testes lentos para executá-los separadamente.

```python
@pytest.mark.slow
def test_processa_arquivo_grande():
    # Testa operação demorada
    pass
```

Executar apenas testes rápidos:
```bash
pytest -m "not slow"
```

---

## Fixtures

Fixtures são funções que preparam dados/configurações para os testes.

### Fixture Simples

```python
import pytest

@pytest.fixture
def calculadora():
    """Cria uma calculadora para cada teste"""
    from app.services.calculate import Calculator
    return Calculator()

def test_soma(calculadora):
    resultado = calculadora.soma(5, 3)
    assert resultado == 8
```

> Cada teste recebe uma **nova instância** de `calculadora`

### Fixture com Setup/Teardown

```python
@pytest.fixture
def banco_dados():
    db = criar_conexao()  # Setup: preparar
    
    yield db  # Teste usa isso aqui
    
    db.fechar()  # Teardown: limpar
```

### Fixture com Escopo

```python
# Scope: function (padrão - cria nova para cada teste)
@pytest.fixture(scope="function")
def calc():
    return Calculator()

# Scope: class (reutiliza para todos os testes da classe)
@pytest.fixture(scope="class")
def db():
    return Database()

# Scope: module (reutiliza para todo o arquivo)
@pytest.fixture(scope="module")
def config():
    return carregar_config()

# Scope: session (reutiliza para TODA a execução)
@pytest.fixture(scope="session")
def servidor():
    s = iniciar_servidor()
    yield s
    s.parar()
```

### Fixture Parametrizada

```python
@pytest.fixture(params=[10, 20, 30, 40])
def valor(request):
    return request.param

def test_com_multiplos_valores(valor):
    assert valor > 0  # Testa com 10, 20, 30, 40
```

---

## Assertions

Validações com mensagens customizadas:

```python
# Básico
assert x == y

# Com mensagem
assert x == y, f"Esperava {y}, recebeu {x}"

# Comparações
assert x > y
assert x < y
assert x >= y
assert x <= y
assert x != y

# Membros
assert item in lista
assert chave in dicionario

# Identidade
assert x is y         # Mesmo objeto na memória
assert x is not y     # Objetos diferentes

# Booleano
assert condicao       # True
assert not condicao   # False

# Nulidade
assert x is None
assert x is not None
```

---

## Plugins Úteis

### pytest-cov (Cobertura de código)
```bash
pip install pytest-cov

pytest --cov=app --cov-report=html
# Gera relatório HTML em htmlcov/index.html
```

### pytest-mock
```bash
pip install pytest-mock

def test_com_mocker(mocker):
    mock = mocker.patch('modulo.funcao')
    # Simples de usar!
```

### pytest-timeout
```bash
pip install pytest-timeout

@pytest.mark.timeout(5)  # Falha se demorar mais de 5 segundos
def test_rapido():
    pass
```

### pytest-xdist (Testes em paralelo)
```bash
pip install pytest-xdist

pytest -n auto  # Executa em múltiplos processos
```

---

## Exemplos Práticos

### Exemplo 1: Estrutura Básica de Testes

```python
import pytest
from app.services.calculate import Calculator

class TestCalculador:
    """Agrupa testes relacionados"""
    
    @pytest.fixture
    def calc(self):
        return Calculator()
    
    def test_soma_positivos(self, calc):
        assert calc.soma(5, 3) == 8
    
    def test_soma_negativos(self, calc):
        assert calc.soma(-5, -3) == -8
    
    def test_divisao_por_zero(self, calc):
        with pytest.raises(ValueError):
            calc.divide(10, 0)
```

### Exemplo 2: Parametrização

```python
@pytest.mark.parametrize("a,b,esperado", [
    (5, 3, 8),      # Teste 1
    (-5, -3, -8),   # Teste 2
    (10, -4, 6),    # Teste 3
])
def test_soma_parametrizado(a, b, esperado):
    calc = Calculator()
    assert calc.soma(a, b) == esperado
```

Isso executa 3 testes, um para cada linha!

### Exemplo 3: Fixtures com Dependências

```python
@pytest.fixture
def usuario_fixo():
    """Fixture que cria um usuário"""
    return {"id": 1, "nome": "João", "email": "joao@mail.com"}

@pytest.fixture
def usuario_admin(usuario_fixo):
    """Depende de usuario_fixo e adiciona perfil"""
    usuario_fixo["perfil"] = "admin"
    return usuario_fixo

def test_usuario_admin(usuario_admin):
    assert usuario_admin["perfil"] == "admin"
    assert usuario_admin["nome"] == "João"
```

### Exemplo 4: Setup/Teardown

```python
@pytest.fixture
def conexao_banco():
    db = Database()
    db.conectar()
    
    yield db  # Aqui o teste executa
    
    db.desconectar()  # Limpa depois

def test_criar_usuario(conexao_banco):
    usuario = Usuario(conexao_banco, "João")
    assert usuario.id is not None
    # BD é fechado automaticamente após o teste
```

### Exemplo 5: Assertions com Mensagens

```python
def test_calculo_complexo(calc):
    resultado = calc.calcular_media_ponderada([10, 20], [1, 1])
    
    assert resultado == 15, \
        f"Esperava 15, mas recebeu {resultado}. Valores: [10, 20], Pesos: [1, 1]"
```

### Exemplo 6: Marcar Testes

```python
@pytest.mark.slow
def test_processa_arquivo_grande():
    # Operação lenta...
    pass

@pytest.mark.skip(reason="Será implementado na próxima sprint")
def test_nova_feature():
    pass

@pytest.mark.xfail(reason="Bug #123 - ainda não corrigido")
def test_comportamento_bugado():
    pass

# Executar:
# pytest --co -q                # Lista todos os testes
# pytest -m slow                # Apenas testes lentos
# pytest -m "not slow"          # Todos MENOS os lentos
# pytest -v                      # Mostra qual passou/falhou
```

---

## Arquivo conftest.py

Um arquivo especial onde você coloca fixtures compartilhadas:

```python
# conftest.py (na raiz do projeto)
import pytest
from app.services.calculate import Calculator

@pytest.fixture
def calculator():
    """Disponível para TODOS os testes"""
    return Calculator()

@pytest.fixture(scope="session")
def config():
    """Carregado UMA VEZ para toda a sessão"""
    return load_config()
```

Agora qualquer teste pode usar `calculator` sem precisar defini-lo!

---

## Configuração: pytest.ini

```ini
# pytest.ini (na raiz do projeto)
[pytest]
# Padrão de arquivos/funções de teste
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Opções padrão
addopts = 
    -v
    --strict-markers
    -ra

# Markers customizados
markers =
    slow: marca teste como lento
    integration: teste de integração
    unit: teste unitário
    
# Caminhos para buscar testes
testpaths = tests app/tests

# Ignorar
norecursedirs = .git venv
```

---

## 📊 Executar Testes

```bash
# Básico
pytest                                  # Todos
pytest test_file.py                     # Um arquivo
pytest test_file.py::TestClass          # Uma classe
pytest test_file.py::test_function      # Uma função

# Opções úteis
pytest -v                               # Verbose (detalhado)
pytest -s                               # Mostra print()
pytest -x                               # Para no primeiro erro
pytest -k "soma"                        # Apenas testes com "soma" no nome
pytest -m slow                          # Apenas tests com marca @slow
pytest --collect-only                   # Lista testes sem executar
pytest --lf                             # Último que falhou
pytest --ff                             # Falhos primeiro
pytest --co -q                          # Lista curta

# Cobertura
pytest --cov=app                        # Cobertura do módulo 'app'
pytest --cov=app --cov-report=html      # Gera HTML
pytest --cov=app --cov-report=term-missing  # Mostra linhas não cobertas

# Paralelizar
pytest -n auto                          # Múltiplos processos (precisa pytest-xdist)

# Debug
pytest -vv                              # Muito verbose
pytest --tb=long                        # Traceback detalhado
pytest --capture=no                     # Desativa captura (mostra tudo)
```

---

## 🔗 Principais Decoradores

| Decorador | O que faz |
|---|---|
| `@pytest.mark.skip` | Pula o teste |
| `@pytest.mark.skipif(condicao)` | Pula se condição for True |
| `@pytest.mark.xfail` | Espera que falhe |
| `@pytest.mark.timeout(segundos)` | Timeout do teste |
| `@pytest.mark.parametrize` | Múltiplos inputs |
| `@pytest.mark.custom` | Marca customizada |

---

## 💡 Boas Práticas

✅ **um assert por teste** - Testa uma coisa  
✅ **Use nomes descritivos** - `test_soma_positivos`, not `test1`  
✅ **Use fixtures** - Não repita setup em todos os testes  
✅ **Organize em classes** - Agrupa testes relacionados  
✅ **Use parametrize** - Para testar múltiplos valores  
✅ **Teste casos edge** - Zero, negativo, muito grande, etc  
❌ **Não use setUp/tearDown** - Use fixtures ao invés  
❌ **Não dependa de ordem** - Testes devem ser independentes  
❌ **Não faça I/O real** - Use mock para BD, HTTP, arquivos  

---

## 📚 Referência Rápida

```python
# Imports
import pytest
from unittest.mock import Mock, patch

# Assertions
assert condicao
assert x == y, "Mensagem"
assert x in lista
assert x is not None

# Exceções
with pytest.raises(ValueError):
    funcao()

with pytest.raises(ValueError, match="mensagem"):
    funcao()

# Números decimais
assert resultado == pytest.approx(3.14, rel=1e-2)

# Fixture
@pytest.fixture
def dados():
    return [1, 2, 3]

# Parametrize
@pytest.mark.parametrize("x,y", [(1, 2), (3, 4)])

# Skip/XFail
@pytest.mark.skip
@pytest.mark.xfail
@pytest.mark.slow

# Executar
pytest          # Tudo
pytest -v       # Verbose
pytest -s       # Com prints
pytest -k nome  # Por padrão
pytest --cov    # Cobertura
```

---

**Próximo:** Veja o [Guia Completo do Mock](./README_MOCK.md)
