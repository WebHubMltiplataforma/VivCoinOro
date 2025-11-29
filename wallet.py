import hashlib
import json
import hmac
from decimal import Decimal
from typing import Dict, List, Optional
import secp256k1
import base58

class VivCoinORoWallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.address = None
        self.balance = Decimal('0.0')
        self.transaction_history = []
        self.connected_chains = {}
        
    def generate_keypair(self):
        """Generar par de claves usando secp256k1 (mismo que Bitcoin)"""
        self.private_key = secp256k1.PrivateKey()
        self.public_key = self.private_key.pubkey
        self.address = self.generate_address()
    
    def generate_address(self) -> str:
        """Generar dirección estilo Bitcoin"""
        # Hash SHA-256 de la clave pública
        sha256_hash = hashlib.sha256(self.public_key.serialize()).digest()
        
        # Hash RIPEMD-160
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
        
        # Agregar version byte (0x00 para Bitcoin mainnet)
        versioned_payload = b'\x00' + ripemd160_hash
        
        # Checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
        
        # Codificar Base58
        full_payload = versioned_payload + checksum
        return base58.b58encode(full_payload).decode('utf-8')
    
    def sign_transaction(self, transaction_data: Dict) -> str:
        """Firmar transacción"""
        message = json.dumps(transaction_data, sort_keys=True).encode()
        signature = self.private_key.ecdsa_sign(message)
        return self.private_key.ecdsa_serialize(signature).hex()
    
    def verify_signature(self, public_key: str, signature: str, message: str) -> bool:
        """Verificar firma"""
        try:
            pubkey = secp256k1.PublicKey(bytes.fromhex(public_key))
            sig = secp256k1.ecdsa_signature(bytes.fromhex(signature))
            return pubkey.ecdsa_verify(message.encode(), sig)
        except:
            return False
    
    def connect_to_blockchain(self, chain_name: str, adapter):
        """Conectar a otra blockchain"""
        self.connected_chains[chain_name] = adapter
        print(f"Conectado a {chain_name}")
    
    def get_multi_chain_balance(self) -> Dict[str, Decimal]:
        """Obtener balance de todas las cadenas conectadas"""
        balances = {'VivCoinORo': self.balance}
        
        for chain_name, adapter in self.connected_chains.items():
            try:
                chain_balance = adapter.get_balance(self.address)
                balances[chain_name] = chain_balance
            except Exception as e:
                print(f"Error obteniendo balance de {chain_name}: {e}")
        
        return balances
    
    def cross_chain_swap(self, from_chain: str, to_chain: str, amount: Decimal) -> bool:
        """Intercambio entre cadenas diferentes"""
        if from_chain not in self.connected_chains or to_chain not in self.connected_chains:
            return False
        
        try:
            # Implementar lógica de intercambio cross-chain
            return self.connected_chains[from_chain].transfer(
                self.connected_chains[to_chain],
                amount,
                self.address
            )
        except Exception as e:
            print(f"Error en intercambio cross-chain: {e}")
            return False