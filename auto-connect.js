// 🔗 CONEXIÓN AUTOMÁTICA A BLOCKCHAINS
class AutoConnector {
    constructor() {
        this.web3Instances = {};
        this.connections = {};
        this.isConnected = false;
    }

    // Conectar automáticamente a todas las blockchains
    async connectAllBlockchains() {
        console.log('🚀 Iniciando conexión automática a todas las blockchains...');
        
        const connectionPromises = [];
        
        // Conectar a mainnets
        for (const [network, endpoint] of Object.entries(CONFIG.RPC_ENDPOINTS)) {
            connectionPromises.push(this.connectToChain(network, endpoint));
        }
        
        // Conectar a testnets
        for (const [network, endpoint] of Object.entries(CONFIG.TESTNET_ENDPOINTS)) {
            connectionPromises.push(this.connectToChain(network, endpoint));
        }
        
        // Esperar todas las conexiones
        await Promise.allSettled(connectionPromises);
        
        // Conectar MetaMask
        await this.connectMetaMask();
        
        // Monitorear conexiones
        this.startConnectionMonitoring();
        
        console.log('✅ Todas las conexiones establecidas');
        return this.connections;
    }

    // Conectar a una blockchain específica
    async connectToChain(network, endpoint) {
        try {
            const web3 = new Web3(new Web3.providers.HttpProvider(endpoint));
            
            // Verificar conexión
            const blockNumber = await web3.eth.getBlockNumber();
            const latency = await this.testLatency(web3);
            
            this.web3Instances[network] = web3;
            this.connections[network] = {
                status: 'connected',
                blockNumber: blockNumber,
                latency: latency,
                endpoint: endpoint,
                lastUpdate: new Date()
            };
            
            console.log(`✅ ${network} conectado - Bloque: ${blockNumber}, Latencia: ${latency}ms`);
            return this.connections[network];
            
        } catch (error) {
            console.error(`❌ Error conectando a ${network}:`, error);
            this.connections[network] = {
                status: 'error',
                error: error.message,
                endpoint: endpoint,
                lastUpdate: new Date()
            };
            return this.connections[network];
        }
    }

    // Conectar MetaMask automáticamente
    async connectMetaMask() {
        if (typeof window.ethereum !== 'undefined') {
            try {
                // Solicitar conexión de cuenta
                const accounts = await window.ethereum.request({ 
                    method: 'eth_requestAccounts' 
                });
                
                const web3 = new Web3(window.ethereum);
                this.web3Instances['METAMASK'] = web3;
                
                this.connections['METAMASK'] = {
                    status: 'connected',
                    address: accounts[0],
                    networkId: await web3.eth.net.getId(),
                    lastUpdate: new Date()
                };
                
                console.log('✅ MetaMask conectado:', accounts[0]);
                
                // Escuchar cambios de cuenta
                window.ethereum.on('accountsChanged', (accounts) => {
                    this.handleAccountsChanged(accounts);
                });
                
                // Escuchar cambios de red
                window.ethereum.on('chainChanged', (chainId) => {
                    this.handleChainChanged(chainId);
                });
                
            } catch (error) {
                console.error('❌ Error conectando MetaMask:', error);
            }
        } else {
            console.warn('⚠️ MetaMask no detectado');
        }
    }

    // Probar latencia de conexión
    async testLatency(web3) {
        const startTime = Date.now();
        try {
            await web3.eth.getBlockNumber();
            return Date.now() - startTime;
        } catch (error) {
            return null;
        }
    }

    // Monitorear conexiones continuamente
    startConnectionMonitoring() {
        setInterval(async () => {
            for (const [network, connection] of Object.entries(this.connections)) {
                if (connection.status === 'connected' && network !== 'METAMASK') {
                    try {
                        const web3 = this.web3Instances[network];
                        const blockNumber = await web3.eth.getBlockNumber();
                        const latency = await this.testLatency(web3);
                        
                        this.connections[network].blockNumber = blockNumber;
                        this.connections[network].latency = latency;
                        this.connections[network].lastUpdate = new Date();
                        
                    } catch (error) {
                        this.connections[network].status = 'error';
                        this.connections[network].error = error.message;
                    }
                }
            }
            
            // Actualizar UI
            this.updateConnectionUI();
            
        }, 10000); // Actualizar cada 10 segundos
    }

    // Manejar cambio de cuentas en MetaMask
    handleAccountsChanged(accounts) {
        if (accounts.length === 0) {
            console.log('🔒 MetaMask desconectado');
            this.connections['METAMASK'].status = 'disconnected';
        } else {
            console.log('🔄 Cuenta MetaMask cambiada:', accounts[0]);
            this.connections['METAMASK'].address = accounts[0];
        }
        this.updateConnectionUI();
    }

    // Manejar cambio de red en MetaMask
    handleChainChanged(chainId) {
        console.log('🔄 Red MetaMask cambiada:', chainId);
        this.connections['METAMASK'].networkId = parseInt(chainId);
        this.updateConnectionUI();
    }

    // Actualizar interfaz de usuario
    updateConnectionUI() {
        if (typeof window.updateConnectionsList === 'function') {
            window.updateConnectionsList(this.connections);
        }
    }

    // Obtener instancia Web3 para una red específica
    getWeb3(network) {
        return this.web3Instances[network];
    }

    // Obtener estado de todas las conexiones
    getConnectionStatus() {
        return this.connections;
    }
}

// Instancia global del conector automático
window.autoConnector = new AutoConnector();