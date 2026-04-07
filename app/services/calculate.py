class Calculator:
    
    def __init__(self):
        # Inicializa a calculadora
        pass
    
    def soma(self, a: float, b: float) -> float:
        # Soma dois números
        return a + b
    
    def subtrai(self, a: float, b: float) -> float:
        # Subtrai dois números
        return a - b
    
    def multiplica(self, a: float, b: float) -> float:
        # Multiplica dois números
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        # Divide dois números
        if b == 0:
            raise ValueError("Se você dividir por zero, o Sonned vai chorar")
        return a / b
    
    def calcular_media_ponderada(self, valores: list[float], pesos: list[float]) -> float:
        # Calcula a média ponderada de uma lista de valores com seus respectivos pesos.
        # Internamente usa soma e divisão - PERFEITO PARA ENSINAR MOCK!
        #
        # Args:
        #     valores: Lista de valores
        #     pesos: Lista de pesos correspondentes
        #
        # Returns:
        #     A média ponderada
        #
        # Raises:
        #     ValueError: Se as listas tiverem tamanhos diferentes ou soma dos pesos for zero
        
        if len(valores) != len(pesos):
            raise ValueError("Valores e pesos devem ter o mesmo tamanho")
        
        if len(valores) == 0:
            raise ValueError("Listas não podem estar vazias")
        
        # Calcula numerador (soma dos valores * pesos)
        numerador = 0.0
        for valor, peso in zip(valores, pesos):
            numerador = self.soma(numerador, self.multiplica(valor, peso))
        
        # Calcula denominador (soma dos pesos)
        denominador = 0.0
        for peso in pesos:
            denominador = self.soma(denominador, peso)
        
        # Divide para obter a média
        return self.divide(numerador, denominador)

    def calcular_desconto(self, valor_original: float, percentual_desconto: float) -> float:
        # Calcula o valor final após aplicar um desconto percentual.
        # Usa subtração e multiplicação internamente.
        #
        # Args:
        #     valor_original: Valor antes do desconto
        #     percentual_desconto: Percentual de desconto (0-100)
        #
        # Returns:
        #     Valor final após o desconto
        
        if percentual_desconto < 0 or percentual_desconto > 100:
            raise ValueError("Percentual de desconto deve estar entre 0 e 100")
        
        valor_desconto = self.multiplica(valor_original, self.divide(percentual_desconto, 100))
        return self.subtrai(valor_original, valor_desconto)