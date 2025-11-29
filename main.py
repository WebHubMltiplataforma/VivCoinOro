#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VivCoinORo - Index Principal Automatizado
Sistema Blockchain con Comportamiento de Oro Digital
Conexiones Automáticas a Blockchains y Wallets
"""

import asyncio
import logging
import signal
import sys
import time
from decimal import Decimal
from typing import Dict, List, Optional

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vivcoinoro.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("VivCoinORo")

class VivCoinORoAutomatedSystem:
    """
    Sistema Principal Automatizado de VivCoinORo
    Gestiona conexiones automáticas a blockchains y wallets
    """
    
    def __init__(self):
        self.is_running = False
        self.components = {}
        self.connected_chains = {}
        self.wallet_connections = {}
        
    async def initialize_system(self):
        """Inicializar todo el sistema automáticamente"""
        logger.info("🚀 Iniciando Sistema VivCoinORo Automatizado...")
        
        try:
            # 1. Inicializar componentes core
            await self._initialize_core_components()
            
            # 2. Conexiones automáticas a blockchains
            await self._auto_connect_blockchains()
            
            # 3. Configuración automática de wallets
            await self._auto_setup_wallets()
            
            # 4. Iniciar servicios en segundo plano
            await self._start_background_services()
            
            # 5. Verificar salud del sistema
            await self._health_check()
            
            logger.info("✅ Sistema VivCoinORo completamente inicializado y operativo")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error inicializando sistema: {e}")
            return False
    
    async def _initialize_core_components(self):
        """Inicializar componentes principales del sistema"""
        from blockchain.core.blockchain import VivCoinORoBlockchain
        from blockchain.consensus.proof_of_gold import ProofOfGold
        from auto_connect.blockchain_manager import BlockchainManager
        from auto_connect.wallet_connector import WalletConnector
        
        logger.info("🔄 Inicializando componentes core...")
        
        # Blockchain principal de VivCoinORo
        self.blockchain = VivCoinORoBlockchain()
        self.components['blockchain'] = self.blockchain
        
        # Consenso Proof-of-Gold
        self.consensus = ProofOfGold(self.blockchain)
        self.components['consensus'] = self.consensus
        
        # Gestor de conexiones blockchain
        self.blockchain_manager = BlockchainManager()
        self.components['blockchain_manager'] = self.blockchain_manager
        
        # Conector de wallets
        self.wallet_connector = WalletConnector()
        self.components['wallet_connector'] = self.wallet_connector
        
        logger.info("✅ Componentes core inicializados")
    
    async def _auto_connect_blockchains(self):
        """Conexión automática a múltiples blockchains"""
        logger.info("🔗 Conectando automáticamente a blockchains...")
        
        # Lista de blockchains para conectar automáticamente
        target_blockchains = [
            'bitcoin',
            'ethereum', 
            'binance',
            'solana',
            'avalanche',
            'polygon',
            'arbitrum',
            'optimism'
        ]
        
        for chain_name in target_blockchains:
            try:
                logger.info(f"🔄 Conectando a {chain_name}...")
                connection = await self.blockchain_manager.auto_connect(chain_name)
                
                if connection:
                    self.connected_chains[chain_name] = connection
                    logger.info(f"✅ Conectado exitosamente a {chain_name}")
                else:
                    logger.warning(f"⚠️ No se pudo conectar a {chain_name}")
                    
            except Exception as e:
                logger.error(f"❌ Error conectando a {chain_name}: {e}")
        
        logger.info(f"✅ Conexiones establecidas: {list(self.connected_chains.keys())}")
    
    async def _auto_setup_wallets(self):
        """Configuración automática de wallets multi-cadena"""
        logger.info("💰 Configurando wallets automáticamente...")
        
        try:
            # Configurar wallet principal de VivCoinORo
            from wallet.core.wallet import VivCoinORoWallet
            self.main_wallet = VivCoinORoWallet()
            self.main_wallet.generate_keypair()
            
            # Conectar wallet a todas las blockchains detectadas
            for chain_name, adapter in self.connected_chains.items():
                self.main_wallet.connect_to_blockchain(chain_name, adapter)
                logger.info(f"🔗 Wallet conectada a {chain_name}")
            
            self.wallet_connections['main'] = self.main_wallet
            logger.info(f"✅ Wallet principal configurada: {self.main_wallet.address}")
            
        except Exception as e:
            logger.error(f"❌ Error configurando wallet: {e}")
    
    async def _start_background_services(self):
        """Iniciar servicios en segundo plano"""
        logger.info("🔄 Iniciando servicios en segundo plano...")
        
        # Servicio de monitoreo de precios
        asyncio.create_task(self._price_monitoring_service())
        
        # Servicio de salud de conexiones
        asyncio.create_task(self._connection_health_service())
        
        # Servicio de sincronización de blockchain
        asyncio.create_task(self._blockchain_sync_service())
        
        logger.info("✅ Servicios en segundo plano iniciados")
    
    async def _price_monitoring_service(self):
        """Servicio de monitoreo de precios en tiempo real"""
        while self.is_running:
            try:
                # Monitorear precio del oro
                gold_price = self.consensus.get_current_gold_price()
                
                # Monitorear precios de criptomonedas conectadas
                for chain_name, connection in self.connected_chains.items():
                    if hasattr(connection, 'get_native_price'):
                        price = connection.get_native_price()
                        logger.info(f"💰 {chain_name.upper()}: ${price}")
                
                # Actualizar precio de VivCoinORo basado en oro
                viv_price = self.blockchain.get_current_vivcoin_price()
                logger.info(f"🌟 VivCoinORo: ${viv_price} (Respaldo: {self.consensus.get_gold_backing_ratio():.2%})")
                
                await asyncio.sleep(60)  # Actualizar cada minuto
                
            except Exception as e:
                logger.error(f"Error en monitoreo de precios: {e}")
                await asyncio.sleep(30)
    
    async def _connection_health_service(self):
        """Servicio de verificación de salud de conexiones"""
        while self.is_running:
            try:
                for chain_name, connection in self.connected_chains.items():
                    is_healthy = await self.blockchain_manager.check_health(chain_name, connection)
                    
                    if not is_healthy:
                        logger.warning(f"🔄 Reconectando a {chain_name}...")
                        # Reconexión automática
                        new_connection = await self.blockchain_manager.auto_connect(chain_name)
                        if new_connection:
                            self.connected_chains[chain_name] = new_connection
                            # Actualizar conexión en wallet
                            self.main_wallet.connect_to_blockchain(chain_name, new_connection)
                
                await asyncio.sleep(120)  # Verificar cada 2 minutos
                
            except Exception as e:
                logger.error(f"Error en servicio de salud: {e}")
                await asyncio.sleep(60)
    
    async def _blockchain_sync_service(self):
        """Servicio de sincronización de blockchain"""
        while self.is_running:
            try:
                # Sincronizar estado de la blockchain
                if hasattr(self.blockchain, 'sync_with_network'):
                    await self.blockchain.sync_with_network()
                
                await asyncio.sleep(30)  # Sincronizar cada 30 segundos
                
            except Exception as e:
                logger.error(f"Error en sincronización: {e}")
                await asyncio.sleep(30)
    
    async def _health_check(self):
        """Verificación completa de salud del sistema"""
        logger.info("🏥 Realizando verificación de salud del sistema...")
        
        health_status = {
            'blockchain': self.blockchain.is_chain_valid() if hasattr(self.blockchain, 'is_chain_valid') else True,
            'wallet': len(self.wallet_connections) > 0,
            'connections': len(self.connected_chains) > 0,
            'gold_price': self.consensus.get_current_gold_price() > Decimal('0'),
            'viv_price': self.blockchain.get_current_vivcoin_price() > Decimal('0')
        }
        
        for component, status in health_status.items():
            if status:
                logger.info(f"✅ {component}: HEALTHY")
            else:
                logger.warning(f"⚠️ {component}: UNHEALTHY")
        
        return all(health_status.values())
    
    async def run(self):
        """Ejecutar el sistema principal"""
        self.is_running = True
        
        # Manejar señales de terminación
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)
        
        try:
            # Inicializar sistema
            success = await self.initialize_system()
            if not success:
                logger.error("❌ No se pudo inicializar el sistema")
                return
            
            # Mantener el sistema corriendo
            logger.info("🟢 Sistema VivCoinORo ejecutándose...")
            while self.is_running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"❌ Error en ejecución principal: {e}")
        finally:
            await self.shutdown()
    
    def _shutdown(self, signum, frame):
        """Manejar señal de apagado"""
        logger.info(f"🛑 Recibida señal de apagado {signum}")
        self.is_running = False
    
    async def shutdown(self):
        """Apagar el sistema gracefulmente"""
        logger.info("🛑 Apagando sistema VivCoinORo...")
        self.is_running = False
        
        # Cerrar conexiones
        for chain_name, connection in self.connected_chains.items():
            if hasattr(connection, 'close'):
                connection.close()
            logger.info(f"🔴 Desconectado de {chain_name}")
        
        logger.info("✅ Sistema VivCoinORo apagado correctamente")

# ✅ NUEVO: Sistema de Conexiones Automáticas
class AutomatedBlockchainConnector:
    """Gestiona conexiones automáticas a blockchains"""
    
    def __init__(self):
        self.adapters = {}
        self.connection_status = {}
    
    async def discover_and_connect(self):
        """Descubrir y conectar automáticamente a blockchains disponibles"""
        logger.info("🔍 Descubriendo blockchains disponibles...")
        
        available_chains = await self._scan_available_blockchains()
        
        for chain in available_chains:
            try:
                adapter = await self._create_adapter(chain)
                if adapter and await self._test_connection(adapter):
                    self.adapters[chain] = adapter
                    self.connection_status[chain] = 'connected'
                    logger.info(f"✅ Conectado automáticamente a {chain}")
                else:
                    self.connection_status[chain] = 'failed'
            except Exception as e:
                logger.error(f"❌ Error conectando a {chain}: {e}")
                self.connection_status[chain] = 'error'
    
    async def _scan_available_blockchains(self) -> List[str]:
        """Escanear blockchains disponibles en la red"""
        # En una implementación real, esto escanearía la red
        # Por ahora retornamos una lista predefinida
        return [
            'bitcoin', 'ethereum', 'binance', 'solana',
            'avalanche', 'polygon', 'arbitrum', 'optimism'
        ]
    
    async def _create_adapter(self, chain_name: str):
        """Crear adapter para blockchain específica"""
        try:
            if chain_name == 'bitcoin':
                from wallet.multi_chain.bitcoin_adapter import BitcoinAdapter
                return BitcoinAdapter()
            elif chain_name == 'ethereum':
                from wallet.multi_chain.ethereum_adapter import EthereumAdapter
                return EthereumAdapter()
            elif chain_name == 'binance':
                from wallet.multi_chain.binance_adapter import BinanceAdapter
                return BinanceAdapter()
            elif chain_name == 'solana':
                from wallet.multi_chain.solana_adapter import SolanaAdapter
                return SolanaAdapter()
            # Agregar más adapters según sea necesario
        except ImportError as e:
            logger.warning(f"Adapter para {chain_name} no disponible: {e}")
            return None
    
    async def _test_connection(self, adapter) -> bool:
        """Probar conexión con el adapter"""
        try:
            # Intentar obtener información básica
            if hasattr(adapter, 'get_network_info'):
                info = adapter.get_network_info()
                return info is not None
            return True
        except:
            return False

# ✅ NUEVO: Función principal de ejecución
async def main():
    """Función principal de entrada al sistema"""
    print("""
    🚀 VivCoinORo - Sistema Blockchain de Oro Digital
    ⭐ Comportamiento Equiparable al Oro
    🔗 Conexiones Automáticas a Blockchains
    💰 Wallet Multi-Cadena Integrada
    🔄 Sistema P2P Completo
    """)
    
    # Crear e iniciar sistema automatizado
    system = VivCoinORoAutomatedSystem()
    await system.run()

if __name__ == "__main__":
    # Ejecutar sistema principal
    asyncio.run(main())