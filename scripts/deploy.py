import json
from web3 import Web3
from solcx import compile_source, install_solc

# ============================================
# CONNECT TO GANACHE
# ============================================

GANACHE_URL = "http://127.0.0.1:8545"

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

assert w3.is_connected(), " Cannot connect to Ganache"

print(" Connected to Ganache")

# ============================================
# INSTALL SOLIDITY COMPILER
# ============================================

install_solc("0.8.20")

# ============================================
# READ CONTRACT FILES
# ============================================

with open("artifacts/Library.sol", "r", encoding="utf-8") as f:
    library_source = f.read()

with open("artifacts/LibraryCoin.sol", "r", encoding="utf-8") as f:
    coin_source = f.read()

# ============================================
# COMPILE CONTRACTS
# ============================================

compiled_library = compile_source(
    library_source,
    solc_version="0.8.20"
)

compiled_coin = compile_source(
    coin_source,
    solc_version="0.8.20"
)

# ============================================
# GET CONTRACT INTERFACES
# ============================================

library_interface = compiled_library['<stdin>:Library']
coin_interface = compiled_coin['<stdin>:LibraryCoin']

# ============================================
# SAVE ABI FILES
# ============================================

with open("artifacts/Library.json", "w") as f:
    json.dump({
        "abi": library_interface['abi']
    }, f, indent=4)

with open("artifacts/LibraryCoin.json", "w") as f:
    json.dump({
        "abi": coin_interface['abi']
    }, f, indent=4)

print(" ABI saved")

# ============================================
# ADMIN ACCOUNT
# ============================================

account = w3.eth.accounts[0]

print(f" Using account: {account}")

# ============================================
# DEPLOY LIBRARY CONTRACT
# ============================================

Library = w3.eth.contract(
    abi=library_interface['abi'],
    bytecode=library_interface['bin']
)

tx_hash = Library.constructor().transact({
    'from': account,
    'gas': 5000000
})

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

library_address = tx_receipt.contractAddress

print(f" Library deployed at: {library_address}")

# ============================================
# DEPLOY LIBRARY COIN CONTRACT
# ============================================

Coin = w3.eth.contract(
    abi=coin_interface['abi'],
    bytecode=coin_interface['bin']
)

tx_hash2 = Coin.constructor().transact({
    'from': account,
    'gas': 5000000
})

tx_receipt2 = w3.eth.wait_for_transaction_receipt(tx_hash2)

coin_address = tx_receipt2.contractAddress

print(f" Coin deployed at: {coin_address}")

# ============================================
# SAVE ADDRESSES
# ============================================

with open("api.txt", "w") as f:

    f.write(f"LIBRARY_ADDRESS={library_address}\n")
    f.write(f"COIN_ADDRESS={coin_address}\n")

print(" Addresses saved to api.txt")

print("\nDEPLOYMENT COMPLETE ")