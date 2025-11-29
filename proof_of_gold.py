from decimal import Decimal
import time

class ProofOfGold:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.gold_price_cache = {}
        self.cache_duration = 300  # 5 minutos
    
    def calculate_mining_difficulty(self, gold_price: Decimal) -> int:
        """
        Ajusta la dificultad de minería basado en el precio del oro
        Precio más alto = Mayor seguridad = Mayor dificultad
        """
        base_difficulty = 4
        price_factor = gold_price / Decimal('1000.0')
        return max(base_difficulty, int(base_difficulty * price_factor))
    
    def get_gold_backing_ratio(self) -> Decimal:
        """Calcula el ratio de respaldo en oro"""
        circulating_supply = self.blockchain.get_circulating_supply()
        if circulating_supply == 0:
            return Decimal('1.0')
        
        gold_value = self.blockchain.gold_backing_reserve * self.get_current_gold_price()
        vivcoin_value = circulating_supply * self.blockchain.get_current_vivcoin_price()
        
        return gold_value / vivcoin_value if vivcoin_value > 0 else Decimal('0.0')
    
    def validate_gold_backing(self) -> bool:
        """Valida que el respaldo en oro sea suficiente"""
        ratio = self.get_gold_backing_ratio()
        return ratio >= Decimal('0.8')  # Mínimo 80% respaldado
    
    def get_current_gold_price(self) -> Decimal:
        """Obtiene precio actual del oro desde múltiples fuentes"""
        current_time = time.time()
        
        # Verificar cache
        if (self.gold_price_cache.get('timestamp', 0) + self.cache_duration) > current_time:
            return Decimal(str(self.gold_price_cache['price']))
        
        # Obtener precio de múltiples oráculos (implementación simplificada)
        prices = [
            self._get_gold_price_from_api1(),
            self._get_gold_price_from_api2(),
            self._get_gold_price_from_api3()
        ]
        
        # Usar mediana para evitar outliers
        prices.sort()
        median_price = Decimal(str(prices[len(prices)//2]))
        
        # Actualizar cache
        self.gold_price_cache = {
            'price': float(median_price),
            'timestamp': current_time
        }
        
        return median_price
    
    def _get_gold_price_from_api1(self) -> float:
        # Implementar conexión a API real
        return 1800.0
    
    def _get_gold_price_from_api2(self) -> float:
        return 1795.5
    
    def _get_gold_price_from_api3(self) -> float:
        return 1802.3