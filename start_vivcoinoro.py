#!/usr/bin/env python3
"""
Script de Inicio Automático para VivCoinORo
Ejecuta todo el sistema con una sola command
"""

import os
import sys
import asyncio
import argparse

def main():
    """Función principal de inicio"""
    parser = argparse.ArgumentParser(description='VivCoinORo - Sistema Blockchain de Oro Digital')
    parser.add_argument('--auto', action='store_true', help='Inicio completamente automático')
    parser.add_argument('--testnet', action='store_true', help='Usar redes de test')
    parser.add_argument('--no-ui', action='store_true', help='Ejecutar sin interfaz web')
    
    args = parser.parse_args()
    
    print("""
    ╔═══════════════════════════════════════════════╗
    ║            🚀 VIVCOINORO SYSTEM              ║
    ║           El Oro Digital del Futuro          ║
    ║                                               ║
    ║  • Comportamiento equiparable al Oro         ║
    ║  • Conexiones automáticas a Blockchains      ║
    ║  • Wallet Multi-Cadena Integrada             ║
    ║  • Sistema P2P Completo                      ║
    ║  • Respaldo en Oro en Tiempo Real            ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    # Configurar variables de entorno
    if args.testnet:
        os.environ['VIVCOINORO_NETWORK'] = 'testnet'
        print("🔧 Modo: TESTNET")
    else:
        os.environ['VIVCOINORO_NETWORK'] = 'mainnet'
        print("🔧 Modo: MAINNET")
    
    # Ejecutar sistema principal
    try:
        from main import main as run_system
        asyncio.run(run_system())
    except KeyboardInterrupt:
        print("\n🛑 Sistema detenido por el usuario")
    except Exception as e:
        print(f"❌ Error iniciando sistema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()