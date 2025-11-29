class UniversalBlockchainConnector:
    """Conexiones automáticas a todas las blockchains principales"""
    
    async def auto_connect_all(self):
        """Conectar automáticamente a todas las blockchains"""
        connections = {}
        
        blockchain_configs = {
            'bitcoin': {'network': 'mainnet', 'auto_sync': True},
            'ethereum': {'network': 'mainnet', 'web3_provider': 'auto'},
            'binance': {'network': 'mainnet', 'api_key': 'auto'},
            'solana': {'network': 'mainnet', 'rpc_url': 'auto'},
            'avalanche': {'network': 'mainnet', 'chain_id': 43114},
            'polygon': {'network': 'mainnet', 'chain_id': 137},
            'arbitrum': {'network': 'mainnet', 'chain_id': 42161},
            'optimism': {'network': 'mainnet', 'chain_id': 10},
            'fantom': {'network': 'mainnet', 'chain_id': 250},
            'cosmos': {'network': 'mainnet', 'chain_id': 'cosmoshub-4'}
        }
        
        for chain_name, config in blockchain_configs.items():
            try:
                adapter = await self._create_chain_adapter(chain_name, config)
                if await self._test_connection(adapter):
                    connections[chain_name] = adapter
                    print(f"✅ {chain_name.upper()} - Conectado")
                else:
                    print(f"⚠️ {chain_name.upper()} - Conexión fallida")
            except Exception as e:
                print(f"❌ {chain_name.upper()} - Error: {e}")
                
        return connections
    
    async def _create_chain_adapter(self, chain_name, config):
        """Crear adapter específico para cada blockchain"""
        if chain_name == 'bitcoin':
            from wallet.multi_chain.bitcoin_adapter import BitcoinAdapter
            return BitcoinAdapter(**config)
        elif chain_name == 'ethereum':
            from wallet.multi_chain.ethereum_adapter import EthereumAdapter
            return EthereumAdapter(**config)
        # ... más adapters