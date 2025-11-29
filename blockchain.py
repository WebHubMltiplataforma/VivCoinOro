import hashlib
import json
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: Decimal
    timestamp: float
    signature: str
    tx_id: str = None
    
    def __post_init__(self):
        if not self.tx_id:
            self.tx_id = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        tx_string = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return hashlib.sha256(tx_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': float(self.amount),
            'timestamp': self.timestamp,
            'signature': self.signature,
            'tx_id': self.tx_id
        }

class Block:
    def __init__(self, index: int, transactions: List[Transaction], 
                 timestamp: float, previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        block_string = f"{self.index}{[tx.to_dict() for tx in self.transactions]}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class VivCoinORoBlockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = 4
        self.mining_reward = Decimal('50.0')
        self.total_supply = Decimal('21000000.0')  # Similar a Bitcoin
        self.gold_backing_reserve = Decimal('0.0')
        
        # Crear bloque génesis
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_transaction = Transaction(
            sender="0",
            recipient="VIVCOIN_FOUNDATION",
            amount=Decimal('1000000.0'),
            timestamp=time.time(),
            signature="GENESIS"
        )
        genesis_block = Block(0, [genesis_transaction], time.time(), "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        self.gold_backing_reserve += Decimal('100000.0')  # Reserva inicial de oro
    
    def get_latest_block(self) -> Block:
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> bool:
        # Validar transacción
        if not self.validate_transaction(transaction):
            return False
        
        self.pending_transactions.append(transaction)
        return True
    
    def validate_transaction(self, transaction: Transaction) -> bool:
        # Implementar validación de firma y saldo
        return True
    
    def mine_pending_transactions(self, mining_reward_address: str) -> Block:
        # Agregar transacción de recompensa
        reward_tx = Transaction(
            sender="0",
            recipient=mining_reward_address,
            amount=self.mining_reward,
            timestamp=time.time(),
            signature="MINING_REWARD"
        )
        self.pending_transactions.append(reward_tx)
        
        block = Block(
            len(self.chain),
            self.pending_transactions,
            time.time(),
            self.get_latest_block().hash
        )
        
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []
        
        # Ajustar reserva de oro basado en el precio actual
        self.adjust_gold_backing()
        
        return block
    
    def adjust_gold_backing(self):
        # Simular ajuste de reserva basado en precio del oro
        gold_price = self.get_current_gold_price()
        target_backing = self.calculate_total_value() / gold_price
        self.gold_backing_reserve = target_backing
    
    def get_current_gold_price(self) -> Decimal:
        # Conectar con oráculo de precio del oro
        return Decimal('1800.0')  # Precio ejemplo
    
    def calculate_total_value(self) -> Decimal:
        total_coins = sum(
            Decimal(str(tx.amount)) 
            for block in self.chain 
            for tx in block.transactions 
            if tx.recipient != "0"
        )
        return total_coins * self.get_current_vivcoin_price()
    
    def get_current_vivcoin_price(self) -> Decimal:
        # Basado en reserva de oro y oferta circulante
        circulating_supply = self.get_circulating_supply()
        if circulating_supply > 0:
            return (self.gold_backing_reserve * self.get_current_gold_price()) / circulating_supply
        return Decimal('1.0')
    
    def get_circulating_supply(self) -> Decimal:
        total = Decimal('0.0')
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == "0":  # Emisión nueva
                    total += tx.amount
        return total
    
    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True