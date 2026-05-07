import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from collections import Counter
from LibraryApp import library_contract

print("\n========== MOST BORROWED BOOKS ==========\n")

try:
    borrow_events = library_contract.events.BookBorrowed.get_logs(
        from_block=0,
        to_block='latest'
    )

    books_counter = Counter()

    for event in borrow_events:
        book_id = event['args']['bookId']
        books_counter[book_id] += 1

    if len(books_counter) == 0:
        print("No borrow history found.")

    else:
        for book_id, count in books_counter.most_common():

            try:
                book = library_contract.functions.books(book_id).call()

                title = book[0]

            except:
                title = "Unknown Book"

            print(f"Book ID {book_id} | {title} --> borrowed {count} times")

except Exception as e:
    print("Error generating report:", e)