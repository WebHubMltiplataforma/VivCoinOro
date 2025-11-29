from decimal import Decimal
from typing import List, Dict, Optional
from enum import Enum
import time

class OrderType(Enum):
    BUY = "BUY"
    SELL = "SELL"

class Order:
    def __init__(self, order_id: str, order_type: OrderType, price: Decimal, 
                 amount: Decimal, user_id: str, timestamp: float = None):
        self.order_id = order_id
        self.order_type = order_type
        self.price = price
        self.amount = amount
        self.user_id = user_id
        self.timestamp = timestamp or time.time()
        self.filled_amount = Decimal('0.0')
    
    @property
    def remaining_amount(self) -> Decimal:
        return self.amount - self.filled_amount
    
    def fill(self, amount: Decimal) -> bool:
        if amount <= self.remaining_amount:
            self.filled_amount += amount
            return True
        return False

class OrderBook:
    def __init__(self):
        self.buy_orders: List[Order] = []
        self.sell_orders: List[Order] = []
        self.trade_history = []
    
    def add_order(self, order: Order) -> List[Dict]:
        """Agregar orden y ejecutar matching"""
        if order.order_type == OrderType.BUY:
            return self._match_buy_order(order)
        else:
            return self._match_sell_order(order)
    
    def _match_buy_order(self, buy_order: Order) -> List[Dict]:
        trades = []
        
        # Buscar órdenes de venta que coincidan
        for sell_order in sorted(self.sell_orders, key=lambda x: x.price):
            if sell_order.price <= buy_order.price and buy_order.remaining_amount > 0:
                trade_amount = min(buy_order.remaining_amount, sell_order.remaining_amount)
                trade_price = sell_order.price
                
                # Ejecutar trade
                if self._execute_trade(buy_order, sell_order, trade_amount, trade_price):
                    trades.append({
                        'buyer': buy_order.user_id,
                        'seller': sell_order.user_id,
                        'amount': float(trade_amount),
                        'price': float(trade_price),
                        'timestamp': time.time()
                    })
                
                # Remover orden completada
                if sell_order.remaining_amount == 0:
                    self.sell_orders.remove(sell_order)
            
            if buy_order.remaining_amount == 0:
                break
        
        # Si queda cantidad, agregar a order book
        if buy_order.remaining_amount > 0:
            self.buy_orders.append(buy_order)
            self.buy_orders.sort(key=lambda x: x.price, reverse=True)
        
        return trades
    
    def _match_sell_order(self, sell_order: Order) -> List[Dict]:
        trades = []
        
        # Buscar órdenes de compra que coincidan
        for buy_order in sorted(self.buy_orders, key=lambda x: x.price, reverse=True):
            if buy_order.price >= sell_order.price and sell_order.remaining_amount > 0:
                trade_amount = min(sell_order.remaining_amount, buy_order.remaining_amount)
                trade_price = buy_order.price
                
                # Ejecutar trade
                if self._execute_trade(buy_order, sell_order, trade_amount, trade_price):
                    trades.append({
                        'buyer': buy_order.user_id,
                        'seller': sell_order.user_id,
                        'amount': float(trade_amount),
                        'price': float(trade_price),
                        'timestamp': time.time()
                    })
                
                # Remover orden completada
                if buy_order.remaining_amount == 0:
                    self.buy_orders.remove(buy_order)
            
            if sell_order.remaining_amount == 0:
                break
        
        # Si queda cantidad, agregar a order book
        if sell_order.remaining_amount > 0:
            self.sell_orders.append(sell_order)
            self.sell_orders.sort(key=lambda x: x.price)
        
        return trades
    
    def _execute_trade(self, buy_order: Order, sell_order: Order, 
                      amount: Decimal, price: Decimal) -> bool:
        """Ejecutar intercambio entre órdenes"""
        if buy_order.fill(amount) and sell_order.fill(amount):
            # Registrar en historial
            self.trade_history.append({
                'timestamp': time.time(),
                'price': float(price),
                'amount': float(amount),
                'buy_order': buy_order.order_id,
                'sell_order': sell_order.order_id
            })
            return True
        return False
    
    def get_market_price(self) -> Optional[Decimal]:
        """Obtener precio de mercado actual"""
        if not self.trade_history:
            return None
        
        recent_trades = sorted(self.trade_history, key=lambda x: x['timestamp'], reverse=True)[:10]
        if not recent_trades:
            return None
        
        total_volume = sum(trade['amount'] for trade in recent_trades)
        if total_volume == 0:
            return None
        
        weighted_price = sum(trade['price'] * trade['amount'] for trade in recent_trades) / total_volume
        return Decimal(str(weighted_price))
    
    def cancel_order(self, order_id: str, user_id: str) -> bool:
        """Cancelar orden"""
        for order_list in [self.buy_orders, self.sell_orders]:
            for order in order_list:
                if order.order_id == order_id and order.user_id == user_id:
                    order_list.remove(order)
                    return True
        return False

