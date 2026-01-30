from decimal import Decimal
import logging

class WhaleAnalyzer:
    def __init__(self, threshold, decimals):
        self.threshold = Decimal(str(threshold))
        self.decimals = decimals 
        self.logger = logging.getLogger("Analyzer")

    def _parse_value(self, hex_value):
        # Handle jika data kosong atau 0x
        if not hex_value or hex_value == '0x':
            return Decimal(0)
        val = Decimal(int(hex_value, 16)) if isinstance(hex_value, str) else Decimal(hex_value)
        return val / (Decimal("10") ** self.decimals)

    def process_transactions(self, transactions, is_token=False, symbol="ETH"):
        alerts = []
        for tx in transactions:
            try:
                if is_token:
                    # Parsing Data Token
                    raw_value = tx.get('data', '0x0')
                    value_readable = self._parse_value(raw_value)
                    
                    if len(tx['topics']) < 3: continue # Skip jika log tidak lengkap

                    sender = "0x" + tx['topics'][1][26:] 
                    receiver = "0x" + tx['topics'][2][26:]
                    tx_hash = tx['transactionHash']
                    block = int(tx['blockNumber'], 16)
                else:
                    # Parsing ETH Native
                    value_readable = Decimal(tx['value']) / Decimal("10" ** 18)
                    sender = tx['from']
                    receiver = tx['to']
                    tx_hash = tx['hash']
                    block = tx['blockNumber']

                # Filter Threshold
                if value_readable >= self.threshold:
                    alerts.append({
                        'hash': tx_hash,
                        'from': sender,
                        'to': receiver,
                        'value': value_readable,
                        'block': block,
                        'symbol': symbol # Kirim simbol token ke Notifier
                    })
            except Exception as e:
                continue
        return alerts