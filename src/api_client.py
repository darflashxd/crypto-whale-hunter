import requests
import logging
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class EtherscanV2Client:
    def __init__(self, api_key, chain_id=1):
        self.api_key = api_key
        self.chain_id = chain_id
        self.base_url = "https://api.etherscan.io/v2/api"
        
        self.session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1, 
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        self.logger = logging.getLogger("EtherscanClient")

    def _make_request(self, module, action, **kwargs):
        params = {
            'module': module,
            'action': action,
            'apikey': self.api_key,
            'chainid': self.chain_id,
            **kwargs
        }

        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Handler khusus untuk Proxy (JSON-RPC)
            if module == 'proxy':
                if 'error' in data:
                    raise ValueError(f"JSON-RPC Error: {data['error']}")
                return data['result']

            # Handler Standar V2
            if 'status' in data and data['status'] != '1':
                if "No transactions found" in data['message'] or "No records found" in data['message']:
                    return []
                raise ValueError(f"API Error: {data['message']} - {data['result']}")
                
            return data['result']

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network Failure: {e}")
            raise

    def get_latest_block(self):
        res = self._make_request('proxy', 'eth_blockNumber')
        return int(res, 16)

    def get_normal_transactions(self, address, start_block):
        return self._make_request(
            module='account',
            action='txlist',
            address=address,
            startblock=start_block,
            endblock='latest',
            sort='asc'
        )

    # --- FITUR BARU: ERC-20 TRACKER ---
    def get_token_transfers(self, token_contract, start_block):
        """
        Mengambil log transfer token spesifik.
        Topic0 '0xddf...' adalah signature standar untuk event 'Transfer(address,address,uint256)'
        """
        return self._make_request(
            module='logs',
            action='getLogs',
            fromBlock=start_block,
            toBlock='latest',
            address=token_contract,
            topic0='0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef' 
        )