class P2PExchange:
    def __init__(self):
        self.order_books = {}  # par trading -> OrderBook
        self.escrow_service = EscrowService()
        self.users = {}
    
    def create_order(self, pair: str, order_type: OrderType, price: Decimal, 
                    amount: Decimal, user_id: str) -> Dict:
        """Crear nueva orden de trading"""
        if pair not in self.order_books:
            self.order_books[pair] = OrderBook()
        
        order_id = f"order_{int(time.time()*1000)}_{user_id}"
        order = Order(order_id, order_type, price, amount, user_id)
        
        # Ejecutar matching
        trades = self.order_books[pair].add_order(order)
        
        # Procesar trades a través de escrow
        for trade in trades:
            self.escrow_service.process_trade(trade, pair)
        
        return {
            'order_id': order_id,
            'trades_executed': trades,
            'remaining_amount': float(order.remaining_amount)
        }
    
    def get_order_book(self, pair: str) -> Dict:
        """Obtener estado del order book"""
        if pair not in self.order_books:
            return {'buy_orders': [], 'sell_orders': []}
        
        order_book = self.order_books[pair]
        return {
            'buy_orders': [
                {
                    'price': float(order.price),
                    'amount': float(order.remaining_amount),
                    'user_id': order.user_id
                }
                for order in order_book.buy_orders[:20]  # Top 20
            ],
            'sell_orders': [
                {
                    'price': float(order.price),
                    'amount': float(order.remaining_amount),
                    'user_id': order.user_id
                }
                for order in order_book.sell_orders[:20]  # Top 20
            ],
            'market_price': float(order_book.get_market_price() or Decimal('0.0'))
        }

class EscrowService:
    def __init__(self):
        self.active_escrows = {}
    
    def process_trade(self, trade: Dict, pair: str):
        """Procesar trade a través de escrow seguro"""
        escrow_id = f"escrow_{int(time.time()*1000)}"
        
        self.active_escrows[escrow_id] = {
            'trade': trade,
            'pair': pair,
            'status': 'pending',
            'created_at': time.time(),
            'buyer_confirmed': False,
            'seller_confirmed': False
        }
        
        # Iniciar proceso de confirmación
        self._initiate_confirmations(escrow_id)
    
    def _initiate_confirmations(self, escrow_id: str):
        """Iniciar confirmaciones de las partes"""
        # Enviar notificaciones a comprador y vendedor
        # Implementar lógica de confirmación
        pass
    
    def confirm_trade(self, escrow_id: str, user_id: str) -> bool:
        """Confirmar trade por usuario"""
        if escrow_id not in self.active_escrows:
            return False
        
        escrow = self.active_escrows[escrow_id]
        trade = escrow['trade']
        
        if user_id == trade['buyer']:
            escrow['buyer_confirmed'] = True
        elif user_id == trade['seller']:
            escrow['seller_confirmed'] = True
        
        # Si ambas partes confirman, liberar fondos
        if escrow['buyer_confirmed'] and escrow['seller_confirmed']:
            return self._release_funds(escrow_id)
        
        return True
    
    def _release_funds(self, escrow_id: str) -> bool:
        """Liberar fondos del escrow"""
        escrow = self.active_escrows[escrow_id]
        escrow['status'] = 'completed'
        
        # Implementar transferencia real de fondos
        print(f"Funds released for escrow {escrow_id}")
        return True