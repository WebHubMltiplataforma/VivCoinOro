#!/usr/bin/env python3
"""
Inicio completo con frontend web
"""

import threading
import webbrowser
import time
from api.rest_api import app

def start_backend():
    """Iniciar backend Flask"""
    print("🚀 Iniciando backend VivCoinORo...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def open_browser():
    """Abrir navegador automáticamente"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

if __name__ == "__main__":
    # Iniciar backend en thread separado
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Abrir navegador
    print("🌐 Abriendo interfaz web...")
    open_browser()
    
    # Mantener el script corriendo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Cerrando VivCoinORo...")