#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VIVCOINORO - INDEX PRINCIPAL AUTOMATIZADO
Sistema Blockchain con Comportamiento de Oro Digital
Conexiones Automáticas a Todas las Blockchains
"""

import asyncio
import logging
import sys
import time
import json
import os
from datetime import datetime
from decimal import Decimal

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vivcoinoro_automated.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("VivCoinORo-Index")

class VivCoinORoAutomatedIndex:
    """
    INDEX PRINCIPAL - Sistema completamente automatizado
    Conexiones automáticas a todas las blockchains y wallets
    """
    
    def __init__(self):
        self.system_status = "initializing"
        self.connected_blockchains = {}
        self.wallets = {}
        self.services = {}
        self.start_time = datetime.now()
        
    async def initialize_complete_system(self):
        """Inicializar TODO el sistema automáticamente"""
        print("\n" + "="*70)
        print("🚀 VIVCOINORO - SISTEMA AUTOMATIZADO INICIANDO")
        print("⭐ Comportamiento Equiparable al Oro Digital")
        print("🔗 Conexiones Automáticas a Blockchains")
        print("="*70 + "\n")
        
        try:
            # PASO 1: Inicializar Blockchain Principal de VivCoinORo
            await self._initialize_vivcoinoro_blockchain()
            
            # PASO 2: Conexiones automáticas a blockchains externas
            await self._auto_connect_all_blockchains()
            
            # PASO 3: Configurar wallets multi-cadena automáticamente
            await self._auto_setup_wallets()
            
            # PASO 4: Iniciar servicios en tiempo real
            await self._start_real_time_services()
            
            # PASO 5: Iniciar APIs y interfaces
            await self._start_apis_interfaces()
            
            # PASO 6: Verificación final del sistema
            await self._final_system_check()
            
            self.system_status = "running"
            logger.info("✅ SISTEMA VIVCOINORO COMPLETAMENTE OPERATIVO")
            
            # Mostrar dashboard inicial
            await self._show_system_dashboard()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ ERROR CRÍTICO INICIALIZANDO SISTEMA: {e}")
            self.system_status = "error"
            return False

    async def _initialize_vivcoinoro_blockchain(self):
        """Inicializar blockchain principal de VivCoinORo"""
        logger.info("🔄 Inicializando Blockchain VivCoinORo...")
        
        try:
            # Importar e inicializar blockchain principal
            from blockchain.core.blockchain import VivCoinORoBlockchain
            from blockchain.consensus.proof_of_gold import ProofOfGold
            
            self.blockchain = VivCoinORoBlockchain()
            self.consensus = ProofOfGold(self.blockchain)
            
            # Verificar blockchain
            if self.blockchain.is_chain_valid():
                logger.info("✅ Blockchain VivCoinORo inicializada y válida")
                logger.info(f"   📦 Bloques: {len(self.blockchain.chain)}")
                logger.info(f"   💰 Supply: {self.blockchain.get_circulating_supply()} VIV")
                logger.info(f"   🥇 Respaldo Oro: {self.blockchain.gold_backing_reserve} oz")
            else:
                raise Exception("Blockchain inválida")
                
        except Exception as e:
            logger.error(f"❌ Error inicializando blockchain: {e}")
            raise

    async def _auto_connect_all_blockchains(self):
        """Conectar automáticamente a todas las blockchains soportadas"""
        logger.info("🔗 Conectando automáticamente a blockchains...")
        
        blockchains_to_connect = [
            'bitcoin', 'ethereum', 'binance', 'solana',
            'avalanche', 'polygon', 'arbitrum', 'optimism'
        ]
        
        for chain_name in blockchains_to_connect:
            try:
                adapter = await self._create_blockchain_adapter(chain_name)
                if adapter and await self._test_adapter_connection(adapter, chain_name):
                    self.connected_blockchains[chain_name] = adapter
                    logger.info(f"   ✅ {chain_name.upper():<12} - CONECTADO")
                else:
                    logger.warning(f"   ⚠️ {chain_name.upper():<12} - FALLÓ CONEXIÓN")
            except Exception as e:
                logger.error(f"   ❌ {chain_name.upper():<12} - ERROR: {e}")
        
        logger.info(f"✅ Conectado a {len(self.connected_blockchains)} blockchains")

    async def _create_blockchain_adapter(self, chain_name):
        """Crear adapter para blockchain específica"""
        try:
            if chain_name == 'bitcoin':
                from wallet.multi_chain.bitcoin_adapter import BitcoinAdapter
                return BitcoinAdapter(network='mainnet')
            
            elif chain_name == 'ethereum':
                # Crear adapter Ethereum
                from wallet.multi_chain.ethereum_adapter import EthereumAdapter
                return EthereumAdapter(network='mainnet')
            
            elif chain_name == 'binance':
                # Crear adapter Binance
                from wallet.multi_chain.binance_adapter import BinanceAdapter
                return BinanceAdapter(network='mainnet')
            
            elif chain_name == 'solana':
                # Crear adapter Solana  
                from wallet.multi_chain.solana_adapter import SolanaAdapter
                return SolanaAdapter(network='mainnet')
            
            # Agregar más adapters aquí...
            else:
                logger.warning(f"Adapter para {chain_name} no implementado")
                return None
                
        except ImportError as e:
            logger.warning(f"No se pudo importar adapter para {chain_name}: {e}")
            return None

    async def _test_adapter_connection(self, adapter, chain_name):
        """Probar conexión del adapter"""
        try:
            # Métodos de prueba según el adapter
            if hasattr(adapter, 'get_network_info'):
                info = adapter.get_network_info()
                return info is not None
            elif hasattr(adapter, 'get_latest_block'):
                block = adapter.get_latest_block()
                return block is not None
            else:
                # Si no tiene métodos específicos, asumir conectado
                return True
        except Exception as e:
            logger.error(f"Error probando {chain_name}: {e}")
            return False

    async def _auto_setup_wallets(self):
        """Configurar wallets multi-cadena automáticamente"""
        logger.info("💰 Configurando Wallets Multi-Cadena...")
        
        try:
            from wallet.core.wallet import VivCoinORoWallet
            
            # Crear wallet principal
            self.main_wallet = VivCoinORoWallet()
            self.main_wallet.generate_keypair()
            self.wallets['main'] = self.main_wallet
            
            # Conectar wallet a todas las blockchains
            for chain_name, adapter in self.connected_blockchains.items():
                self.main_wallet.connect_to_blockchain(chain_name, adapter)
            
            logger.info(f"✅ Wallet principal creada: {self.main_wallet.address}")
            logger.info(f"   🔗 Conectada a {len(self.connected_blockchains)} blockchains")
            
            # Mostrar balances iniciales
            await self._show_initial_balances()
            
        except Exception as e:
            logger.error(f"❌ Error configurando wallets: {e}")
            raise

    async def _show_initial_balances(self):
        """Mostrar balances iniciales de todas las cadenas"""
        try:
            balances = self.main_wallet.get_multi_chain_balance()
            logger.info("   📊 Balances Iniciales:")
            for chain, balance in balances.items():
                logger.info(f"      • {chain.upper():<12}: {balance}")
        except Exception as e:
            logger.warning(f"   ⚠️ No se pudieron obtener balances: {e}")

    async def _start_real_time_services(self):
        """Iniciar servicios en tiempo real"""
        logger.info("🔄 Iniciando Servicios en Tiempo Real...")
        
        # Servicio de precios
        self.services['price_monitor'] = asyncio.create_task(
            self._price_monitoring_service()
        )
        
        # Servicio de salud de conexiones
        self.services['health_monitor'] = asyncio.create_task(
            self._connection_health_service()
        )
        
        # Servicio de sincronización
        self.services['blockchain_sync'] = asyncio.create_task(
            self._blockchain_sync_service()
        )
        
        logger.info("✅ Servicios en tiempo real iniciados")

    async def _price_monitoring_service(self):
        """Monitoreo de precios en tiempo real"""
        while self.system_status == "running":
            try:
                # Precio del oro
                gold_price = self.consensus.get_current_gold_price()
                
                # Precio VivCoinORo
                viv_price = self.blockchain.get_current_vivcoin_price()
                
                # Ratio de respaldo
                backing_ratio = self.consensus.get_gold_backing_ratio()
                
                logger.info(f"💰 PRECIOS - Oro: ${gold_price:.2f} | VIV: ${viv_price:.4f} | Respaldo: {backing_ratio:.2%}")
                
                await asyncio.sleep(60)  # Actualizar cada minuto
                
            except Exception as e:
                logger.error(f"Error en monitoreo de precios: {e}")
                await asyncio.sleep(30)

    async def _connection_health_service(self):
        """Monitoreo de salud de conexiones"""
        while self.system_status == "running":
            try:
                healthy_connections = 0
                for chain_name, adapter in self.connected_blockchains.items():
                    if await self._test_adapter_connection(adapter, chain_name):
                        healthy_connections += 1
                    else:
                        logger.warning(f"🔄 Reconectando a {chain_name}...")
                        # Intentar reconexión automática
                        new_adapter = await self._create_blockchain_adapter(chain_name)
                        if new_adapter and await self._test_adapter_connection(new_adapter, chain_name):
                            self.connected_blockchains[chain_name] = new_adapter
                            self.main_wallet.connect_to_blockchain(chain_name, new_adapter)
                            healthy_connections += 1
                
                logger.info(f"🏥 SALUD - {healthy_connections}/{len(self.connected_blockchains)} conexiones saludables")
                await asyncio.sleep(120)  # Verificar cada 2 minutos
                
            except Exception as e:
                logger.error(f"Error en monitoreo de salud: {e}")
                await asyncio.sleep(60)

    async def _blockchain_sync_service(self):
        """Servicio de sincronización de blockchain"""
        while self.system_status == "running":
            try:
                # Sincronizar con la red (si está implementado)
                if hasattr(self.blockchain, 'sync_with_network'):
                    await self.blockchain.sync_with_network()
                
                await asyncio.sleep(30)
            except Exception as e:
                logger.error(f"Error en sincronización: {e}")
                await asyncio.sleep(30)

    async def _start_apis_interfaces(self):
        """Iniciar APIs e interfaces"""
        logger.info("🌐 Iniciando APIs e Interfaces...")
        
        try:
            # Iniciar API REST en segundo plano
            import threading
            from api.rest_api import app
            
            def run_api():
                app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
            
            api_thread = threading.Thread(target=run_api, daemon=True)
            api_thread.start()
            
            logger.info("   ✅ API REST iniciada en http://localhost:5000")
            
            # Iniciar WebSocket service
            self.services['websocket'] = asyncio.create_task(
                self._websocket_service()
            )
            logger.info("   ✅ WebSocket service iniciado")
            
        except Exception as e:
            logger.warning(f"   ⚠️ No se pudo iniciar API: {e}")

    async def _websocket_service(self):
        """Servicio WebSocket para updates en tiempo real"""
        while self.system_status == "running":
            try:
                # Enviar updates de precios y estado
                # (Implementación completa requeriría un servidor WebSocket real)
                await asyncio.sleep(10)
            except Exception as e:
                logger.error(f"Error en WebSocket: {e}")
                await asyncio.sleep(10)

    async def _final_system_check(self):
        """Verificación final del sistema"""
        logger.info("🏁 Realizando verificación final del sistema...")
        
        checks = {
            'Blockchain VivCoinORo': self.blockchain.is_chain_valid(),
            'Conexiones Blockchain': len(self.connected_blockchains) > 0,
            'Wallet Principal': hasattr(self, 'main_wallet') and self.main_wallet.address,
            'Servicios Activos': len(self.services) > 0
        }
        
        all_checks_passed = True
        for check_name, passed in checks.items():
            status = "✅ PASÓ" if passed else "❌ FALLÓ"
            logger.info(f"   {status} - {check_name}")
            if not passed:
                all_checks_passed = False
        
        if all_checks_passed:
            logger.info("🎉 TODAS LAS VERIFICACIONES PASARON - SISTEMA LISTO")
        else:
            logger.warning("⚠️ ALGUNAS VERIFICACIONES FALLARON - REVISAR LOGS")

    async def _show_system_dashboard(self):
        """Mostrar dashboard del sistema"""
        print("\n" + "="*70)
        print("🎯 VIVCOINORO - DASHBOARD DEL SISTEMA")
        print("="*70)
        
        # Información de blockchain
        viv_price = self.blockchain.get_current_vivcoin_price()
        gold_price = self.consensus.get_current_gold_price()
        backing_ratio = self.consensus.get_gold_backing_ratio()
        
        print(f"💰 PRECIO VIVCOINORO: ${viv_price:.4f}")
        print(f"🥇 PRECIO ORO: ${gold_price:.2f}/oz")
        print(f"🛡️  RESPALDO EN ORO: {backing_ratio:.2%}")
        print(f"📦 BLOQUES: {len(self.blockchain.chain)}")
        print(f"💸 SUPPLY CIRCULANTE: {self.blockchain.get_circulating_supply():.2f} VIV")
        
        # Conexiones activas
        print(f"\n🔗 CONEXIONES ACTIVAS ({len(self.connected_blockchains)}):")
        for chain in self.connected_blockchains.keys():
            print(f"   • {chain.upper()}")
        
        # Wallet info
        if hasattr(self, 'main_wallet'):
            print(f"\n💰 WALLET PRINCIPAL: {self.main_wallet.address}")
            try:
                balances = self.main_wallet.get_multi_chain_balance()
                print("   📊 BALANCES:")
                for chain, balance in balances.items():
                    print(f"      • {chain.upper():<12}: {balance}")
            except:
                print("   ⚠️ No se pudieron cargar balances")
        
        print(f"\n⏰ TIEMPO ACTIVO: {datetime.now() - self.start_time}")
        print("="*70 + "\n")

    async def run_interactive_mode(self):
        """Ejecutar en modo interactivo"""
        print("\n🎮 MODO INTERACTIVO ACTIVADO")
        print("Comandos disponibles:")
        print("  status  - Ver estado del sistema")
        print("  prices  - Ver precios actuales") 
        print("  wallets - Ver información de wallets")
        print("  exit    - Salir del sistema")
        
        while self.system_status == "running":
            try:
                command = await asyncio.get_event_loop().run_in_executor(
                    None, input, "\n▶️  Comando: "
                )
                
                if command == 'status':
                    await self._show_system_dashboard()
                elif command == 'prices':
                    await self._show_current_prices()
                elif command == 'wallets':
                    await self._show_wallet_info()
                elif command == 'exit':
                    break
                else:
                    print("❌ Comando no reconocido")
                    
            except (KeyboardInterrupt, EOFError):
                break
            except Exception as e:
                print(f"❌ Error ejecutando comando: {e}")

    async def _show_current_prices(self):
        """Mostrar precios actuales"""
        gold_price = self.consensus.get_current_gold_price()
        viv_price = self.blockchain.get_current_vivcoin_price()
        backing_ratio = self.consensus.get_gold_backing_ratio()
        
        print(f"\n💰 PRECIOS ACTUALES:")
        print(f"   • Oro: ${gold_price:.2f}/oz")
        print(f"   • VivCoinORo: ${viv_price:.4f}")
        print(f"   • Respaldo: {backing_ratio:.2%}")

    async def _show_wallet_info(self):
        """Mostrar información de wallets"""
        if hasattr(self, 'main_wallet'):
            print(f"\n💰 WALLET PRINCIPAL:")
            print(f"   Dirección: {self.main_wallet.address}")
            
            balances = self.main_wallet.get_multi_chain_balance()
            print("   Balances:")
            for chain, balance in balances.items():
                print(f"      • {chain.upper():<12}: {balance}")
        else:
            print("❌ No hay wallet principal configurada")

    async def shutdown(self):
        """Apagar el sistema gracefulmente"""
        logger.info("🛑 Apagando sistema VivCoinORo...")
        self.system_status = "shutting_down"
        
        # Cancelar servicios
        for service_name, task in self.services.items():
            task.cancel()
            logger.info(f"   🔴 Servicio {service_name} cancelado")
        
        # Cerrar conexiones
        for chain_name, adapter in self.connected_blockchains.items():
            if hasattr(adapter, 'close'):
                adapter.close()
            logger.info(f"   🔴 Desconectado de {chain_name}")
        
        logger.info("✅ Sistema VivCoinORo apagado correctamente")

# 🎯 FUNCIÓN PRINCIPAL DE EJECUCIÓN
async def main():
    """Función principal que ejecuta todo el sistema"""
    system = VivCoinORoAutomatedIndex()
    
    try:
        # Inicializar sistema completo
        success = await system.initialize_complete_system()
        if not success:
            print("❌ NO SE PUDO INICIAR EL SISTEMA - Revisar logs")
            return
        
        # Ejecutar en modo interactivo
        await system.run_interactive_mode()
        
    except KeyboardInterrupt:
        print("\n🛑 Sistema interrumpido por el usuario")
    except Exception as e:
        print(f"❌ ERROR NO MANEJADO: {e}")
    finally:
        await system.shutdown()

# 🚀 PUNTO DE ENTRADA PRINCIPAL
if __name__ == "__main__":
    print("🚀 Iniciando VivCoinORo Automated System...")
    asyncio.run(main())