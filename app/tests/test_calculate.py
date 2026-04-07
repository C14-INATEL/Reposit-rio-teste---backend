"""Testes para a classe Calculator."""

import pytest
from unittest.mock import Mock, patch, call
from ..services.calculate import Calculator


class TestCalculator:
    
    @pytest.fixture
    def calculator(self):
        return Calculator()
    
    # Testes de Soma

    def teste_exemplo(self):
        calculadora = Calculator()
        resultado = calculadora.soma(2, 3)
        assert resultado == 5

    def test_soma_positivos(self, calculator):
        resultado = calculator.soma(5, 3)
        assert resultado == 8
    
    def test_soma_negativos(self, calculator):
        resultado = calculator.soma(-5, -3)
        assert resultado == -8
    
    def test_soma_misto(self, calculator):
        resultado = calculator.soma(10, -4)
        assert resultado == 6
    
    # Testes de Subtração
    def test_subtrai_positivos(self, calculator):
        resultado = calculator.subtrai(10, 3)
        assert resultado == 7
    
    def test_subtrai_negativo(self, calculator):
        resultado = calculator.subtrai(-5, -3)
        assert resultado == -2
    
    # Testes de Multiplicação
    def test_multiplica_positivos(self, calculator):
        resultado = calculator.multiplica(5, 3)
        assert resultado == 15
    
    def test_multiplica_negativo(self, calculator):
        resultado = calculator.multiplica(-5, 3)
        assert resultado == -15
    
    def test_multiplica_zero(self, calculator):
        resultado = calculator.multiplica(5, 0)
        assert resultado == 0
    
    # Testes de Divisão
    def test_divide_positivos(self, calculator):
        resultado = calculator.divide(10, 2)
        assert resultado == 5
    
    def test_divide_resultado_decimal(self, calculator):
        resultado = calculator.divide(10, 3)
        assert resultado == pytest.approx(3.333, rel=1e-3)
    
    def test_divide_negativo(self, calculator):
        resultado = calculator.divide(-10, 2)
        assert resultado == -5
    
    def test_divide_por_zero_raises_error(self, calculator):
        with pytest.raises(ValueError, match="Se você dividir por zero, o Sonned vai chorar"):
            calculator.divide(10, 0)
    
    # Testes de Média Ponderada
    def test_media_ponderada_simples(self, calculator):
        """Testa média ponderada com valores simples."""
        valores = [1, 2, 3]
        pesos = [1, 1, 1]
        resultado = calculator.calcular_media_ponderada(valores, pesos)
        assert resultado == pytest.approx(2.0)
    
    def test_media_ponderada_pesos_diferentes(self, calculator):
        """Testa média ponderada com pesos diferentes."""
        valores = [10, 20, 30]
        pesos = [1, 2, 3]
        # (10*1 + 20*2 + 30*3) / (1+2+3) = 140 / 6 = 23.33...
        resultado = calculator.calcular_media_ponderada(valores, pesos)
        assert resultado == pytest.approx(23.333, rel=1e-3)
    
    def test_media_ponderada_tamanhos_diferentes_raises_error(self, calculator):
        """Testa que erro é lançado quando listas têm tamanhos diferentes."""
        with pytest.raises(ValueError, match="Valores e pesos devem ter o mesmo tamanho"):
            calculator.calcular_media_ponderada([1, 2, 3], [1, 2])
    
    def test_media_ponderada_vazia_raises_error(self, calculator):
        """Testa que erro é lançado quando listas estão vazias."""
        with pytest.raises(ValueError, match="Listas não podem estar vazias"):
            calculator.calcular_media_ponderada([], [])
    
    # Testes de Desconto
    def test_desconto_25_porcento(self, calculator):
        """Testa desconto de 25% em valor de 100."""
        resultado = calculator.calcular_desconto(100, 25)
        assert resultado == 75
    
    def test_desconto_zero(self, calculator):
        """Testa que desconto de 0% não altera o valor."""
        resultado = calculator.calcular_desconto(100, 0)
        assert resultado == 100
    
    def test_desconto_100_porcento(self, calculator):
        """Testa desconto de 100% resulta em zero."""
        resultado = calculator.calcular_desconto(100, 100)
        assert resultado == 0
    
    def test_desconto_percentual_invalido_raises_error(self, calculator):
        """Testa que erro é lançado com percentual inválido."""
        with pytest.raises(ValueError, match="Percentual de desconto deve estar entre 0 e 100"):
            calculator.calcular_desconto(100, 150)


