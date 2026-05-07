import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from datetime import datetime
from LibraryApp import w3, library_contract

user_address = input("Enter wallet address: ").strip()

print("\n========== USER ACTIVITY HISTORY ==========\n")

try:
    borrow_events = library_contract.events.BookBorrowed.get_logs(
        from_block=0,
        to_block='latest'
    )

    return_events = library_contract.events.BookReturned.get_logs(
        from_block=0,
        to_block='latest'
    )

    found = False

    # Borrow Events
    for event in borrow_events:

        user = event['args']['user']

        if user.lower() == user_address.lower():

            found = True

            book_id = event['args']['bookId']

            block = w3.eth.get_block(event['blockNumber'])

            timestamp = datetime.fromtimestamp(block['timestamp'])

            print(f"[BORROW]")
            print(f"Book ID: {book_id}")
            print(f"Block: {event['blockNumber']}")
            print(f"Time: {timestamp}")
            print("-" * 40)

    # Return Events
    for event in return_events:

        user = event['args']['user']

        if user.lower() == user_address.lower():

            found = True

            book_id = event['args']['bookId']

            block = w3.eth.get_block(event['blockNumber'])

            timestamp = datetime.fromtimestamp(block['timestamp'])

            print(f"[RETURN]")
            print(f"Book ID: {book_id}")
            print(f"Block: {event['blockNumber']}")
            print(f"Time: {timestamp}")
            print("-" * 40)

    if not found:
        print("No activity found for this address.")

except Exception as e:
    print("Error reading history:", e)