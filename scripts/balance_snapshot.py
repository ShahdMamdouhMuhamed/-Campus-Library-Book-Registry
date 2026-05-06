import csv
import sys
import os
import json
from web3 import Web3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import GANACHE_URL, COIN_CONTRACT_ADDRESS

# ── Connect ──
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
assert w3.is_connected(), "❌ Cannot connect to Ganache"
print("✅ Connected to Ganache")

# ── Load ABI ──
with open("abi/LibraryCoin.json") as f:
    coin_abi = json.load(f)

coin = w3.eth.contract(address=COIN_CONTRACT_ADDRESS, abi=coin_abi)

# ── Get all accounts ──
accounts = w3.eth.accounts

# ── Build snapshot ──
rows = []
for account in accounts:
    eth_balance = w3.from_wei(w3.eth.get_balance(account), "ether")
    coin_balance = coin.functions.balanceOf(account).call()
    rows.append({
        "address": account,
        "eth_balance": round(float(eth_balance), 4),
        "coin_balance": coin_balance,
    })
    print(f"📊 {account} | ETH: {eth_balance:.4f} | LBRC: {coin_balance}")

# ── Write CSV ──
csv_path = "balance_snapshot.csv"
with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["address", "eth_balance", "coin_balance"])
    writer.writeheader()
    writer.writerows(rows)

print(f"\n✅ Snapshot saved to {csv_path}")