# ========================================================================
# TESTES COM MOCK - Para ensino de mocking
# ========================================================================
# Aqui mostramos como mockar as operações básicas (soma, divisão, etc)
# para testar as operações complexas isoladamente!
# ========================================================================

class TestCalculatorComMock:
    """Exemplos de testes usando Mock para ensinar esse conceito."""
    
    @pytest.fixture
    def calculator(self):
        return Calculator()
    
    def test_media_ponderada_mockando_soma(self, calculator):
        """
        EXEMPLO 1: Mockando a função soma ao testar calcular_media_ponderada.
        
        Vantagens:
        - Testa apenas a lógica da média ponderada
        - Não depende se soma está funcionando
        - Garante que soma foi chamada corretamente
        """
        with patch.object(calculator, 'soma', wraps=calculator.soma) as mock_soma:
            resultado = calculator.calcular_media_ponderada([10, 20], [1, 1])
            
            # Verifica que o resultado está correto
            assert resultado == 15.0
            
            # Verifica que soma foi chamada (internamente na média ponderada)
            assert mock_soma.called
            
            # Pode até contar quantas vezes foi chamada!
            print(f"\nSoma foi chamada {mock_soma.call_count} vezes")
    
    def test_media_ponderada_com_mock_divide(self, calculator):
        """
        EXEMPLO 2: Mockando a função divide para testar calcular_media_ponderada.
        
        Se o mock retornar um valor específico, a média ponderada retornará aquele valor.
        """
        with patch.object(calculator, 'divide', return_value=99.0) as mock_divide:
            resultado = calculator.calcular_media_ponderada([10, 20], [1, 1])
            
            # Mesmo que os valores fossem calculados corretamente,
            # como dividimos por um valor mockado, o resultado é o mockado
            assert resultado == 99.0
            
            # Podemos verificar que divide foi chamado com certos argumentos
            assert mock_divide.called
    
    def test_desconto_mockando_multiplicacao(self, calculator):
        """
        EXEMPLO 3: Mockando a função multiplica ao testar calcular_desconto.
        
        Isso isola a lógica de desconto das operações matemáticas básicas.
        """
        with patch.object(calculator, 'multiplica', return_value=25.0) as mock_mult:
            with patch.object(calculator, 'subtrai', return_value=75.0) as mock_sub:
                resultado = calculator.calcular_desconto(100, 25)
                
                # Resultado é o do mock
                assert resultado == 75.0
                
                # Verifica que as funções foram chamadas
                assert mock_mult.called
                assert mock_sub.called
                print(f"\nMultiplica foi chamada com: {mock_mult.call_args}")
                print(f"Subtrai foi chamada com: {mock_sub.call_args}")
    
    def test_media_ponderada_mock_side_effect(self, calculator):
        """
        EXEMPLO 4: Usando side_effect para retornar valores diferentes a cada chamada.
        
        Útil quando a função é chamada múltiplas vezes com comportamentos diferentes.
        """
        # Simula que soma retorna valores específicos a cada chamada
        with patch.object(calculator, 'soma', side_effect=[10.0, 20.0, 30.0, 2.0]) as mock_soma:
            with patch.object(calculator, 'divide', return_value=15.0):
                resultado = calculator.calcular_media_ponderada([5], [1])
                
                # O resultado final é o valor do divide mockado
                assert resultado == 15.0
                
                # Verificar que soma foi chamada múltiplas vezes
                assert mock_soma.call_count > 0
    
    def test_dividir_isolado_com_mock(self):
        """
        EXEMPLO 5: Criando um mock completo ao invés de usar a classe real.
        
        Útil quando você quer isolar completamente uma função.
        """
        # Cria um mock da calculadora
        mock_calculator = Mock()
        mock_calculator.divide.return_value = 5.0
        
        # Testa como se fosse a calculadora real
        resultado = mock_calculator.divide(10, 2)
        assert resultado == 5.0
        
        # Verifica como foi chamada
        mock_calculator.divide.assert_called_once_with(10, 2)
    
    def test_erro_propagado_com_mock(self, calculator):
        """
        EXEMPLO 6: Mockando para simular erros!
        
        Você pode forçar um erro sem precisar de dados reais que causem erro.
        """
        with patch.object(calculator, 'divide', side_effect=ValueError("Erro simulado!")) as mock_divide:
            with pytest.raises(ValueError, match="Erro simulado!"):
                calculator.calcular_media_ponderada([10, 20], [1, 1])
            
            # Verifica que divide foi tentada
            assert mock_divide.called


