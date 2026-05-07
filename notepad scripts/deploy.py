import json
from web3 import Web3

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Test connection
if not w3.is_connected():
    print("❌ Cannot connect to Ganache. Make sure it's running on port 7545")
    exit(1)

print(f"✅ Connected to Ganache")
print(f"Chain ID: {w3.eth.chain_id}")
print(f"First account: {w3.eth.accounts[0]}")

# Load contract artifacts
try:
    with open('artifacts/LibraryCoin.json', 'r') as f:
        coin_data = json.load(f)
    coin_abi = coin_data['abi']
    coin_bytecode = coin_data['bytecode']
    print("✅ Loaded LibraryCoin.json")
except Exception as e:
    print(f"❌ Error loading LibraryCoin.json: {e}")
    exit(1)

try:
    with open('artifacts/Library.json', 'r') as f:
        library_data = json.load(f)
    library_abi = library_data['abi']
    library_bytecode = library_data['bytecode']
    print("✅ Loaded Library.json")
except Exception as e:
    print(f"❌ Error loading Library.json: {e}")
    exit(1)

# Deploy LibraryCoin first
accounts = w3.eth.accounts
admin = accounts[0]
nonce = w3.eth.get_transaction_count(admin)

print(f"\n🚀 Deploying LibraryCoin from {admin}...")
coin_contract = w3.eth.contract(abi=coin_abi, bytecode=coin_bytecode)
tx_hash = coin_contract.constructor().transact({'from': admin, 'nonce': nonce})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
coin_address = tx_receipt.contractAddress
print(f"✅ LibraryCoin deployed at: {coin_address}")

# Deploy Library
nonce = w3.eth.get_transaction_count(admin)
print(f"\n🚀 Deploying Library from {admin}...")
library_contract = w3.eth.contract(abi=library_abi, bytecode=library_bytecode)
tx_hash = library_contract.constructor(coin_address).transact({'from': admin, 'nonce': nonce})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
library_address = tx_receipt.contractAddress
print(f"✅ Library deployed at: {library_address}")

# Save addresses
addresses = {
    'LibraryCoin': coin_address,
    'Library': library_address
}
with open('artifacts/deployed_addresses.json', 'w') as f:
    json.dump(addresses, f, indent=2)

print("\n" + "="*50)
print("✅ DEPLOYMENT COMPLETE!")
print("="*50)
print(f"Library: {library_address}")
print(f"LibraryCoin: {coin_address}")
print("\n📝 Update autosetup.py with these addresses")