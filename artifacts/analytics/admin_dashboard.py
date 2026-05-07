import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from collections import Counter
from LibraryApp import w3, library_contract, coin_contract

print("\n========== ADMIN DASHBOARD ==========\n")

# Total Books
try:
    total_books = library_contract.functions.totalBooks().call()
    print(f"Total Books: {total_books}")
except Exception as e:
    print("Error reading total books:", e)

# Coin Supply
try:
    total_supply = coin_contract.functions.totalSupply().call()
    print(f"Total Library Coins Minted: {total_supply}")
except Exception as e:
    print("Error reading coin supply:", e)

# Current Admin
try:
    admin = library_contract.functions.getAdmin().call()
    print(f"Current Admin: {admin}")
except Exception as e:
    print("Error reading admin:", e)

# Pause Status
try:
    paused = library_contract.functions.paused().call()
    print(f"System Paused: {paused}")
except Exception as e:
    print("Error reading pause status:", e)

# Top Active Users
print("\n========== TOP ACTIVE USERS ==========\n")

try:
    borrow_events = library_contract.events.BookBorrowed.get_logs(
        from_block=0,
        to_block='latest'
    )

    user_counter = Counter()

    for event in borrow_events:
        user = event['args']['user']
        user_counter[user] += 1

    if len(user_counter) == 0:
        print("No borrowing activity found.")

    else:
        top_users = user_counter.most_common(3)

        for index, (user, count) in enumerate(top_users, start=1):
            print(f"{index}. {user} --> {count} borrows")

except Exception as e:
    print("Error reading events:", e)