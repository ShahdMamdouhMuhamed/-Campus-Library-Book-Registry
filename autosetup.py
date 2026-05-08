import json
import sys
import time
from pathlib import Path
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

# ====================== PATH SETUP ======================
sys.path.insert(0, str(Path(__file__).parent))
from config.settings import (
    GANACHE_URL,
    LIBRARY_ADDRESS,
    COIN_ADDRESS,
    LIBRARY_ABI_PATH,
    COIN_ABI_PATH
)

# ====================== CONNECTION ======================
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

if not w3.is_connected():
    print(f"❌ Cannot connect to Ganache at {GANACHE_URL}")
    sys.exit(1)

# ====================== LOAD ABI ======================
def load_abi(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, list) else data.get("abi", data)

library_abi = load_abi(LIBRARY_ABI_PATH)
coin_abi = load_abi(COIN_ABI_PATH)

# ====================== CONTRACTS ======================
library_contract = w3.eth.contract(address=LIBRARY_ADDRESS, abi=library_abi)
coin_contract = w3.eth.contract(address=COIN_ADDRESS, abi=coin_abi)

accounts = w3.eth.accounts
admin = accounts[0]

print("=" * 70)
print(" CAMPUS LIBRARY - AUTO SETUP")
print("=" * 70)

# ====================== ADD BOOKS ======================
print("\n📚 Adding Sample Books...")

book_ids = [1, 2, 3, 4, 5, 6]
book_titles = [
    "Introduction to Blockchain",
    "Python for Beginners",
    "Data Structures & Algorithms",
    "Database Management Systems",
    "Machine Learning Fundamentals",
    "Web Development with JavaScript"
]

try:
    tx = library_contract.functions.batchAddBooks(book_ids, book_titles)

    nonce = w3.eth.get_transaction_count(admin)
    built_tx = tx.build_transaction({
        "from": admin,
        "nonce": nonce,
        "gas": 800000,
        "gasPrice": w3.to_wei("20", "gwei")
    })

    tx_hash = w3.eth.send_transaction(built_tx)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f" {len(book_ids)} books added successfully!")

except Exception as e:
    print("❌ Error adding books:", e)

# ====================== MINT COINS ======================
print("\n Minting Library Coins...")

try:
    for i in range(1, 5):
        tx = coin_contract.functions.mint(
            accounts[i],
            5000 * 10**18
        )

        nonce = w3.eth.get_transaction_count(admin)
        built_tx = tx.build_transaction({
            "from": admin,
            "nonce": nonce,
            "gas": 300000,
            "gasPrice": w3.to_wei("20", "gwei")
        })

        tx_hash = w3.eth.send_transaction(built_tx)
        w3.eth.wait_for_transaction_receipt(tx_hash)

    print(" Coins minted successfully!")

except Exception as e:
    print("❌ Error minting coins:", e)

# ====================== SYNC BLOCKCHAIN ======================
print("\n Syncing blockchain state...")
time.sleep(1)

try:
    total_books = library_contract.functions.totalBooks().call()
except Exception as e:
    total_books = f"Error: {e}"

try:
    total_supply = coin_contract.functions.totalSupply().call() / 10**18
except Exception as e:
    total_supply = f"Error: {e}"

# ====================== SUMMARY ======================
print("\n" + "=" * 70)
print(" SETUP FINISHED SUCCESSFULLY!")
print("=" * 70)

print(f"Library Contract : {LIBRARY_ADDRESS}")
print(f"LibraryCoin      : {COIN_ADDRESS}")
print(f"Total Books      : {total_books}")
print(f"Total Supply     : {total_supply} LBRC")

print("\n You can now run: py LibraryApp.py")


