# 🧪 Guia Completo: unittest.mock em Python

A biblioteca `unittest.mock` é essencial para testes isolados e confiáveis. Ela permite mockar (substituir) objetos, funções e dependências nos seus testes.

---

## 📋 Índice

1. [Conceitos Básicos](#conceitos-básicos)
2. [Principais Classes e Funções](#principais-classes-e-funções)
3. [Mock()](#mock)
4. [patch()](#patch)
5. [Assertions](#assertions)
6. [Exemplos Práticos](#exemplos-práticos)

---

## Conceitos Básicos

### O que é Mock?
Um **mock** é um objeto "falso" que simula o comportamento de um objeto real. Usado em testes para:
- Isolar o código testado
- Simular comportamentos sem usar APIs, BD, arquivos
- Validar que funções foram chamadas corretamente
- Contorlar o comportamento de dependências

---

## Principais Classes e Funções

### 1️⃣ **Mock()**
Cria um objeto mock que simula qualquer coisa.

```python
from unittest.mock import Mock

# Criar um mock simples
mock_obj = Mock()
mock_obj.metodo.return_value = 100

resultado = mock_obj.metodo(10, 20)
print(resultado)  # 100
```

**Propriedades úteis:**
- `return_value`: O que a função retorna
- `side_effect`: Lista de valores ou exceção
- `call_count`: Quantas vezes foi chamada
- `called`: Se foi chamada (True/False)
- `call_args`: Os argumentos da última chamada
- `call_args_list`: Lista de todas as chamadas

---

### 2️⃣ **MagicMock()**
Um Mock mais poderoso que suporta operadores mágicos (`__add__`, `__mul__`, etc).

```python
from unittest.mock import MagicMock

mock_num = MagicMock()
mock_num.__add__.return_value = 100

resultado = mock_num + 50  # Usa __add__
print(resultado)  # 100

# Também suporta iteração
mock_list = MagicMock()
mock_list.__iter__.return_value = iter([1, 2, 3])
print(list(mock_list))  # [1, 2, 3]
```

---

### 3️⃣ **patch() - O mais importante!**
Substitui uma função/classe por um mock durante o teste.

#### Variações:

**A) Como context manager (com `with`):**
```python
from unittest.mock import patch

def test_algo():
    with patch('modulo.funcao') as mock_func:
        mock_func.return_value = 100
        # Testa aqui
        resultado = minha_funcao()
        assert resultado == 100
```

**B) Como decorador:**
```python
@patch('modulo.funcao')
def test_algo(mock_func):
    mock_func.return_value = 100
    # Testa aqui
```

**C) patch.object() - Para mockar métodos de uma classe:**
```python
from unittest.mock import patch

class Calculadora:
    def soma(self, a, b):
        return a + b

with patch.object(Calculadora, 'soma', return_value=999) as mock_soma:
    calc = Calculadora()
    print(calc.soma(5, 5))  # 999 (não 10!)
```

**D) patch.multiple() - Para mockar vários de uma vez:**
```python
with patch.multiple('modulo',
                    funcao1=Mock(return_value=10),
                    funcao2=Mock(return_value=20)):
    # Ambas estão mockadas
```

---

### 4️⃣ **return_value**
Define o valor retornado quando o mock é chamado.

```python
mock = Mock(return_value=42)
print(mock())  # 42
print(mock(1, 2, 3))  # 42 (argumentos não importam)
```

---

### 5️⃣ **side_effect**
Controla o comportamento de chamadas múltiplas ou simula exceções.

**Múltiplos valores:**
```python
mock = Mock(side_effect=[10, 20, 30])
print(mock())  # 10
print(mock())  # 20
print(mock())  # 30
# print(mock())  # ❌ StopIteration!
```

**Simular exceção:**
```python
mock = Mock(side_effect=ValueError("Erro!"))
mock()  # ❌ Lança ValueError
```

**Função customizada:**
```python
def efeito(x):
    return x * 2

mock = Mock(side_effect=efeito)
print(mock(5))  # 10
print(mock(10))  # 20
```

---

### 6️⃣ **spec - Validação de interface**
Garante que o mock só tem atributos do objeto real.

```python
from unittest.mock import Mock

class Banco:
    def depositar(self, valor):
        pass

mock_banco = Mock(spec=Banco)
mock_banco.depositar(100)  # ✅ OK

# Isso vai dar erro porque 'sacar' não existe em Banco:
# mock_banco.sacar(50)  # ❌ AttributeError
```

---

## Assertions

Métodos para validar se e como um mock foi chamado:

### **assert_called()**
Verifica se foi chamada (sem importar argumentos).

```python
mock = Mock()
mock()
mock.assert_called()  # ✅

# Sem chamar:
mock2 = Mock()
mock2.assert_called()  # ❌ AssertionError
```

### **assert_called_once()**
Verifica se foi chamada EXATAMENTE UMA VEZ.

```python
mock = Mock()
mock()
mock.assert_called_once()  # ✅

mock()  # Segunda chamada
mock.assert_called_once()  # ❌ Falha! Foi chamada 2 vezes
```

### **assert_called_with(args, **kwargs)**
Verifica se foi chamada COM ESSES ARGUMENTOS ESPECÍFICOS.

```python
mock = Mock()
mock(10, 20, debug=True)

mock.assert_called_with(10, 20, debug=True)  # ✅
mock.assert_called_with(10, 20)  # ❌ Falta debug=True
```

### **assert_called_once_with()**
Uma chamada com argumentos específicos.

```python
mock = Mock()
mock(5, 5)

mock.assert_called_once_with(5, 5)  # ✅
```

### **assert_any_call()**
Verifica se foi chamada COM ESSES ARGUMENTOS (não precisa ser a última).

```python
mock = Mock()
mock(1, 1)
mock(2, 2)
mock(3, 3)

mock.assert_any_call(2, 2)  # ✅ Foi chamada com (2, 2)
```

### **assert_not_called()**
Verifica que NÃO foi chamada.

```python
mock = Mock()
mock.assert_not_called()  # ✅

mock()
mock.assert_not_called()  # ❌ Falha
```

### **assert_has_calls()**
Verifica uma sequência de chamadas.

```python
from unittest.mock import call

mock = Mock()
mock(1)
mock(2)
mock(3)

mock.assert_has_calls([call(1), call(2), call(3)])  # ✅
```

---

## Exemplos Práticos

### Exemplo 1: Mockar requisição HTTP
```python
from unittest.mock import patch
import requests

def buscar_usuario(id):
    response = requests.get(f'https://api.com/users/{id}')
    return response.json()

def test_buscar_usuario():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'id': 1, 'nome': 'João'}
        
        resultado = buscar_usuario(1)
        
        assert resultado == {'id': 1, 'nome': 'João'}
        mock_get.assert_called_once_with('https://api.com/users/1')
```

### Exemplo 2: Mockar banco de dados
```python
from unittest.mock import Mock

class UsuarioRepository:
    def __init__(self, db):
        self.db = db
    
    def criar(self, nome):
        return self.db.insert('usuarios', {'nome': nome})

def test_criar_usuario():
    mock_db = Mock()
    mock_db.insert.return_value = 1  # ID do usuário criado
    
    repo = UsuarioRepository(mock_db)
    usuario_id = repo.criar('Maria')
    
    assert usuario_id == 1
    mock_db.insert.assert_called_once_with('usuarios', {'nome': 'Maria'})
```

### Exemplo 3: Isolar funções
```python
from unittest.mock import patch

class Calculadora:
    def media_ponderada(self, valores, pesos):
        soma_ponderada = sum(v*p for v, p in zip(valores, pesos))
        soma_pesos = sum(pesos)
        return soma_ponderada / soma_pesos
    
    def divide(self, a, b):
        return a / b

def test_media_ponderada_mock_divide():
    calc = Calculadora()
    
    with patch.object(calc, 'divide', return_value=99) as mock_divide:
        resultado = calc.media_ponderada([10, 20, 30], [1, 2, 3])
        
        # O resultado é 99 porque mockamos divide
        assert resultado == 99
        # Verificamos que divide foi chamada
        assert mock_divide.called
```

### Exemplo 4: Simular múltiplos cenários
```python
from unittest.mock import Mock

def processar_dados(api):
    primeiro = api.buscar(1)
    segundo = api.buscar(2)
    terceiro = api.buscar(3)
    return [primeiro, segundo, terceiro]

def test_processar_dados():
    mock_api = Mock()
    
    # Cada chamada retorna um valor diferente
    mock_api.buscar.side_effect = [
        {'id': 1, 'valor': 100},
        {'id': 2, 'valor': 200},
        {'id': 3, 'valor': 300}
    ]
    
    resultado = processar_dados(mock_api)
    
    assert len(resultado) == 3
    assert resultado[0]['valor'] == 100
    assert resultado[2]['valor'] == 300
```

### Exemplo 5: Simular exceção
```python
from unittest.mock import Mock

class ProcessadorArquivo:
    def __init__(self, leitor):
        self.leitor = leitor
    
    def processar(self):
        try:
            dados = self.leitor.ler_arquivo()
            return dados.upper()
        except FileNotFoundError:
            return "Arquivo não encontrado"

def test_arquivo_nao_encontrado():
    mock_leitor = Mock()
    mock_leitor.ler_arquivo.side_effect = FileNotFoundError("Arquivo não existe")
    
    processador = ProcessadorArquivo(mock_leitor)
    resultado = processador.processar()
    
    assert resultado == "Arquivo não encontrado"
```

---

## 🔗 Propriedades Úteis do Mock

| Propriedade | O que faz |
|---|---|
| `mock.called` | Retorna True se foi chamada |
| `mock.call_count` | Número de vezes que foi chamada |
| `mock.call_args` | Argumentos da última chamada |
| `mock.call_args_list` | Lista de TODAS as chamadas |
| `mock.return_value` | Valor retornado |
| `mock.side_effect` | Controla múltiplas chamadas |
| `mock.mock_calls` | Todas as chamadas e sub-chamadas |

---

## 💡 Boas Práticas

✅ **Use mock para isolar testes** - Teste uma coisa por vez
✅ **Mock I/O (arquivos, BD, HTTP)** - Deixa testes rápidos
✅ **Mock é para dependências** - Não mockne o código que você está testando
✅ **Valide chamadas com assertions** - Garanta que o código usa mock corretamente
❌ **Não abuse de mock** - Se mocka tudo, não testa nada
❌ **Mock não deve ser complexo** - Se é, o código também é

---

## 📚 Referência Rápida

```python
# Criar
Mock()                          # Mock simples
MagicMock()                     # Mock com operadores
Mock(return_value=X)            # Com valor pré-definido
Mock(side_effect=[a,b,c])       # Múltiplos retornos
Mock(spec=Classe)               # Valida interface

# Usar em contexto
with patch('modulo.funcao') as mock:
    pass

# Como decorador
@patch('modulo.funcao')
def test(mock):
    pass

# Validar
mock.assert_called()
mock.assert_called_once()
mock.assert_called_with(args)
mock.assert_called_once_with(args)
mock.assert_any_call(args)
mock.assert_not_called()

# Inspecionar
mock.called                     # True/False
mock.call_count                 # Quantas vezes
mock.call_args                  # Última chamada
mock.call_args_list             # Todas as chamadas
```

---

**Próximo:** Veja o [Guia Completo do Pytest](./README_PYTEST.md)
