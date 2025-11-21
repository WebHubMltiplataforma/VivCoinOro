// 💰 GESTIÓN AUTOMÁTICA DE WALLETS
class AutoWalletManager {
    constructor() {
        this.wallets = {};
        this.balances = {};
        this.tokenPrices = {};
    }

    // Inicializar gestión automática de wallets
    async initializeWallets() {
        console.log('💰 Inicializando gestión automática de wallets...');
        
        // Configurar wallets automáticas
        this.setupAutoWallets();
        
        // Cargar balances automáticamente
        await this.loadAllBalances();
        
        // Iniciar monitoreo continuo
        this.startBalanceMonitoring();
        
        // Monitorear precios de tokens
        this.startPriceMonitoring();
    }

    // Configurar wallets automáticas
    setupAutoWallets() {
        this.wallets = {
            VAULT: {
                address: CONFIG.WALLETS.VAULT,
                type: 'vault',
                name: 'Bóveda Principal',
                autoManage: true
            },
            WALLET1: {
                address: CONFIG.WALLETS.WALLET1,
                type: 'operational',
                name: 'Wallet Operativa 1',
                autoManage: true
            },
            WALLET2: {
                address: CONFIG.WALLETS.WALLET2,
                type: 'operational', 
                name: 'Wallet Operativa 2',
                autoManage: true
            },
            METAMASK: {
                address: CONFIG.WALLETS.METAMASK,
                type: 'user',
                name: 'MetaMask Usuario',
                autoManage: false
            }
        };
        
        console.log('✅ Wallets configuradas:', this.wallets);
    }

    // Cargar todos los balances automáticamente
    async loadAllBalances() {
        const balancePromises = [];
        
        for (const [walletKey, wallet] of Object.entries(this.wallets)) {
            if (wallet.autoManage) {
                balancePromises.push(this.loadWalletBalances(walletKey, wallet.address));
            }
        }
        
        await Promise.allSettled(balancePromises);
        this.updateWalletUI();
    }

    // Cargar balances de una wallet específica
    async loadWalletBalances(walletKey, address) {
        try {
            const balances = {};
            
            // Obtener balances nativos de cada red
            for (const [network, web3] of Object.entries(window.autoConnector.web3Instances)) {
                if (web3 && network !== 'METAMASK') {
                    try {
                        const balance = await web3.eth.getBalance(address);
                        const symbol = this.getNativeSymbol(network);
                        
                        balances[symbol] = {
                            balance: web3.utils.fromWei(balance, 'ether'),
                            raw: balance,
                            network: network
                        };
                    } catch (error) {
                        console.warn(`No se pudo obtener balance ${network} para ${address}`);
                    }
                }
            }
            
            // Obtener balances de tokens ERC-20
            await this.loadTokenBalances(address, balances);
            
            this.balances[walletKey] = balances;
            console.log(`✅ Balances cargados para ${walletKey}:`, balances);
            
        } catch (error) {
            console.error(`❌ Error cargando balances para ${walletKey}:`, error);
        }
    }

    // Obtener símbolo nativo de la red
    getNativeSymbol(network) {
        const symbols = {
            ETHEREUM: 'ETH',
            POLYGON: 'MATIC',
            BSC: 'BNB',
            BASE: 'ETH',
            ARBITRUM: 'ETH',
            OPTIMISM: 'ETH',
            AVALANCHE: 'AVAX',
            ZKSYNC: 'ETH',
            LINEA: 'ETH',
            SCROLL: 'ETH'
        };
        return symbols[network] || network;
    }

    // Cargar balances de tokens ERC-20
    async loadTokenBalances(address, balances) {
        // ABI mínimo para balanceOf
        const minABI = [
            {
                "constant": true,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            }
        ];
        
        // Tokens a verificar (USDT, USDC, DAI, etc.)
        const commonTokens = {
            ETHEREUM: {
                'USDT': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
                'USDC': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
                'DAI': '0x6B175474E89094C44Da98b954EedeAC495271d0F'
            },
            POLYGON: {
                'USDT': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
                'USDC': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
                'DAI': '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063'
            }
        };
        
        for (const [network, tokens] of Object.entries(commonTokens)) {
            const web3 = window.autoConnector.getWeb3(network);
            if (!web3) continue;
            
            for (const [symbol, contractAddress] of Object.entries(tokens)) {
                try {
                    const contract = new web3.eth.Contract(minABI, contractAddress);
                    const balance = await contract.methods.balanceOf(address).call();
                    const decimalBalance = balance / 10**6; // Asumiendo 6 decimales para stablecoins
                    
                    if (decimalBalance > 0) {
                        balances[symbol] = {
                            balance: decimalBalance,
                            raw: balance,
                            network: network,
                            contract: contractAddress
                        };
                    }
                } catch (error) {
                    // Continuar con el siguiente token
                }
            }
        }
    }

    // Monitoreo continuo de balances
    startBalanceMonitoring() {
        setInterval(async () => {
            await this.loadAllBalances();
        }, 30000); // Actualizar cada 30 segundos
    }

    // Monitoreo de precios
    async startPriceMonitoring() {
        setInterval(async () => {
            await this.updateTokenPrices();
        }, 60000); // Actualizar precios cada minuto
    }

    // Actualizar precios de tokens
    async updateTokenPrices() {
        try {
            // Simular obtención de precios (integrar con API real)
            this.tokenPrices = {
                'ETH': { price: 1850.75, change: 1.2 },
                'MATIC': { price: 0.75, change: 0.5 },
                'BNB': { price: 215.30, change: -0.3 },
                'USDT': { price: 1.00, change: 0.0 },
                'USDC': { price: 1.00, change: 0.0 }
            };
            
            this.updateWalletUI();
        } catch (error) {
            console.error('Error actualizando precios:', error);
        }
    }

    // Actualizar interfaz de usuario
    updateWalletUI() {
        if (typeof window.updateWalletDisplay === 'function') {
            window.updateWalletDisplay(this.wallets, this.balances, this.tokenPrices);
        }
    }

    // Obtener balance total en USD
    getTotalBalanceUSD(walletKey) {
        const balances = this.balances[walletKey];
        if (!balances) return 0;
        
        let total = 0;
        for (const [symbol, data] of Object.entries(balances)) {
            const price = this.tokenPrices[symbol]?.price || 0;
            total += parseFloat(data.balance) * price;
        }
        
        return total;
    }

    // Transferencia automática entre wallets
    async autoTransfer(fromWallet, toWallet, amount, symbol) {
        // Implementar lógica de transferencia automática
        console.log(`🔄 Transferencia automática: ${amount} ${symbol} de ${fromWallet} a ${toWallet}`);
        
        // Aquí iría la lógica real de transferencia
        return true;
    }
}

// Instancia global del gestor de wallets
window.autoWalletManager = new AutoWalletManager();