from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
import time
from decimal import Decimal

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Instancias globales (en producción usar inyección de dependencias)
blockchain = None
wallet = None
p2p_exchange = None

@app.route('/api/blockchain/info', methods=['GET'])
def get_blockchain_info():
    return jsonify({
        'height': len(blockchain.chain),
        'current_difficulty': blockchain.difficulty,
        'total_supply': float(blockchain.get_circulating_supply()),
        'gold_backing_ratio': float(blockchain.get_gold_backing_ratio()),
        'current_price': float(blockchain.get_current_vivcoin_price()),
        'gold_reserve': float(blockchain.gold_backing_reserve)
    })

@app.route('/api/wallet/balance', methods=['GET'])
def get_wallet_balance():
    address = request.args.get('address')
    if not address:
        return jsonify({'error': 'Address required'}), 400
    
    balances = wallet.get_multi_chain_balance()
    return jsonify({
        'address': address,
        'balances': {k: float(v) for k, v in balances.items()}
    })

@app.route('/api/exchange/orderbook/<pair>', methods=['GET'])
def get_orderbook(pair):
    orderbook = p2p_exchange.get_order_book(pair)
    return jsonify(orderbook)

@app.route('/api/exchange/order', methods=['POST'])
def create_order():
    data = request.json
    try:
        result = p2p_exchange.create_order(
            pair=data['pair'],
            order_type=data['order_type'],
            price=Decimal(str(data['price'])),
            amount=Decimal(str(data['amount'])),
            user_id=data['user_id']
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connection_established', {'status': 'connected'})

@socketio.on('subscribe_price')
def handle_price_subscription(data):
    pair = data.get('pair', 'VIVCOIN/USD')
    # Enviar updates periódicos de precio
    # Implementar lógica real de suscripción

@socketio.on('new_transaction')
def handle_new_transaction(data):
    # Broadcast nueva transacción a todos los clientes
    emit('transaction_update', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)