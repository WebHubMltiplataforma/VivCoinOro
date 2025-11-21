// 🚀 INICIALIZACIÓN PRINCIPAL DEL SISTEMA AUTOMÁTICO
class VivCoinORoSystem {
    constructor() {
        this.isSystemActive = false;
        this.initialized = false;
    }

    // Inicializar sistema completo automáticamente
    async initializeAutoSystem() {
        if (this.initialized) {
            console.log('✅ Sistema ya inicializado');
            return;
        }

        console.log('🚀 INICIANDO SISTEMA VIVCOINORO AUTOMÁTICO...');
        
        try {
            // 1. Conectar a todas las blockchains automáticamente
            await window.autoConnector.connectAllBlockchains();
            
            // 2. Inicializar gestión automática de wallets
            await window.autoWalletManager.initializeWallets();
            
            // 3. Inicializar trading automático
            await window.autoTrading.initializeAutoTrading();
            
            this.initialized = true;
            this.isSystemActive = true;
            
            // Actualizar UI
            this.updateSystemUI();
            
            console.log('🎉 SISTEMA VIVCOINORO INICIALIZADO EXITOSAMENTE');
            alert('✅ Sistema VivCoinORo inicializado automáticamente!\n\n• Todas las blockchains conectadas\n• Wallets automáticas configuradas\n• Sistema de trading listo');
            
        } catch (error) {
            console.error('❌ Error inicializando sistema:', error);
            alert('❌ Error inicializando sistema automático. Verifica la consola para más detalles.');
        }
    }

    // Actualizar interfaz de usuario
    updateSystemUI() {
        // Actualizar estado global
        document.getElementById('globalStatus').textContent = 'SISTEMA AUTOMÁTICO ACTIVO';
        
        // Actualizar contador de conexiones
        const connections = window.autoConnector.getConnectionStatus();
        const connectedCount = Object.values(connections).filter(c => c.status === 'connected').length;
        document.getElementById('connectionsCount').textContent = `${connectedCount} conectadas`;
        
        // Actualizar lista de conexiones
        this.updateConnectionsList(connections);
        
        // Actualizar display de wallets
        this.updateWalletDisplay();
    }

    // Actualizar lista de conexiones en UI
    updateConnectionsList(connections) {
        const connectionsList = document.getElementById('connectionsList');
        connectionsList.innerHTML = '';
        
        for (const [network, connection] of Object.entries(connections)) {
            const connectionItem = document.createElement('div');
            connectionItem.className = 'connection-item';
            
            const statusClass = `status-${connection.status}`;
            const statusText = connection.status === 'connected' ? 'Conectado' : 
                              connection.status === 'error' ? 'Error' : 'Desconectado';
            
            connectionItem.innerHTML = `
                <div class="connection-info">
                    <div class="connection-status ${statusClass}"></div>
                    <div>
                        <div>${network}</div>
                        <div class="connection-details">
                            ${statusText} - 
                            ${connection.latency ? `${connection.latency}ms` : ''} - 
                            ${connection.blockNumber ? `Bloque #${connection.blockNumber.toLocaleString()}` : ''}
                            ${connection.address ? ` - ${connection.address.substring(0, 8)}...` : ''}
                        </div>
                    </div>
                </div>
            `;
            connectionsList.appendChild(connectionItem);
        }
    }

    // Actualizar display de wallets en UI
    updateWalletDisplay() {
        const walletsContainer = document.getElementById('autoWalletsContainer');
        const wallets = window.autoWalletManager.wallets;
        const balances = window.autoWalletManager.balances;
        
        walletsContainer.innerHTML = '';
        
        for (const [walletKey, wallet] of Object.entries(wallets)) {
            const walletBalances = balances[walletKey] || {};
            const totalUSD = window.autoWalletManager.getTotalBalanceUSD(walletKey);
            
            const walletElement = document.createElement('div');
            walletElement.className = 'wallet-display';
            walletElement.innerHTML = `
                <div class="wallet-header">
                    <strong>${wallet.name}</strong>
                    <span class="wallet-type">${wallet.type}</span>
                </div>
                <div class="wallet-address">${wallet.address}</div>
                <div class="wallet-total">Total: $${totalUSD.toFixed(2)} USD</div>
                <div class="wallet-balances">
                    ${Object.entries(walletBalances).map(([symbol, data]) => `
                        <div class="balance-item">
                            <div class="balance-amount">${parseFloat(data.balance).toFixed(4)}</div>
                            <div class="balance-label">${symbol}</div>
                        </div>
                    `).join('')}
                </div>
            `;
            walletsContainer.appendChild(walletElement);
        }
    }

    // Refrescar todas las conexiones
    async refreshAllConnections() {
        console.log('🔄 Refrescando todas las conexiones...');
        await window.autoConnector.connectAllBlockchains();
        await window.autoWalletManager.loadAllBalances();
        this.updateSystemUI();
        alert('✅ Todas las conexiones y balances actualizados automáticamente');
    }

    // Activar/desactivar trading automático
    toggleAutoTrading() {
        const isActive = window.autoTrading.toggleAutoTrading();
        document.getElementById('tradingStatus').textContent = isActive ? 'ACTIVO' : 'INACTIVO';
        
        const stats = window.autoTrading.getTradingStats();
        document.getElementById('tradingStats').innerHTML = `
            <div>Órdenes totales: ${stats.totalOrders}</div>
            <div>Estrategias activas: ${stats.activeStrategies}</div>
            <div>Ganancias hoy: $${stats.todayProfit}</div>
        `;
    }

    // Gestionar liquidez automática
    manageAutoLiquidity() {
        alert('🤖 Iniciando gestión automática de liquidez...\n\nEl sistema gestionará automáticamente:\n• Pools de liquidez\n• Rebalanceo de fondos\n• Optimización de APY');
    }
}

// Instancia global del sistema
window.vivSystem = new VivCoinORoSystem();

// Funciones globales para HTML
function initializeAutoSystem() {
    window.vivSystem.initializeAutoSystem();
}

function refreshAllConnections() {
    window.vivSystem.refreshAllConnections();
}

function toggleAutoTrading() {
    window.vivSystem.toggleAutoTrading();
}

function manageAutoLiquidity() {
    window.vivSystem.manageAutoLiquidity();
}

// Exportar funciones para uso global
window.updateConnectionsList = (connections) => {
    window.vivSystem.updateConnectionsList(connections);
};

window.updateWalletDisplay = (wallets, balances, prices) => {
    window.vivSystem.updateWalletDisplay();
};

// Inicialización automática cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏁 VivCoinORo System Cargado - Listo para Inicialización Automática');
    
    // Iniciar automáticamente después de 2 segundos
    setTimeout(() => {
        if (confirm('¿Deseas iniciar el sistema VivCoinORo automáticamente?')) {
            initializeAutoSystem();
        }
    }, 2000);
});