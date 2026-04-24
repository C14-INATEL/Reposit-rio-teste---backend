"""Testes para a classe Calculator."""

import pytest
from unittest.mock import Mock, patch
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
        valores = [1, 2, 3]
        pesos = [1, 1, 1]
        resultado = calculator.calcular_media_ponderada(valores, pesos)
        assert resultado == pytest.approx(2.0)

    def test_media_ponderada_pesos_diferentes(self, calculator):
        valores = [10, 20, 30]
        pesos = [1, 2, 3]
        resultado = calculator.calcular_media_ponderada(valores, pesos)
        assert resultado == pytest.approx(23.333, rel=1e-3)

    def test_media_ponderada_tamanhos_diferentes_raises_error(self, calculator):
        with pytest.raises(ValueError, match="Valores e pesos devem ter o mesmo tamanho"):
            calculator.calcular_media_ponderada([1, 2, 3], [1, 2])

    def test_media_ponderada_vazia_raises_error(self, calculator):
        with pytest.raises(ValueError, match="Listas não podem estar vazias"):
            calculator.calcular_media_ponderada([], [])

    # Testes de Desconto
    def test_desconto_25_porcento(self, calculator):
        resultado = calculator.calcular_desconto(100, 25)
        assert resultado == 75

    def test_desconto_zero(self, calculator):
        resultado = calculator.calcular_desconto(100, 0)
        assert resultado == 100

    def test_desconto_100_porcento(self, calculator):
        resultado = calculator.calcular_desconto(100, 100)
        assert resultado == 0

    def test_desconto_percentual_invalido_raises_error(self, calculator):
        with pytest.raises(ValueError, match="Percentual de desconto deve estar entre 0 e 100"):
            calculator.calcular_desconto(100, 150)


# ========================================================================
# TESTES COM MOCK
# ========================================================================

class TestCalculatorComMock:

    @pytest.fixture
    def calculator(self):
        return Calculator()

    def test_media_ponderada_mockando_soma(self, calculator):
        with patch.object(calculator, 'soma', wraps=calculator.soma) as mock_soma:
            resultado = calculator.calcular_media_ponderada([10, 20], [1, 1])

            assert resultado == 15.0
            assert mock_soma.called

    def test_media_ponderada_com_mock_divide(self, calculator):
        with patch.object(calculator, 'divide', return_value=99.0) as mock_divide:
            resultado = calculator.calcular_media_ponderada([10, 20], [1, 1])

            assert resultado == 99.0
            assert mock_divide.called

    def test_desconto_mockando_multiplicacao(self, calculator):
        with patch.object(calculator, 'multiplica', return_value=25.0) as mock_mult:
            with patch.object(calculator, 'subtrai', return_value=75.0) as mock_sub:
                resultado = calculator.calcular_desconto(100, 25)

                assert resultado == 75.0
                assert mock_mult.called
                assert mock_sub.called

    def test_media_ponderada_mock_side_effect(self, calculator):
        with patch.object(calculator, 'soma', side_effect=[10.0, 20.0, 30.0, 2.0]) as mock_soma:
            with patch.object(calculator, 'divide', return_value=15.0):
                resultado = calculator.calcular_media_ponderada([5], [1])

                assert resultado == 15.0
                assert mock_soma.call_count > 0

    def test_dividir_isolado_com_mock(self):
        mock_calculator = Mock()
        mock_calculator.divide.return_value = 5.0

        resultado = mock_calculator.divide(10, 2)
        assert resultado == 5.0

        mock_calculator.divide.assert_called_once_with(10, 2)

    def test_erro_propagado_com_mock(self, calculator):
        with patch.object(calculator, 'divide', side_effect=ValueError("Erro simulado!")) as mock_divide:
            with pytest.raises(ValueError, match="Erro simulado!"):
                calculator.calcular_media_ponderada([10, 20], [1, 1])

            assert mock_divide.called

    def test_media_ponderada_mock_verificacao_incorreta(self, calculator):
         with patch.object(calculator, 'divide', return_value=10.0) as mock_divide:
             calculator.calcular_media_ponderada([10, 20], [1, 1])

         with pytest.raises(AssertionError):
             mock_divide.assert_called_with(999, 999)

    def test_desconto_mock_valor_errado(self, calculator):
          with patch.object(calculator, 'multiplica', return_value=50.0):
             with patch.object(calculator, 'subtrai', return_value=50.0):
                resultado = calculator.calcular_desconto(100, 50)

             with pytest.raises(AssertionError):
                assert resultado == 25.0