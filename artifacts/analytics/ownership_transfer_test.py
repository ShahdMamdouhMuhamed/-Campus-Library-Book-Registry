import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from LibraryApp import w3, library_contract

print("\n========== OWNERSHIP TRANSFER TEST ==========\n")

old_admin = w3.eth.accounts[0]
new_admin = w3.eth.accounts[1]

print(f"Old Admin: {old_admin}")
print(f"New Admin: {new_admin}")

# ---------------------------------------------------
# TEST OLD ADMIN ACCESS BEFORE TRANSFER
# ---------------------------------------------------

print("\n[1] Testing old admin access BEFORE transfer...")

try:

    tx = library_contract.functions.pause().transact({
        'from': old_admin
    })

    w3.eth.wait_for_transaction_receipt(tx)

    print("PASS: Old admin can pause contract.")

except Exception as e:

    print("FAIL:", e)

# Resume again for clean testing
try:

    tx = library_contract.functions.resume().transact({
        'from': old_admin
    })

    w3.eth.wait_for_transaction_receipt(tx)

except:
    pass

# ---------------------------------------------------
# TRANSFER OWNERSHIP
# ---------------------------------------------------

print("\n[2] Transferring ownership...")

try:

    tx = library_contract.functions.transferOwnership(
        new_admin
    ).transact({
        'from': old_admin
    })

    w3.eth.wait_for_transaction_receipt(tx)

    print("PASS: Ownership transferred.")

except Exception as e:

    print("FAIL:", e)

# ---------------------------------------------------
# TEST OLD ADMIN AFTER TRANSFER
# ---------------------------------------------------

print("\n[3] Testing OLD admin after transfer...")

try:

    tx = library_contract.functions.pause().transact({
        'from': old_admin
    })

    w3.eth.wait_for_transaction_receipt(tx)

    print("FAIL: Old admin still has access!")

except:

    print("PASS: Old admin access removed.")

# ---------------------------------------------------
# TEST NEW ADMIN ACCESS
# ---------------------------------------------------

print("\n[4] Testing NEW admin access...")

try:

    tx = library_contract.functions.pause().transact({
        'from': new_admin
    })

    w3.eth.wait_for_transaction_receipt(tx)

    print("PASS: New admin has access.")

except Exception as e:

    print("FAIL:", e)

# Resume again
try:

    tx = library_contract.functions.resume().transact({
        'from': new_admin
    })

    w3.eth.wait_for_transaction_receipt(tx)

except:
    pass

# ---------------------------------------------------
# VERIFY CURRENT ADMIN
# ---------------------------------------------------

print("\n[5] Verifying current admin...")

try:

    current_admin = library_contract.functions.getAdmin().call()

    print("Current Admin:", current_admin)

    if current_admin.lower() == new_admin.lower():
        print("PASS: Ownership updated correctly.")
    else:
        print("FAIL: Ownership mismatch.")

except Exception as e:

    print("FAIL:", e)

print("\n========== TEST COMPLETE ==========\n")