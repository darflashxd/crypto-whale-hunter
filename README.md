# 🐋 Multi-Token Crypto Whale Hunter (Etherscan V2)

A robust, non-custodial market intelligence tool designed to track "Whale" activities (large transactions) across the Ethereum network in real-time. Built with the new **Etherscan API V2** standard.

> **Status:** Production Ready 🟢
> **Architecture:** Modular Service-Oriented (SOA)

## ✨ Key Features

* **🕵️ Multi-Token Tracking:** Monitors multiple assets simultaneously (e.g., USDT, PEPE, SHIB, LINK) in a single loop.
* **🧠 Smart Decimal Parsing:** Automatically handles mathematical differences between Stablecoins (6 decimals) and Standard Tokens (18 decimals).
* **⚡ Etherscan V2 Native:** Utilizes the latest unified API endpoints with robust error handling and exponential backoff strategies.
* **🔔 Rich Discord Alerts:** Sends clean, visual notifications with color-coded context and direct Etherscan links.
* **🛡️ Non-Custodial:** 100% Safe. Operates on a "Read-Only" basis. No Private Keys or Wallet connection required.

## 📂 Project Structure

```text
crypto-whale-hunter/
├── config/             # Configuration files
├── src/                # Source code
│   ├── api_client.py   # Etherscan V2 Wrapper
│   ├── analyzer.py     # Logic for Whale Detection & Math
│   └── notifier.py     # Discord Embed Builder
├── main.py             # Application Entry Point
├── tokens.json         # Watchlist Database
├── .env                # API Keys (Not included in repo)
└── requirements.txt    # Python Dependencies

🚀 Installation
Clone the Repository

Bash

git clone [https://github.com/YOUR_USERNAME/crypto-whale-hunter.git](https://github.com/YOUR_USERNAME/crypto-whale-hunter.git)
cd crypto-whale-hunter
Set Up Virtual Environment

Bash

python -m venv venv
# For Linux/Mac:
source venv/bin/activate
# For Windows:
# venv\Scripts\activate
Install Dependencies

Bash

pip install -r requirements.txt
⚙️ Configuration
1. Environment Variables
Create a .env file in the root directory and add your credentials:

Cuplikan kode

ETHERSCAN_API_KEY=YourEtherscanKeyHere
DISCORD_WEBHOOK_URL=YourDiscordWebhookUrlHere
2. Token Watchlist (tokens.json)
Edit tokens.json to define which tokens to track. You can add as many as you want.

Example:

JSON

[
    {
        "symbol": "USDT",
        "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "decimals": 6,
        "threshold": 500000
    },
    {
        "symbol": "SHIB",
        "address": "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
        "decimals": 18,
        "threshold": 1000000000
    }
]
🏃 Usage
Run the main script:

Bash

python main.py
You will see logs in your terminal indicating that the system is scanning blocks. When a transaction exceeding your defined threshold occurs, you will receive a Discord notification immediately.

📖 How to Read Alerts
Inflow to Exchange (e.g., To: Binance): 🔴 Potential Dump. Whale is moving funds to an exchange, likely to sell.

Outflow to Wallet (e.g., From: Binance): 🟢 Accumulation. Whale is withdrawing funds to cold storage. Bullish signal.

Wallet to Wallet: ⚪ Neutral. OTC deals or internal transfers.

⚠️ Disclaimer
This tool is for educational and informational purposes only. On-chain data does not guarantee market movements. Do Your Own Research (DYOR) before trading.
