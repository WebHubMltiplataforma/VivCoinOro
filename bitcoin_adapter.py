# wallet/multi_chain/bitcoin_adapter.py
import hashlib
import struct
import base58
import requests
import json
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
import time

class BitcoinAdapter:
    def __init__(self, network: str = 'mainnet'):
        self.network = network
        self.rpc_url = self._get_rpc_url()
        self.headers = {'Content-Type': 'application/json'}
        
        # Configuración de redes
        self.network_params = {
            'mainnet': {
                'rpc_port': 8332,
                'network_byte': b'\x00',
                'wif_prefix': b'\x80',
                'api_base': 'https://blockstream.info/api'
            },
            'testnet': {
                'rpc_port': 18332,
                'network_byte': b'\x6f',
                'wif_prefix': b'\xef',
                'api_base': 'https://blockstream.info/testnet/api'
            }
        }
        
        # Conexión automática a nodos
        self.node_endpoints = self._discover_nodes()
        
    def _get_rpc_url(self) -> str:
        """Obtener URL RPC basado en configuración"""
        params = self.network_params[self.network]
        # En producción, usar variables de entorno
        username = "bitcoinrpc"
        password = "password"
        host = "localhost"
        port = params['rpc_port']
        
        return f"http://{username}:{password}@{host}:{port}/"
    
    def _discover_nodes(self) -> List[str]:
        """Descubrir nodos Bitcoin automáticamente"""
        public_nodes = [
            'https://blockstream.info/api/',
            'https://mempool.space/api/',
            'https://bitcoin.canadiancontrol.net/api/'
        ]
        
        if self.network == 'testnet':
            public_nodes = [
                'https://blockstream.info/testnet/api/',
                'https://mempool.space/testnet/api/'
            ]
        
        return public_nodes
    
    def rpc_call(self, method: str, params: list = None) -> Dict:
        """Llamada JSON-RPC a nodo Bitcoin"""
        payload = {
            'jsonrpc': '2.0',
            'id': 'vivcoinoro',
            'method': method,
            'params': params or []
        }
        
        # Intentar con nodos en orden
        for endpoint in [self.rpc_url] + self.node_endpoints:
            try:
                if endpoint.startswith('http'):
                    response = requests.post(
                        endpoint, 
                        json=payload, 
                        headers=self.headers,
                        timeout=30
                    )
                else:
                    response = requests.post(
                        self.rpc_url,
                        json=payload,
                        headers=self.headers,
                        timeout=30
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    if 'error' not in result or result['error'] is None:
                        return result
            except Exception as e:
                print(f"Error conectando a {endpoint}: {e}")
                continue
        
        raise Exception("No se pudo conectar a ningún nodo Bitcoin")
    
    def get_balance(self, address: str) -> Decimal:
        """Obtener balance de dirección Bitcoin"""
        try:
            # Método 1: Usando API pública
            for endpoint in self.node_endpoints:
                try:
                    response = requests.get(f"{endpoint}address/{address}", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        confirmed = data.get('chain_stats', {}).get('funded_txo_sum', 0)
                        unconfirmed = data.get('mempool_stats', {}).get('funded_txo_sum', 0)
                        total_satoshis = confirmed + unconfirmed
                        return Decimal(total_satoshis) / Decimal('100000000')
                except:
                    continue
            
            # Método 2: Usando RPC
            result = self.rpc_call('getreceivedbyaddress', [address, 1])
            return Decimal(str(result.get('result', 0)))
            
        except Exception as e:
            print(f"Error obteniendo balance Bitcoin: {e}")
            return Decimal('0')
    
    def create_transaction(self, from_address: str, to_address: str, 
                          amount: Decimal, private_key: str = None) -> Dict:
        """Crear transacción Bitcoin"""
        try:
            # Convertir a satoshis
            satoshis = int(amount * Decimal('100000000'))
            
            # Obtener UTXOs
            utxos = self.get_utxos(from_address)
            if not utxos:
                raise Exception("No hay UTXOs disponibles")
            
            # Seleccionar UTXOs para la transacción
            selected_utxos = self._select_utxos(utxos, satoshis)
            total_input = sum(utxo['value'] for utxo in selected_utxos)
            
            # Calcular fee (usar fee estimation)
            fee_rate = self.estimate_fee()
            estimated_fee = self._calculate_fee(len(selected_utxos), 2, fee_rate)
            
            # Verificar fondos suficientes
            if total_input < satoshis + estimated_fee:
                raise Exception("Fondos insuficientes")
            
            # Crear transacción
            change = total_input - satoshis - estimated_fee
            
            # Construir transacción
            transaction = {
                'inputs': selected_utxos,
                'outputs': [
                    {'address': to_address, 'value': satoshis}
                ]
            }
            
            if change > 0:
                transaction['outputs'].append({
                    'address': from_address,
                    'value': change
                })
            
            # Firmar transacción si se proporciona private_key
            if private_key:
                signed_tx = self._sign_transaction(transaction, private_key)
                transaction['signed_hex'] = signed_tx
                transaction['txid'] = self._calculate_txid(signed_tx)
            
            return transaction
            
        except Exception as e:
            print(f"Error creando transacción Bitcoin: {e}")
            raise
    
    def get_utxos(self, address: str) -> List[Dict]:
        """Obtener UTXOs no gastados"""
        try:
            utxos = []
            
            # Usar API pública
            for endpoint in self.node_endpoints:
                try:
                    response = requests.get(f"{endpoint}address/{address}/utxo", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        for utxo in data:
                            utxos.append({
                                'txid': utxo['txid'],
                                'vout': utxo['vout'],
                                'value': utxo['value'],
                                'confirmations': utxo.get('status', {}).get('confirmed', False)
                            })
                        break
                except:
                    continue
            
            return utxos
            
        except Exception as e:
            print(f"Error obteniendo UTXOs: {e}")
            return []
    
    def _select_utxos(self, utxos: List[Dict], target_amount: int) -> List[Dict]:
        """Seleccionar UTXOs usando algoritmo de selección óptima"""
        # Ordenar UTXOs por valor (mayor primero)
        utxos.sort(key=lambda x: x['value'], reverse=True)
        
        selected = []
        total = 0
        
        for utxo in utxos:
            if total >= target_amount:
                break
            selected.append(utxo)
            total += utxo['value']
        
        if total < target_amount:
            # Si no hay suficientes con mayor primero, intentar con todos
            selected = utxos
            total = sum(utxo['value'] for utxo in utxos)
            
        if total < target_amount:
            raise Exception("Fondos insuficientes")
        
        return selected
    
    def estimate_fee(self) -> int:
        """Estimar fee rate en satoshis/byte"""
        try:
            # Usar múltiples fuentes para estimación
            fee_estimates = []
            
            # Fuente 1: Mempool.space
            try:
                response = requests.get('https://mempool.space/api/v1/fees/recommended', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    fee_estimates.append(data.get('fastestFee', 20))
            except:
                pass
            
            # Fuente 2: Blockstream
            try:
                response = requests.get('https://blockstream.info/api/fee-estimates', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    fee_estimates.append(int(data.get('2', 20)))
            except:
                pass
            
            # Usar el promedio o valor por defecto
            if fee_estimates:
                return max(1, sum(fee_estimates) // len(fee_estimates))
            else:
                return 20  # Fee por defecto
            
        except Exception as e:
            print(f"Error estimando fee: {e}")
            return 20
    
    def _calculate_fee(self, input_count: int, output_count: int, fee_rate: int) -> int:
        """Calcular fee total basado en tamaño de transacción"""
        # Tamaño base + inputs * 148 + outputs * 34
        base_size = 10
        input_size = input_count * 148
        output_size = output_count * 34
        total_size = base_size + input_size + output_size
        
        return total_size * fee_rate
    
    def _sign_transaction(self, transaction: Dict, private_key_wif: str) -> str:
        """Firmar transacción Bitcoin (implementación simplificada)"""
        # En producción, usar biblioteca como python-bitcoinlib
        try:
            # Decodificar clave privada WIF
            private_key = self._wif_to_private_key(private_key_wif)
            
            # Aquí iría la lógica completa de firma
            # Por simplicidad, retornamos un placeholder
            return "signed_transaction_hex_placeholder"
            
        except Exception as e:
            print(f"Error firmando transacción: {e}")
            raise
    
    def _wif_to_private_key(self, wif: str) -> bytes:
        """Convertir formato WIF a clave privada"""
        # Decodificar Base58
        decoded = base58.b58decode_check(wif)
        
        # Remover byte de red
        if len(decoded) == 33:  # WIF comprimido
            return decoded[1:33]
        elif len(decoded) == 32:  # WIF no comprimido
            return decoded[1:33]
        else:
            return decoded[1:]
    
    def _calculate_txid(self, tx_hex: str) -> str:
        """Calcular TXID de transacción"""
        # Decodificar hex, hacer double SHA256, revertir bytes
        tx_bytes = bytes.fromhex(tx_hex)
        hash1 = hashlib.sha256(tx_bytes).digest()
        hash2 = hashlib.sha256(hash1).digest()
        return hash2[::-1].hex()
    
    def broadcast_transaction(self, signed_tx_hex: str) -> str:
        """Transmitir transacción a la red Bitcoin"""
        try:
            # Intentar con múltiples nodos
            for endpoint in self.node_endpoints:
                try:
                    response = requests.post(
                        f"{endpoint}tx", 
                        data=signed_tx_hex,
                        headers={'Content-Type': 'text/plain'},
                        timeout=30
                    )
                    if response.status_code == 200:
                        return response.text.strip()  # TXID
                except:
                    continue
            
            # Fallback a RPC
            result = self.rpc_call('sendrawtransaction', [signed_tx_hex])
            return result.get('result')
            
        except Exception as e:
            print(f"Error transmitiendo transacción: {e}")
            raise
    
    def get_transaction_status(self, txid: str) -> Dict:
        """Obtener estado de transacción"""
        try:
            for endpoint in self.node_endpoints:
                try:
                    response = requests.get(f"{endpoint}tx/{txid}", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        return {
                            'confirmed': data.get('status', {}).get('confirmed', False),
                            'block_height': data.get('status', {}).get('block_height'),
                            'confirmations': data.get('status', {}).get('confirmations', 0),
                            'timestamp': data.get('status', {}).get('block_time')
                        }
                except:
                    continue
            
            return {'confirmed': False, 'confirmations': 0}
            
        except Exception as e:
            print(f"Error obteniendo estado de transacción: {e}")
            return {'confirmed': False, 'confirmations': 0}
    
    def create_swap_to_vivcoin(self, btc_amount: Decimal, vivcoin_address: str) -> Dict:
        """Crear swap de Bitcoin a VivCoinORo"""
        try:
            # Generar dirección temporal para el swap
            swap_address = self.generate_new_address()
            
            swap_details = {
                'swap_id': f"btc_viv_{int(time.time())}",
                'btc_amount': float(btc_amount),
                'btc_address': swap_address,
                'vivcoin_address': vivcoin_address,
                'exchange_rate': self.get_exchange_rate(),
                'expiry_time': int(time.time()) + 3600,  # 1 hora
                'status': 'pending'
            }
            
            return swap_details
            
        except Exception as e:
            print(f"Error creando swap: {e}")
            raise
    
    def get_exchange_rate(self) -> float:
        """Obtener tasa de cambio BTC/VIV"""
        try:
            # Múltiples fuentes para el precio
            sources = [
                'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT',
                'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd',
                'https://api.bitfinex.com/v1/pubticker/btcusd'
            ]
            
            prices = []
            for source in sources:
                try:
                    response = requests.get(source, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if 'binance' in source:
                            prices.append(float(data['price']))
                        elif 'coingecko' in source:
                            prices.append(float(data['bitcoin']['usd']))
                        elif 'bitfinex' in source:
                            prices.append(float(data['last_price']))
                except:
                    continue
            
            if prices:
                avg_price = sum(prices) / len(prices)
                # Suponer 1 VIV = 1 USD para el ejemplo
                return 1.0 / avg_price
            else:
                return 0.000025  # Tasa por defecto (~40,000 USD/BTC)
                
        except Exception as e:
            print(f"Error obteniendo tasa de cambio: {e}")
            return 0.000025
    
    def generate_new_address(self) -> str:
        """Generar nueva dirección Bitcoin"""
        try:
            # Usar RPC para generar dirección
            result = self.rpc_call('getnewaddress', ['vivcoinoro', 'bech32'])
            return result.get('result')
        except:
            # Fallback: generar dirección offline (solo para testing)
            return self._generate_offline_address()
    
    def _generate_offline_address(self) -> str:
        """Generar dirección offline (solo para testing)"""
        # EN PRODUCCIÓN USAR BIBLIOTECAS SEGURAS
        import os
        private_key = os.urandom(32)
        
        # Calcular dirección (simplificado)
        # En producción usar python-bitcoinlib o similar
        return "bc1qtestaddressgeneratedoffline"
    
    def validate_address(self, address: str) -> bool:
        """Validar dirección Bitcoin"""
        try:
            result = self.rpc_call('validateaddress', [address])
            return result.get('result', {}).get('isvalid', False)
        except:
            # Validación básica offline
            return address.startswith(('1', '3', 'bc1'))
    
    def get_network_info(self) -> Dict:
        """Obtener información de la red Bitcoin"""
        try:
            result = self.rpc_call('getblockchaininfo')
            return result.get('result', {})
        except Exception as e:
            print(f"Error obteniendo info de red: {e}")
            return {}