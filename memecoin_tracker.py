import requests
import csv
from datetime import datetime

# Liste des réseaux à surveiller
NETWORKS = ["solana", "ethereum", "bsc", "base"]

def get_memecoin_data():
    all_data = []
    for network in NETWORKS:
        url = f"https://api.dexscreener.com/latest/dex/tokens?chain={network}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for token in data.get("pairs", []):
                if "pepe" in token["baseToken"]["symbol"].lower() or "doge" in token["baseToken"]["symbol"].lower():
                    all_data.append({
                        "network": network,
                        "token": token["baseToken"]["symbol"],
                        "price": token["priceUsd"],
                        "volume_24h": token.get("volume", {}).get("h24"),
                        "txns_24h": token.get("txns", {}).get("h24"),
                        "liquidity_usd": token.get("liquidity", {}).get("usd")
                    })
    return all_data

def save_to_csv(data):
    filename = f"memecoin_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Données sauvegardées dans {filename}")

if __name__ == "__main__":
    data = get_memecoin_data()
    if data:
        save_to_csv(data)
    else:
        print("❌ Aucune donnée trouvée.")
