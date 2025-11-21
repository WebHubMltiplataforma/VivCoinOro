// 🔐 CONFIGURACIÓN AUTOMÁTICA DE APIS Y CONEXIONES
const CONFIG = {
    // INFURA CONFIGURATION
    INFURA_KEY: "4df8eead51294cd09eadf4b51efaa014",
    
    // POLYGONSCAN API
    POLYGONSCAN_API_KEY: "01b_Lg_ZvjpnKoQGgqGlT",
    
    // QUICKNODE CONFIG
    QUICKNODE: {
        WSS_URL: "wss://purple-bold-sunset.matic.quiknode.pro/6e2958c9720ad8d75f46b01d483e002df46d4524",
        HTTP_URL: "https://purple-bold-sunset.matic.quiknode.pro/6e2958c9720ad8d75f46b01d483e002df46d4524",
        API_KEY: "QN_d030347654fb4367a09e6b9f56a71ddb"
    },
    
    // ETHERSCAN API
    ETHERSCAN_API: "0x0e3a2a1f2146d86a604adc220b4967a898d7fe07",
    
    // WALLETS AUTOMÁTICAS
    WALLETS: {
        VAULT: "0xfb146E2601c5F77743E4888E75D6577C2F56bAbb",
        WALLET1: "0x5182CaAe1EccBa71aa854E89847eE530a361b8bA", 
        WALLET2: "0x5774808c2856f7FDF1A0a8F375A41559794BeF6B",
        METAMASK: "0xfb146E2601c5F77743E4888E75D6577C2F56bAbb"
    },
    
    // CONTRATOS INTELIGENTES
    CONTRACTS: {
        VIV_TOKEN: "0xfb146E2601c5F77743E4888E75D6577C2F56bAbb",
        LIQUIDITY_POOL: "0x5774808c2856f7FDF1A0a8F375A41559794BeF6B",
        TREASURY: "0x5182CaAe1EccBa71aa854E89847eE530a361b8bA"
    },
    
    // RPC ENDPOINTS AUTOMÁTICOS
    RPC_ENDPOINTS: {
        ETHEREUM: "https://mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        POLYGON: "https://polygon-mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        BSC: "https://bsc-mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        BASE: "https://base-mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        ARBITRUM: "https://arbitrum-mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        OPTIMISM: "https://optimism-mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        AVALANCHE: "https://avalanche-mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        ZKSYNC: "https://zksync-mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        LINEA: "https://linea-mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        SCROLL: "https://scroll-mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        MANTLE: "https://mantle-mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        BLAST: "https://blast-mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014"
    },
    
    // TESTNETS
    TESTNET_ENDPOINTS: {
        SEPOLIA: "https://sepolia.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        POLYGON_AMOY: "https://polygon-amoy.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        BASE_SEPOLIA: "https://base-sepolia.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
        OPTIMISM_SEPOLIA: "https://optimism-sepolia.infura.io/v3/4df8eead51294cd09eadf4b51efaa014"
    }
};

// Exportar configuración para uso global
window.VIV_CONFIG = CONFIG;