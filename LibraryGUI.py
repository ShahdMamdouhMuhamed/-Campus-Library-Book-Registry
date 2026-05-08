# =========================================================
# CAMPUS LIBRARY BOOK REGISTRY GUI
# =========================================================

import customtkinter as ctk
from tkinter import messagebox
from web3 import Web3
import json
import os

# =========================================================
# APP STYLE
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =========================================================
# GANACHE CONNECTION
# =========================================================

GANACHE_URL = "http://127.0.0.1:7545"

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if not w3.is_connected():
    raise Exception("❌ Cannot connect to Ganache")

print("✅ Connected to Ganache")

# =========================================================
# FILE PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ABI_PATH = os.path.join(BASE_DIR, "artifacts", "Library.json")
API_PATH = os.path.join(BASE_DIR, "api.txt")

# =========================================================
# LOAD ABI
# =========================================================

with open(ABI_PATH, "r") as f:
    contract_json = json.load(f)

if isinstance(contract_json, dict):
    abi = contract_json["abi"]
else:
    abi = contract_json

print("✅ ABI Loaded")

# =========================================================
# LOAD CONTRACT ADDRESS
# =========================================================

with open(API_PATH, "r") as f:
    lines = f.readlines()

LIBRARY_ADDRESS = lines[0].split("=")[-1].strip()

print("✅ Contract Address Loaded")

# =========================================================
# CREATE CONTRACT
# =========================================================

library_contract = w3.eth.contract(
    address=Web3.to_checksum_address(LIBRARY_ADDRESS),
    abi=abi
)

print("✅ Contract Ready")

# =========================================================
# GUI SETTINGS
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =========================================================
# MAIN APP
# =========================================================

class LibraryGUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Campus Library Book Registry")
        self.geometry("1400x850")

        self.account = w3.eth.accounts[0]

        # =================================================
        # SIDEBAR
        # =================================================

        self.sidebar = ctk.CTkFrame(
            self,
            width=280,
            corner_radius=0
        )

        self.sidebar.pack(side="left", fill="y")

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="📚 CAMPUS LIBRARY",
            font=("Arial", 28, "bold")
        )

        self.logo.pack(pady=40)

        self.account_label = ctk.CTkLabel(
            self.sidebar,
            text=f"Connected Account:\n{self.account[:12]}...",
            font=("Arial", 16)
        )

        self.account_label.pack(pady=20)

        # =================================================
        # BUTTONS
        # =================================================

        self.borrow_btn = ctk.CTkButton(
            self.sidebar,
            text="Borrow Book",
            height=50,
            font=("Arial", 18),
            command=self.borrow_book
        )

        self.borrow_btn.pack(pady=15, padx=20, fill="x")

        self.return_btn = ctk.CTkButton(
            self.sidebar,
            text="Return Book",
            height=50,
            font=("Arial", 18),
            command=self.return_book
        )

        self.return_btn.pack(pady=15, padx=20, fill="x")

        self.list_btn = ctk.CTkButton(
            self.sidebar,
            text="List Books",
            height=50,
            font=("Arial", 18),
            command=self.list_books
        )

        self.list_btn.pack(pady=15, padx=20, fill="x")

        self.analytics_btn = ctk.CTkButton(
            self.sidebar,
            text="Analytics Dashboard",
            height=50,
            font=("Arial", 18),
            command=self.analytics_dashboard
        )

        self.analytics_btn.pack(pady=15, padx=20, fill="x")

        self.admin_btn = ctk.CTkButton(
            self.sidebar,
            text="Admin Panel",
            fg_color="#a00000",
            hover_color="#c00000",
            height=50,
            font=("Arial", 18),
            command=self.admin_panel
        )

        self.admin_btn.pack(pady=15, padx=20, fill="x")

        # =================================================
        # MAIN FRAME
        # =================================================

        self.main_frame = ctk.CTkFrame(self)

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Campus Library Book Registry",
            font=("Arial", 40, "bold")
        )

        self.title_label.pack(pady=30)

        self.subtitle = ctk.CTkLabel(
            self.main_frame,
            text="Blockchain-Based Library Management System",
            font=("Arial", 22)
        )

        self.subtitle.pack(pady=10)

        # =================================================
        # OUTPUT BOX
        # =================================================

        self.output_box = ctk.CTkTextbox(
            self.main_frame,
            width=900,
            height=500,
            font=("Consolas", 16)
        )

        self.output_box.pack(pady=30)

        self.log("✅ System Connected Successfully")
        self.log(f"👤 Current Account: {self.account}")

    # =====================================================
    # LOG
    # =====================================================

    def log(self, text):
        self.output_box.insert("end", text + "\n")
        self.output_box.see("end")

    # =====================================================
    # ADMIN PANEL
    # =====================================================

    def admin_panel(self):

        dialog = ctk.CTkInputDialog(
            text="Enter Admin Password",
            title="Admin Access"
        )

        password = dialog.get_input()

        if password != "admin123":
            messagebox.showerror("Denied", "Wrong Password")
            return

        win = ctk.CTkToplevel(self)

        win.geometry("450x350")
        win.title("Admin Panel")

        title = ctk.CTkLabel(
            win,
            text="Add Book",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=20)

        book_id_entry = ctk.CTkEntry(
            win,
            placeholder_text="Book ID",
            width=300,
            height=45
        )

        book_id_entry.pack(pady=15)

        title_entry = ctk.CTkEntry(
            win,
            placeholder_text="Book Title",
            width=300,
            height=45
        )

        title_entry.pack(pady=15)

        def add_book():

            try:

                book_id = int(book_id_entry.get())
                title = title_entry.get()

                tx_hash = library_contract.functions.addBook(
                    book_id,
                    title
                ).transact({
                    "from": self.account
                })

                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

                self.log(f"📚 Added Book: {title}")
                self.log(f"📦 Block: {receipt.blockNumber}")

                messagebox.showinfo(
                    "Success",
                    "Book Added Successfully"
                )

                win.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        btn = ctk.CTkButton(
            win,
            text="Add Book",
            height=45,
            command=add_book
        )

        btn.pack(pady=25)

    # =====================================================
    # BORROW BOOK
    # =====================================================

    def borrow_book(self):

        dialog = ctk.CTkInputDialog(
            text="Enter Book ID",
            title="Borrow Book"
        )

        try:

            book_id = int(dialog.get_input())

            tx_hash = library_contract.functions.borrowBook(
                book_id
            ).transact({
                "from": self.account
            })

            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            self.log(f"📕 Borrowed Book ID {book_id}")
            self.log(f"📦 Block: {receipt.blockNumber}")

            messagebox.showinfo(
                "Success",
                "Book Borrowed Successfully"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =====================================================
    # RETURN BOOK
    # =====================================================

    def return_book(self):

        dialog = ctk.CTkInputDialog(
            text="Enter Book ID",
            title="Return Book"
        )

        try:

            book_id = int(dialog.get_input())

            tx_hash = library_contract.functions.returnBook(
                book_id
            ).transact({
                "from": self.account
            })

            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            self.log(f"📗 Returned Book ID {book_id}")
            self.log(f"📦 Block: {receipt.blockNumber}")

            messagebox.showinfo(
                "Success",
                "Book Returned Successfully"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =====================================================
    # LIST BOOKS
    # =====================================================

    def list_books(self):

        self.output_box.delete("1.0", "end")

        try:

            self.log("========== ALL BOOKS ==========\n")

            found = False

            for i in range(1, 100):

                try:

                    book = library_contract.functions.books(i).call()

                    title = book[0]
                    available = book[1]

                    if len(title) > 0:

                        found = True

                        status = (
                            "✅ Available"
                            if available
                            else "❌ Borrowed"
                        )

                        self.log(f"📘 Book ID: {i}")
                        self.log(f"📖 Title: {title}")
                        self.log(f"📌 Status: {status}")
                        self.log("--------------------------------")

                except:
                    pass

            if not found:
                self.log("No books found.")

        except Exception as e:
            self.log(str(e))

    # =====================================================
    # ANALYTICS
    # =====================================================

    def analytics_dashboard(self):

        self.output_box.delete("1.0", "end")

        try:

            total_books = library_contract.functions.totalBooks().call()

            admin = library_contract.functions.getAdmin().call()

            paused = library_contract.functions.paused().call()

            self.log("========== ANALYTICS DASHBOARD ==========\n")

            self.log(f"📚 Total Books: {total_books}")
            self.log(f"👑 Admin: {admin}")
            self.log(f"⏸️ System Paused: {paused}")

            borrow_events = library_contract.events.BookBorrowed.get_logs(
                from_block=0,
                to_block="latest"
            )

            return_events = library_contract.events.BookReturned.get_logs(
                from_block=0,
                to_block="latest"
            )

            self.log(f"📕 Borrow Events: {len(borrow_events)}")
            self.log(f"📗 Return Events: {len(return_events)}")

        except Exception as e:
            self.log(str(e))

# =========================================================
# RUN APP
# =========================================================

app = LibraryGUI()
app.mainloop()