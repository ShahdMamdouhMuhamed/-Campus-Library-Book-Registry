import json
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

# ====================== CONFIG ======================
RPC_URL = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(RPC_URL))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

LIBRARY_ADDRESS = "0x8CF9e90eD6b8489D957eabD45c9B586038d2d84B"
COIN_ADDRESS     ="0xf9d339FD278d051E7F4B9702054872dF7F1444a3"

# Load ABIs
def load_abi(name):
    with open(f'artifacts/{name}.json', 'r', encoding='utf-8') as f:
        abi = json.load(f)
        return abi if isinstance(abi, list) else abi.get('abi', abi)

library_abi = load_abi("Library")
coin_abi = load_abi("LibraryCoin")

library_contract = w3.eth.contract(address=LIBRARY_ADDRESS, abi=library_abi)
coin_contract = w3.eth.contract(address=COIN_ADDRESS, abi=coin_abi)

accounts = w3.eth.accounts
admin = accounts[0]

print("="*70)
print(" CAMPUS LIBRARY - AUTO SETUP")
print("="*70)

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

tx = library_contract.functions.batchAddBooks(book_ids, book_titles)
nonce = w3.eth.get_transaction_count(admin)
built_tx = tx.build_transaction({'from': admin, 'nonce': nonce, 'gas': 800000, 'gasPrice': w3.to_wei('20', 'gwei')})

tx_hash = w3.eth.send_transaction(built_tx)
w3.eth.wait_for_transaction_receipt(tx_hash)
print(f" {len(book_ids)} books added successfully!")

# ====================== MINT COINS ======================
print("\n Minting Library Coins...")

for i in range(1, 5):
    tx = coin_contract.functions.mint(accounts[i], 5000 * 10**18)
    nonce = w3.eth.get_transaction_count(admin)
    built_tx = tx.build_transaction({'from': admin, 'nonce': nonce, 'gas': 300000, 'gasPrice': w3.to_wei('20', 'gwei')})
    tx_hash = w3.eth.send_transaction(built_tx)
    w3.eth.wait_for_transaction_receipt(tx_hash)

print(" Coins minted to test accounts!")

# ====================== SUMMARY ======================
print("\n" + "="*70)
print(" SETUP FINISHED SUCCESSFULLY!")
print("="*70)
print(f"Library Contract : {LIBRARY_ADDRESS}")
print(f"LibraryCoin      : {COIN_ADDRESS}")
print(f"Total Books      : {library_contract.functions.totalBooks().call()}")
print(f"Total Supply     : {coin_contract.functions.totalSupply().call() / 10**18} LBRC")
print("\nYou can now run: python library_app.py")