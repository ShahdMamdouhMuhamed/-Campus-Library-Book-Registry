import json
import csv
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

# ====================== CONFIG ======================
RPC_URL = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(RPC_URL))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

LIBRARY_ADDRESS = "0xd8b934580fcE35a11B58C6D73aDeE468a2833fa8"
COIN_ADDRESS     = "0xf8e81D47203A594245E36C48e151709F0C19fBe8"

# Load ABIs
def load_abi(name):
    with open(f'artifacts/{name}.json', 'r', encoding='utf-8') as f:
        abi = json.load(f)
        return abi if isinstance(abi, list) else abi.get('abi', abi)

coin_abi = load_abi("LibraryCoin")
coin_contract = w3.eth.contract(address=COIN_ADDRESS, abi=coin_abi)

print("="*60)
print(" BALANCE SNAPSHOT EXPORTER")
print("="*60)

accounts = w3.eth.accounts
snapshot = []

print("Scanning accounts...")

for acc in accounts:
    try:
        eth_bal = w3.from_wei(w3.eth.get_balance(acc), 'ether')
        coin_bal = coin_contract.functions.balanceOf(acc).call() / (10 ** 18)

        snapshot.append({
            'address': acc,
            'eth_balance': round(float(eth_bal), 4),
            'coin_balance': round(float(coin_bal), 2)
        })

        print(f"✓ {acc[:8]}... | ETH: {eth_bal:.4f} | LBRC: {coin_bal:.2f}")
    except:
        pass

# Save to CSV
with open('balance_snapshot.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['address', 'eth_balance', 'coin_balance'])
    writer.writeheader()
    writer.writerows(snapshot)

print("\n Snapshot saved successfully to 'balance_snapshot.csv'")
print(f"Total accounts scanned: {len(snapshot)}")