# ========================================================================
# 📚 RESUMO: UTILIDADES PRÁTICAS DO MOCK NESTE PROJETO
# ========================================================================
"""
O MOCK é uma ferramenta poderosa para testes. Aqui estão as UTILIDADES PRÁTICAS:

1. **ISOLAR DEPENDÊNCIAS - Não depender de funções externas**
   └─ Problema: Se soma() está quebrada, o teste de media_ponderada() também falha
   └─ Solução: Mock soma() para testar media_ponderada() isoladamente
   └─ Exemplo: test_media_ponderada_mockando_soma()
   └─ Benefício: Cada teste testa apenas SUA lógica, não a dos outros

---

2. **SIMULAR ERROS/CENÁRIOS RUINS - Sem precisar de dados reais que causem erro**
   └─ Problema: Como testar o que acontece quando divide(10, 0)?
                Precisamos de um erro real, mas é difícil de configurar
   └─ Solução: Mock divide() para simular qualquer erro você quer
   └─ Exemplo: test_erro_propagado_com_mock() - força um ValueError
   └─ Benefício: Testa tratamento de erros de forma controlada

---

3. **NÃO USAR O BANCO DE DADOS - Testes sem BD ficam muito mais rápidos**
   └─ Problema: Se cada teste acessa o BD, os testes ficam LENTOS
   └─ Solução: Mock a classe do repositório para não acessar BD
   └─ Exemplo (você pode adicionar): Mockar OperationRepository.criar_operacao()
   └─ Benefício: Testes rodam em milissegundos ao invés de segundos
   
   Código de exemplo:
   with patch('app.repositories.OperationRepository.criar_operacao') as mock_repo:
       mock_repo.return_value = Operation(id=1, resultado=100)
       # Testa sem tocar no BD real

---

4. **NÃO FAZER REQUISIÇÕES HTTP - Sem depender de API externa**
   └─ Problema: Você testa uma função que chama uma API externa?
                Se a API cair, TODOS seus testes falham
   └─ Solução: Mock o requests.get() para retornar dados fake
   └─ Benefício: Testes rodam offline, rápido e confiável
   
   Código de exemplo:
   with patch('requests.get') as mock_get:
       mock_get.return_value.json.return_value = {"resultado": 100}
       # Testa sem chamar a API real

---

5. **NÃO LER/ESCREVER ARQUIVOS - Evita ter arquivos temporários**
   └─ Problema: Você salva dados em arquivo? Criar/deletar arquivos é lento
   └─ Solução: Mock arquivo() para não escrever de verdade
   └─ Benefício: Testes não deixam arquivos lixo no disco
   
   Código de exemplo:
   with patch('builtins.open', mock_open(read_data="dados")) as mock_file:
       # Lê dados fake sem arquivo real
       data = open('dados.txt').read()

---

6. **VALIDAR QUE ALGO FOI CHAMADO - Verificar se código chamou o que deveria**
   └─ Problema: Como saber se a função A realmente chamou a função B?
   └─ Solução: Mock B e valide que foi chamada
   └─ Exemplo: mock_soma.assert_called_with(10, 20)
   └─ Benefício: Garante que a lógica está funcionando como esperado

---

7. **TESTAR COMPORTAMENTOS MÚLTIPLOS - Simular vários cenários**
   └─ Problema: Uma função é chamada 3 vezes com valor diferentes
   └─ Solução: side_effect=[valor1, valor2, valor3]
   └─ Exemplo: test_media_ponderada_mock_side_effect()
   └─ Benefício: Testa comportamento complexo com múltiplas chamadas

---

RESUMO DAS TÉCNICAS USADAS NO PROJETO:

• patch.object(obj, 'metodo', wraps=obj.metodo)
  └─ Mantém função real mas rastreia chamadas

• patch.object(obj, 'metodo', return_value=X)
  └─ Substitui retorno por valor fake

• Mock()
  └─ Cria função/objeto completamente fake

• side_effect=[val1, val2, ...]
  └─ Retorna valores diferentes a cada chamada

• side_effect=ValueError(...)
  └─ Força lançar exceção

"""
