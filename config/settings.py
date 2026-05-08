import json
import os
from pathlib import Path

# ==================== GANACHE ====================
GANACHE_URL = os.getenv("GANACHE_URL", "http://127.0.0.1:7545")

# ==================== FILE PATHS ====================
PROJECT_ROOT = Path(__file__).parent.parent
LIBRARY_ABI_PATH = PROJECT_ROOT / "artifacts" / "Library.json"
COIN_ABI_PATH = PROJECT_ROOT / "artifacts" / "LibraryCoin.json"

# ==================== CONTRACT ADDRESSES ====================
# Load from api.txt (updated by deploy.py)
def load_addresses():
    api_file = PROJECT_ROOT / "api.txt"
    if api_file.exists():
        with open(api_file, 'r') as f:
            lines = f.readlines()
            addresses = {}
            for line in lines:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    addresses[key.strip()] = value.strip()
            return addresses
    return {}

_addresses = load_addresses()
LIBRARY_ADDRESS = _addresses.get('LIBRARY_ADDRESS', '0x0000000000000000000000000000000000000000')
COIN_ADDRESS = _addresses.get('COIN_ADDRESS', '0x0000000000000000000000000000000000000000')
REGISTRY_CONTRACT_ADDRESS = LIBRARY_ADDRESS
COIN_CONTRACT_ADDRESS = COIN_ADDRESS

# ==================== ADMIN ACCOUNT ====================
ADMIN_ADDRESS = os.getenv("ADMIN_ADDRESS", "0x0000000000000000000000000000000000000000")
ADMIN_PRIVATE_KEY = os.getenv("ADMIN_PRIVATE_KEY", "0x...")  # Set via environment if needed


CONTRACT_ADDRESSES = {
    "Library": LIBRARY_ADDRESS,
    "LibraryCoin": COIN_ADDRESS,
    "admin": ADMIN_ADDRESS,
}