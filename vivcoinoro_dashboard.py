from flask import Flask, render_template, jsonify

app = Flask(__name__)

class VivCoinORoDashboard:
    def __init__(self):
        self.app = app
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/')
        def dashboard():
            return render_template('index.html')
        
        @self.app.route('/api/system-status')
        def system_status():
            return jsonify({
                'status': 'operational',
                'blockchains_connected': 8,
                'liquidity_pools': 5,
                'exchange_registrations': 6,
                'gold_backing_ratio': 0.85
            })
        
        @self.app.route('/api/price-data')
        def price_data():
            return jsonify({
                'viv_price': 0.0185,
                'gold_price': 1850.75,
                'market_cap': 385000000,
                'volume_24h': 2500000
            })
    
    async def launch(self):
        """Lanzar servidor web"""
        import threading
        
        def run_server():
            self.app.run(host='0.0.0.0', port=8080, debug=False)
            
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        print("🌐 Dashboard web: http://localhost:8080")