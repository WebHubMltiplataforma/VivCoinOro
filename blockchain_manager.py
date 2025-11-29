import asyncio
import logging
from typing import Dict, List, Optional
from decimal import Decimal

logger = logging.getLogger("BlockchainManager")

class BlockchainManager:
    """Gestiona conexiones automáticas a múltiples blockchains"""
    
    def __init__(self):
        self.connections = {}
        self.health_status = {}
        self.auto_reconnect = True
        
    async def auto_connect(self, chain_name: str) -> Optional[object]:
        """Conexión automática a blockchain específica"""
        try:
            logger.info(f"🔄 Conectando automáticamente a {chain_name}...")
            
            # Crear adapter específico para la blockchain
            adapter = await self._create_adapter(chain_name)
            if not adapter:
                return None
            
            # Probar conexión
            if await self._test_adapter_connection(adapter, chain_name):
                self.connections[chain_name] = adapter
                self.health_status[chain_name] = 'connected'
                logger.info(f"✅ Conexión exitosa a {chain_name}")
                return adapter
            else:
                logger.warning(f"⚠️ No se pudo conectar a {chain_name}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error en conexión automática a {chain_name}: {e}")
            return None
    
    async def _create_adapter(self, chain_name: str) -> Optional[object]:
        """Crear adapter para blockchain específica"""
        try:
            if chain_name == 'bitcoin':
                from wallet.multi_chain.bitcoin_adapter import BitcoinAdapter
                return BitcoinAdapter(network='mainnet')
            
            elif chain_name == 'ethereum':
                from wallet.multi_chain.ethereum_adapter import EthereumAdapter
                return EthereumAdapter(network='mainnet')
            
            elif chain_name == 'binance':
                from wallet.multi_chain.binance_adapter import BinanceAdapter
                return BinanceAdapter(network='mainnet')
            
            elif chain_name == 'solana':
                from wallet.multi_chain.solana_adapter import SolanaAdapter
                return SolanaAdapter(network='mainnet')
            
            elif chain_name == 'avalanche':
                from wallet.multi_chain.avalanche_adapter import AvalancheAdapter
                return AvalancheAdapter(network='mainnet')
            
            elif chain_name == 'polygon':
                from wallet.multi_chain.polygon_adapter import PolygonAdapter
                return PolygonAdapter(network='mainnet')
            
            elif chain_name == 'arbitrum':
                from wallet.multi_chain.arbitrum_adapter import ArbitrumAdapter
                return ArbitrumAdapter(network='mainnet')
            
            elif chain_name == 'optimism':
                from wallet.multi_chain.optimism_adapter import OptimismAdapter
                return OptimismAdapter(network='mainnet')
            
            else:
                logger.warning(f"⚠️ Blockchain {chain_name} no soportada")
                return None
                
        except ImportError as e:
            logger.error(f"❌ Error importando adapter para {chain_name}: {e}")
            return None
    
    async def _test_adapter_connection(self, adapter, chain_name: str) -> bool:
        """Probar conexión del adapter"""
        try:
            # Métodos comunes para probar conexión
            test_methods = [
                'get_network_info',
                'get_latest_block',
                'get_native_price'
            ]
            
            for method in test_methods:
                if hasattr(adapter, method):
                    result = getattr(adapter, method)()
                    if result:
                        return True
            
            # Si no tiene métodos específicos, considerar conectado
            return True
            
        except Exception as e:
            logger.error(f"❌ Error probando conexión a {chain_name}: {e}")
            return False
    
    async def check_health(self, chain_name: str, adapter=None) -> bool:
        """Verificar salud de conexión específica"""
        if not adapter:
            adapter = self.connections.get(chain_name)
        
        if not adapter:
            self.health_status[chain_name] = 'disconnected'
            return False
        
        try:
            # Verificar conexión
            is_healthy = await self._test_adapter_connection(adapter, chain_name)
            self.health_status[chain_name] = 'connected' if is_healthy else 'unhealthy'
            return is_healthy
            
        except Exception as e:
            logger.error(f"❌ Error en health check de {chain_name}: {e}")
            self.health_status[chain_name] = 'error'
            return False
    
    async def get_connection_status(self) -> Dict:
        """Obtener estado de todas las conexiones"""
        status = {}
        for chain_name, adapter in self.connections.items():
            is_healthy = await self.check_health(chain_name, adapter)
            status[chain_name] = {
                'connected': is_healthy,
                'status': self.health_status.get(chain_name, 'unknown'),
                'adapter': type(adapter).__name__
            }
        return status
    
    def get_connected_chains(self) -> List[str]:
        """Obtener lista de blockchains conectadas"""
        return list(self.connections.keys())