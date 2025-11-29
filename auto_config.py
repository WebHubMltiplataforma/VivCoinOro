# Configuración Automática de VivCoinORo
AUTO_CONFIG = {
    'blockchain': {
        'auto_connect': True,
        'auto_sync': True,
        'reconnect_attempts': 3,
        'health_check_interval': 60
    },
    'wallet': {
        'auto_create': True,
        'auto_backup': True,
        'multi_chain': True,
        'backup_interval': 3600
    },
    'network': {
        'discover_peers': True,
        'max_connections': 50,
        'node_timeout': 30
    },
    'api': {
        'auto_start': True,
        'port': 5000,
        'cors_enabled': True
    },
    'monitoring': {
        'price_alerts': True,
        'health_checks': True,
        'performance_metrics': True
    }
}

# Blockchains para conectar automáticamente
AUTO_CONNECT_CHAINS = [
    'bitcoin',
    'ethereum', 
    'binance',
    'solana',
    'avalanche',
    'polygon',
    'arbitrum', 
    'optimism'
]

# Configuración de APIs públicas
PUBLIC_APIS = {
    'bitcoin': [
        'https://blockstream.info/api/',
        'https://mempool.space/api/'
    ],
    'ethereum': [
        'https://mainnet.infura.io/v3/',
        'https://cloudflare-eth.com/'
    ],
    'price_feeds': [
        'https://api.coingecko.com/api/v3/',
        'https://api.binance.com/api/v3/',
        'https://min-api.cryptocompare.com/data/'
    ]
}