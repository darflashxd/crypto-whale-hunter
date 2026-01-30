import requests

def send_discord_alert(webhook_url, tx_data):
    symbol = tx_data.get('symbol', 'ETH')
    amount = tx_data['value']
    
    # Format angka: Jika USDT ($), pakai 2 desimal. Jika Token lain, pakai integer rapi.
    if symbol == "USDT" or symbol == "USDC":
        amount_str = f"$ {amount:,.2f}"
    else:
        amount_str = f"{amount:,.0f} {symbol}"

    embed = {
        "title": f"🚨 {symbol} WHALE DETECTED",
        "description": "Pergerakan besar terdeteksi on-chain.",
        "color": 0x00ff00, 
        "fields": [
            {"name": "Asset Value", "value": f"**{amount_str}**", "inline": True},
            {"name": "Block", "value": f"{tx_data['block']}", "inline": True},
            {"name": "From", "value": f"`{tx_data['from'][:10]}...`", "inline": True},
            {"name": "To", "value": f"`{tx_data['to'][:10]}...`", "inline": True},
            {"name": "Explorer", "value": f"[View Transaction](https://etherscan.io/tx/{tx_data['hash']})", "inline": False}
        ],
        "footer": {"text": "Multi-Token Intel System v2"}
    }

    try:
        requests.post(webhook_url, json={"embeds": [embed]})
    except Exception as e:
        print(f"Webhook Error: {e}")