import asyncio
import aiohttp
import logging
from typing import List, Dict

logger = logging.getLogger("NodeDiscovery")

class NodeDiscovery:
    """Descubrimiento automático de nodos blockchain"""
    
    def __init__(self):
        self.known_nodes = {}
        
    async def discover_bitcoin_nodes(self) -> List[str]:
        """Descubrir nodos Bitcoin automáticamente"""
        bitcoin_seeds = [
            'https://blockstream.info/api/',
            'https://mempool.space/api/',
            'https://bitcoin.canadiancontrol.net/api/',
            'https://btc.nownodes.io/'
        ]
        
        working_nodes = []
        for seed in bitcoin_seeds:
            if await self._test_node(seed, 'bitcoin'):
                working_nodes.append(seed)
        
        return working_nodes
    
    async def discover_ethereum_nodes(self) -> List[str]:
        """Descubrir nodos Ethereum automáticamente"""
        ethereum_seeds = [
            'https://mainnet.infura.io/v3/',
            'https://eth.nownodes.io/',
            'https://nodes.mewapi.io/rpc/eth',
            'https://cloudflare-eth.com/'
        ]
        
        working_nodes = []
        for seed in ethereum_seeds:
            if await self._test_node(seed, 'ethereum'):
                working_nodes.append(seed)
        
        return working_nodes
    
    async def _test_node(self, node_url: str, chain: str) -> bool:
        """Probar si un nodo está funcionando"""
        try:
            async with aiohttp.ClientSession() as session:
                if chain == 'bitcoin':
                    # Probar endpoint de Bitcoin
                    async with session.get(f"{node_url}blocks/tip/height", timeout=10) as response:
                        return response.status == 200
                elif chain == 'ethereum':
                    # Probar endpoint de Ethereum
                    payload = {
                        "jsonrpc": "2.0",
                        "method": "eth_blockNumber",
                        "params": [],
                        "id": 1
                    }
                    async with session.post(node_url, json=payload, timeout=10) as response:
                        return response.status == 200
                else:
                    # Prueba genérica
                    async with session.get(node_url, timeout=10) as response:
                        return response.status == 200
        except:
            return False