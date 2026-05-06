import json
from web3 import Web3
from solcx import compile_source, install_solc
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import GANACHE_URL, ADMIN_PRIVATE_KEY, ADMIN_ADDRESS

# ── Connect to Ganache ──
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
assert w3.is_connected(), "❌ Cannot connect to Ganache"
print("✅ Connected to Ganache")

install_solc("0.8.26")

# ── Read contracts ──
with open("Library.sol") as f:
    library_src = f.read()

with open("LibraryCoin.sol") as f:
    coin_src = f.read()

# ── Compile ──
compiled_library = compile_source(library_src, solc_version="0.8.26", output_values=["abi", "bin"])
compiled_coin    = compile_source(coin_src,    solc_version="0.8.26", output_values=["abi", "bin"])

_, library_data = list(compiled_library.items())[0]
_, coin_data    = list(compiled_coin.items())[0]

# ── Save ABI ──
os.makedirs("abi", exist_ok=True)
with open("abi/LibraryRegistry.json", "w") as f:
    json.dump(library_data["abi"], f, indent=2)
with open("abi/LibraryCoin.json", "w") as f:
    json.dump(coin_data["abi"], f, indent=2)
print("✅ ABI saved")

# ── Deploy Library ──
Library = w3.eth.contract(abi=library_data["abi"], bytecode=library_data["bin"])
tx1 = Library.constructor().build_transaction({
    "from": ADMIN_ADDRESS,
    "nonce": w3.eth.get_transaction_count(ADMIN_ADDRESS),
    "gas": 3000000,
})
signed1  = w3.eth.account.sign_transaction(tx1, ADMIN_PRIVATE_KEY)
receipt1 = w3.eth.wait_for_transaction_receipt(w3.eth.send_raw_transaction(signed1.raw_transaction))
library_address = receipt1.contractAddress
print(f"✅ Library deployed at: {library_address}")

# ── Deploy LibraryCoin ──
Coin = w3.eth.contract(abi=coin_data["abi"], bytecode=coin_data["bin"])
tx2 = Coin.constructor().build_transaction({
    "from": ADMIN_ADDRESS,
    "nonce": w3.eth.get_transaction_count(ADMIN_ADDRESS),
    "gas": 3000000,
})
signed2  = w3.eth.account.sign_transaction(tx2, ADMIN_PRIVATE_KEY)
receipt2 = w3.eth.wait_for_transaction_receipt(w3.eth.send_raw_transaction(signed2.raw_transaction))
coin_address = receipt2.contractAddress
print(f"✅ LibraryCoin deployed at: {coin_address}")

# ── Seed 3 books ──
library_contract = w3.eth.contract(address=library_address, abi=library_data["abi"])

books = [
    (1, "The Great Gatsby"),
    (2, "1984"),
    (3, "To Kill a Mockingbird"),
]

for book_id, title in books:
    tx = library_contract.functions.addBook(book_id, title).build_transaction({
        "from": ADMIN_ADDRESS,
        "nonce": w3.eth.get_transaction_count(ADMIN_ADDRESS),
        "gas": 200000,
    })
    signed  = w3.eth.account.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    w3.eth.wait_for_transaction_receipt(w3.eth.send_raw_transaction(signed.raw_transaction))
    print(f"📚 Book added: {title}")

# ── Update settings.py ──
settings_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "settings.py")
with open(settings_path, "r") as f:
    content = f.read()

content = content.replace('REGISTRY_CONTRACT_ADDRESS = ""', f'REGISTRY_CONTRACT_ADDRESS = "{library_address}"')
content = content.replace('COIN_CONTRACT_ADDRESS = ""',     f'COIN_CONTRACT_ADDRESS = "{coin_address}"')

with open(settings_path, "w") as f:
    f.write(content)

print("\n Deploy complete!")
print(f"   Library  → {library_address}")
print(f"   Coin     → {coin_address}")