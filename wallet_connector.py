import asyncio
import logging
from typing import Dict, List, Optional
from decimal import Decimal

logger = logging.getLogger("WalletConnector")

class WalletConnector:
    """Gestiona conexiones automáticas de wallets"""
    
    def __init__(self):
        self.wallets = {}
        self.auto_backup = True
        
    async def auto_setup_wallet(self, blockchain_connections: Dict) -> Dict:
        """Configuración automática de wallet multi-cadena"""
        try:
            from wallet.core.wallet import VivCoinORoWallet
            
            logger.info("💰 Configurando wallet automáticamente...")
            
            # Crear wallet principal
            wallet = VivCoinORoWallet()
            wallet.generate_keypair()
            
            # Conectar a todas las blockchains disponibles
            for chain_name, adapter in blockchain_connections.items():
                wallet.connect_to_blockchain(chain_name, adapter)
                logger.info(f"🔗 Wallet conectada a {chain_name}")
            
            # Configurar backup automático
            if self.auto_backup:
                await self._setup_auto_backup(wallet)
            
            self.wallets['main'] = wallet
            logger.info(f"✅ Wallet configurada: {wallet.address}")
            
            return {
                'wallet': wallet,
                'address': wallet.address,
                'connected_chains': list(blockchain_connections.keys())
            }
            
        except Exception as e:
            logger.error(f"❌ Error configurando wallet: {e}")
            raise
    
    async def _setup_auto_backup(self, wallet):
        """Configurar backup automático de wallet"""
        try:
            # Backup de claves (en producción usar encriptación)
            backup_data = {
                'address': wallet.address,
                'public_key': wallet.public_key.serialize().hex() if wallet.public_key else None,
                'backup_timestamp': asyncio.get_event_loop().time()
            }
            
            # Guardar backup seguro
            # EN PRODUCCIÓN: Usar encriptación y almacenamiento seguro
            with open('wallet_backup.json', 'w') as f:
                import json
                json.dump(backup_data, f, indent=2)
            
            logger.info("✅ Backup automático de wallet configurado")
            
        except Exception as e:
            logger.error(f"⚠️ Error en backup automático: {e}")