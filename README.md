Berikut adalah **file lengkapnya** (gabungan dari bagian atas yang kamu kirim, ditambah panduan instalasi dan cara pakai).

Saya sudah merapikan struktur foldernya agar sesuai dengan kodingan aslimu (di mana `tokens.json` ada di folder utama, bukan di folder `config` yang belum kita buat).

Tinggal copy **semua** blok kode di bawah ini, lalu paste ke `nano README.md`.

```markdown
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
├── src/                # Source code modules
│   ├── api_client.py   # Etherscan V2 Wrapper
│   ├── analyzer.py     # Logic for Whale Detection & Math
│   └── notifier.py     # Discord Embed Builder
├── main.py             # Application Entry Point
├── tokens.json         # Watchlist Database
├── .env                # API Keys (Not included in repo)
├── .gitignore          # Git exclusion rules
└── requirements.txt    # Python Dependencies

```

## 🚀 Installation

1. **Clone the Repository**
```bash
git clone [https://github.com/darflashxd/crypto-whale-hunter.git](https://github.com/darflashxd/crypto-whale-hunter.git)
cd crypto-whale-hunter

```


2. **Set Up Virtual Environment**
```bash
python -m venv venv
# Linux/MacOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

```


3. **Install Dependencies**
```bash
pip install -r requirements.txt

```



## ⚙️ Configuration

### 1. Environment Variables

Create a `.env` file in the root directory and add your credentials:

```env
ETHERSCAN_API_KEY=YourEtherscanKey
DISCORD_WEBHOOK_URL=YourDiscordWebhookUrl

```

### 2. Token Watchlist (`tokens.json`)

Edit `tokens.json` to define which tokens to track.
**Example:**

```json
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

```

## 🏃 Usage

Run the main script:

```bash
python main.py

```

You will see logs in your terminal indicating that the system is scanning blocks. When a transaction exceeding your defined `threshold` occurs, you will receive a Discord notification immediately.

## 📖 How to Read Alerts

* **Inflow to Exchange (e.g., To: Binance):** 🔴 **Potential Dump.** Whale is moving funds to an exchange, likely to sell.
* **Outflow to Wallet (e.g., From: Binance):** 🟢 **Accumulation.** Whale is withdrawing funds to cold storage. Bullish signal.
* **Wallet to Wallet:** ⚪ **Neutral.** OTC deals or internal transfers.

## ⚠️ Disclaimer

This tool is for educational purposes only. On-chain data does not guarantee market movements. **Do Your Own Research (DYOR)** before trading.

---

