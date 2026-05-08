import json
from web3 import Web3
from solcx import compile_source, install_solc

# ============================================
# CONNECT TO GANACHE
# ============================================

GANACHE_URL = "http://127.0.0.1:7545"

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

assert w3.is_connected(), " Cannot connect to Ganache"

print(" Connected to Ganache")

# ============================================
# INSTALL SOLIDITY COMPILER
# ============================================

install_solc("0.8.19")
print(" Solidity 0.8.19 installed")


# ============================================
# READ CONTRACT FILES
# ============================================

with open("artifacts/Library.sol", "r", encoding="utf-8") as f:
    library_source = f.read()

with open("artifacts/LibraryCoin.sol", "r", encoding="utf-8") as f:
    coin_source = f.read()

print(" Contract sources loaded")

# ============================================
# COMPILE CONTRACTS
# ============================================

try:
    compiled_library = compile_source(
        library_source,
        solc_version="0.8.19",
        optimize_runs=200
    )
    print(" Library.sol compiled successfully")
except Exception as e:
    print(f" Error compiling Library.sol: {e}")
    raise

try:
    compiled_coin = compile_source(
        coin_source,
        solc_version="0.8.19",
        optimize_runs=200
    )
    print(" LibraryCoin.sol compiled successfully")
except Exception as e:
    print(f" Error compiling LibraryCoin.sol: {e}")
    raise

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

try:
    tx_hash = Library.constructor().transact({
        'from': account,
        'gas': 6000000,
        'gasPrice': w3.eth.gas_price
    })
    print(f" Library deployment tx: {tx_hash.hex()}")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
except Exception as e:
    print(f" Error deploying Library contract: {e}")
    raise

library_address = tx_receipt.contractAddress

print(f" Library deployed at: {library_address}")

# ============================================
# DEPLOY LIBRARY COIN CONTRACT
# ============================================

Coin = w3.eth.contract(
    abi=coin_interface['abi'],
    bytecode=coin_interface['bin']
)

try:
    tx_hash = Coin.constructor().transact({
        'from': account,
        'gas': 6000000,
        'gasPrice': w3.eth.gas_price
    })
    print(f" LibraryCoin deployment tx: {tx_hash.hex()}")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
except Exception as e:
    print(f" Error deploying LibraryCoin contract: {e}")
    raise

coin_address = tx_receipt.contractAddress

print(f" LibraryCoin deployed at: {coin_address}")

# ============================================
# SAVE ADDRESSES
# ============================================

with open("api.txt", "w") as f:

    f.write(f"LIBRARY_ADDRESS={library_address}\n")
    f.write(f"COIN_ADDRESS={coin_address}\n")

print(" Addresses saved to api.txt")

print("\nDEPLOYMENT COMPLETE ")