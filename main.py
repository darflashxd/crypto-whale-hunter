import time
import os
import json
import logging
from dotenv import load_dotenv
from src.api_client import EtherscanV2Client
from src.analyzer import WhaleAnalyzer
from src.notifier import send_discord_alert

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("MultiToken_Hunter")

load_dotenv()
API_KEY = os.getenv("ETHERSCAN_API_KEY")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def load_tokens():
    """Membaca konfigurasi dari file tokens.json"""
    try:
        with open('tokens.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.critical(f"Gagal membaca tokens.json: {e}")
        return []

def main():
    logger.info("--- MULTI-TOKEN WHALE HUNTER DIMULAI ---")
    
    tokens = load_tokens()
    if not tokens: return
    
    logger.info(f"Target Terpasang: {len(tokens)} Token")
    for t in tokens:
        logger.info(f"-> {t['symbol']} (Threshold: {t['threshold']:,})")

    client = EtherscanV2Client(API_KEY, chain_id=1)
    
    # Sinkronisasi Awal
    try:
        last_block = client.get_latest_block()
        logger.info(f"Start Block: {last_block}")
    except Exception as e:
        logger.critical(f"Koneksi Gagal: {e}")
        return

    try:
        while True:
            try:
                current_block = client.get_latest_block()
            except:
                time.sleep(5)
                continue

            if current_block > last_block:
                logger.info(f"⚡ Blok {current_block}: Memindai {len(tokens)} Token...")
                
                # --- LOOPING UNTUK SETIAP TOKEN ---
                for token in tokens:
                    try:
                        # 1. Ambil Log Transfer Spesifik Token Ini
                        logs = client.get_token_transfers(token['address'], last_block)
                        
                        # 2. Inisialisasi Analyzer sesuai spesifikasi token (Desimal & Threshold beda-beda)
                        analyzer = WhaleAnalyzer(
                            threshold=token['threshold'], 
                            decimals=token['decimals']
                        )
                        
                        # 3. Analisis dengan label Symbol yang benar
                        alerts = analyzer.process_transactions(
                            logs, 
                            is_token=True, 
                            symbol=token['symbol']
                        )
                        
                        if alerts:
                            logger.info(f"🚨 {token['symbol']}: Ditemukan {len(alerts)} Transaksi!")
                            for alert in alerts:
                                send_discord_alert(WEBHOOK_URL, alert)
                                time.sleep(0.5)
                                
                    except Exception as e:
                        logger.error(f"Skip {token['symbol']}: {e}")
                        
                    # Jeda sedikit antar token biar gak kena Rate Limit
                    time.sleep(0.2) 

                last_block = current_block
            
            # Interval antar blok
            time.sleep(10)

    except KeyboardInterrupt:
        logger.info("Sistem dimatikan.")

if __name__ == "__main__":
    main()