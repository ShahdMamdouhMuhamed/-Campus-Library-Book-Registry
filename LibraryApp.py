import json
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

# ====================== CONFIG ======================
RPC_URL = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(RPC_URL))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

LIBRARY_ADDRESS = "0xCa8CAb5759707cFDCC0ce977388Ed7DbFEe211f6"
COIN_ADDRESS = "0x7FDFfe4F7E1Fe07c327c4909901bb94576cd499C"

# Load ABIs
def load_abi(name):
    try:
        with open(f'artifacts/{name}.json', 'r', encoding='utf-8') as f:
            abi = json.load(f)
            return abi if isinstance(abi, list) else abi.get('abi', abi)
    except:
        print(f" Cannot load {name}.json")
        return []

library_abi = load_abi("Library")
coin_abi = load_abi("LibraryCoin")

library_contract = w3.eth.contract(address=LIBRARY_ADDRESS, abi=library_abi)
coin_contract = w3.eth.contract(address=COIN_ADDRESS, abi=coin_abi)

# ====================== HELPERS ======================
def get_account():
    accounts = w3.eth.accounts
    print("\nAvailable Accounts:")
    for i, acc in enumerate(accounts):
        eth_bal = w3.from_wei(w3.eth.get_balance(acc), 'ether')
        print(f"{i+1}. {acc} ({eth_bal:.4f} ETH)")
    choice = int(input("\nSelect account number: ")) - 1
    return accounts[choice]

def send_tx(func, account):
    try:
        nonce = w3.eth.get_transaction_count(account)
        tx = func.build_transaction({
            'from': account,
            'nonce': nonce,
            'gas': 600000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        tx_hash = w3.eth.send_transaction(tx)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f" Success! Tx Hash: {tx_hash.hex()}")
        print(f"Block: {receipt.blockNumber}")
        return receipt
    except Exception as e:
        print(f" Transaction Failed: {e}")
        return None

# ====================== USER FUNCTIONS ======================
def register_user(account):
    name = input("Enter your full name: ").strip()
    if not name:
        print(" Name cannot be empty!")
        return
    try:
        send_tx(library_contract.functions.registerUser(name), account)
        print(" Registration successful!")
    except Exception as e:
        print(f" {e}")

def get_user_name(account):
    try:
        return library_contract.functions.users(account).call()
    except:
        return ""

def show_balances(address):
    try:
        eth_bal = w3.from_wei(w3.eth.get_balance(address), 'ether')
        coin_bal = coin_contract.functions.balanceOf(address).call() / 1e18
        print("\n" + "="*60)
        print(f"Address : {address}")
        print(f"ETH Balance     : {eth_bal:.4f} ETH")
        print(f"Library Coin    : {coin_bal:.2f} LBRC")
        print("="*60)
    except Exception as e:
        print(f" Error: {e}")

# ====================== ACTIVITY HISTORY ======================
def show_activity_history(address):
    print("\n Fetching Activity History...")
    print("="*80)
    print(f"{'Block':<8} {'Action':<20} {'Details':<40}")
    print("-"*80)

    count = 0
    latest_block = w3.eth.block_number

    for block_num in range(latest_block - 100, latest_block + 1):  # scan last 100 blocks
        if block_num < 0:
            continue
        try:
            block = w3.eth.get_block(block_num, full_transactions=True)
            for tx in block.transactions:
                if tx['to'] in [LIBRARY_ADDRESS.lower(), COIN_ADDRESS.lower()]:
                    try:
                        receipt = w3.eth.get_transaction_receipt(tx['hash'])
                        # Check events (simplified)
                        if receipt:
                            print(f"{block_num:<8} {'Transaction':<20} {tx['hash'].hex()[:20]}...")
                            count += 1
                    except:
                        pass
        except:
            pass
    
    if count == 0:
        print("No recent activity found for this address.")
    else:
        print(f"\n Found {count} transactions.")

# ====================== MAIN MENU ======================
def main():
    print("\n" + "="*70)
    print("  CAMPUS LIBRARY BOOK REGISTRY")
    print("="*70)

    account = get_account()
    user_name = get_user_name(account)

    if not user_name:
        print("\n Welcome new user! Please register first.")
        register_user(account)
        user_name = get_user_name(account)

    while True:
        print(f"\n👤 Logged in as: {user_name} ({account[:8]}...)")
        print("\n--- User Menu ---")
        print("1. Borrow Book")
        print("2. Return Book")
        print("3. Check My Balances")
        print("4. View My Activity History")   # ← Added
        print("5. Check Any Address Balances")
        print("6. List All Books")
        print("7. Admin Menu (Hidden)")
        print("0. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            book_id = int(input("Enter Book ID: "))
            try:
                send_tx(library_contract.functions.borrowBook(book_id), account)
            except Exception as e:
                print(f" {e}")

        elif choice == "2":
            book_id = int(input("Enter Book ID: "))
            try:
                send_tx(library_contract.functions.returnBook(book_id), account)
            except Exception as e:
                print(f" {e}")

        elif choice == "3":
            show_balances(account)

        elif choice == "4":
            show_activity_history(account)

        elif choice == "5":
            addr = input("Enter address: ").strip()
            show_balances(addr)

        elif choice == "6":
            total = library_contract.functions.totalBooks().call()
            print(f"\n Total Books: {total}")
            for i in range(1, total + 1):
                try:
                    book = library_contract.functions.books(i).call()
                    status = " Available" if book[1] else f" Borrowed by {book[2][:8]}..."
                    print(f"ID {i}: {book[0]} → {status}")
                except:
                    pass

        elif choice == "7":  # Admin Menu
            pwd = input("Enter Admin Password: ")
            if pwd != "admin123":
                print(" Access Denied!")
                continue
            print("\n🔑 ADMIN MENU")
            print("a. Add Single Book")
            print("b. Pause System")
            print("c. Resume System")
            sub = input("Choose: ").strip().lower()
            if sub == "a":
                bid = int(input("Book ID: "))
                title = input("Title: ")
                try:
                    send_tx(library_contract.functions.addBook(bid, title), account)
                except Exception as e:
                    print(e)

        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print(" Invalid choice!")

if __name__ == "__main__":
    if not w3.is_connected():
        print(" Cannot connect to Ganache. Make sure it's running.")
    else:
        main()