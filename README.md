# 📚 Campus Library Book Registry

> A blockchain-backed library system where every book loan and return is permanently logged on-chain and cannot be disputed.

Built with **Solidity**, **Ganache**, and **web3.py** as part of the *Technologies of Cryptocurrencies* course final project.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [How to Run](#how-to-run)
- [Security & Monitoring](#security--monitoring) ⭐ **NEW**
- [Roles](#roles)
- [Smart Contracts](#smart-contracts)
- [Team](#team)

---

## Overview

The Campus Library Book Registry is a decentralized application (DApp) that replaces a traditional library management system with a transparent, tamper-proof blockchain solution. Every book addition, loan, and return is recorded as an on-chain transaction — no record can be altered or deleted after the fact.

The system issues a custom ERC-20 token called **Library Coin (LBRC)** which can be distributed to users as a reward mechanism. All sensitive operations are restricted to the Admin role via Solidity access control.

---

## Features

### Admin
- Add single or batch library books to the registry
- Mint and distribute Library Coin (LBRC) to users
- View a full system dashboard (total books, coins minted, top active users)
- Pause and resume all user-facing operations (emergency stop)
- Transfer admin ownership to another address

### Normal User
- Browse available books and check their loan status
- Borrow and return books via signed transactions
- Register a display name tied to their wallet address
- View personal activity history (all past borrows/returns)
- Check Library Coin and ETH balance for any address

### System & Background
- Automated security tests (onlyOwner access control verification)
- Live alert monitor — prints an alert whenever a book is borrowed or returned
- Data history report — most borrowed books table generated from chain history
- Balance snapshot exporter — CSV of all account balances at any point in time
- Full system documentation and README

---

## Technologies Used

| Layer | Technology |
|---|---|
| Smart Contracts | Solidity ^0.8.0 |
| Local Blockchain | Ganache (ganache-cli) |
| Python Web3 Library | web3.py |
| Contract Compilation | solcx (py-solc-x) |
| Terminal Interface | Python 3 (built-in) |
| Token Standard | ERC-20 |
| Testing | Python unittest |
| Version Control | Git + GitHub |

---

## Project Structure

```
library_registry/
│
├── contracts/                     # Solidity smart contracts
│   ├── LibraryRegistry.sol        # Core contract: books, loans, access control
│   ├── LibraryCoin.sol            # ERC-20 Library Coin
│   └── interfaces/
│       └── IERC20.sol             # ERC-20 interface reference
│
├── scripts/                       # Python automation scripts
│   ├── deploy.py                  # Deploy contracts + seed sample data
│   ├── demo.py                    # ⭐ NEW: Complete demo guide (Member 5)
│   └── (additional scripts)
│
├── artifacts/
│   ├── Library.sol                # Core contract
│   ├── LibraryCoin.sol            # ERC-20 token
│   │
│   └── 📁 analytics/
│       ├── security_tests.py      # ⭐ NEW: Automated security tests (Member 5)
│       ├── live_alert_monitor.py  # ⭐ NEW: Real-time event monitoring (Member 5)
│       ├── integration_tests.py   # ⭐ NEW: End-to-end workflow tests (Member 5)
│       ├── admin_dashboard.py     # Admin statistics dashboard
│       ├── history_report.py      # Borrow history report
│       └── personal_history.py    # User activity history
│
├── abi/
│   ├── Library.json               # Contract ABI
│   └── LibraryCoin.json           # Token ABI
│
├── config/
│   └── settings.py                # Ganache URL, deployed addresses, admin key
│
├── tests/
│   └── test_security.py           # Unittest for access control
│
├── docs/
│   └── user_manual.md             # Plain-English usage guide
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### Prerequisites

Make sure the following are installed on your machine:

- Python 3.9 or higher
- Node.js (required for Ganache)
- Ganache CLI

```bash
# Install Ganache globally
npm install -g ganache
```

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/library_registry.git
cd library_registry
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Ganache

Open a new terminal window and run:

```bash
ganache --deterministic --accounts 10 --port 8545
```

The `--deterministic` flag ensures the same accounts are generated every run. Copy the **first account's private key** — this will be your Admin key.

### 5. Configure settings

Open `config/settings.py` and fill in:

```python
GANACHE_URL = "http://127.0.0.1:7545"
ADMIN_PRIVATE_KEY = "0x..."   # Paste first account's private key here
ADMIN_ADDRESS = "0x..."       # Paste first account's address here

# These are filled in automatically after deploy.py runs:
REGISTRY_CONTRACT_ADDRESS = ""
COIN_CONTRACT_ADDRESS = ""
```

### 6. Deploy the contracts

```bash
python scripts/deploy.py
```

This compiles both contracts, deploys them to Ganache, seeds 3 sample books, and saves the deployed addresses to `config/settings.py`.

---

## How to Run

### Start the terminal app

```bash
python app/main.py
```

You will see the main menu. New users are prompted to register a display name on first use.

### Run the admin dashboard

```bash
python scripts/admin_dashboard.py
```

### Start the live alert monitor (run in a separate terminal)

```bash
python scripts/alert_monitor.py
```

### Run the security test

```bash
python scripts/security_test.py
```

### Export a balance snapshot to CSV

```bash
python scripts/balance_snapshot.py
```

### Generate the data history report

```bash
python scripts/data_history_report.py
```

---

## Security & Monitoring

### 🔒 Security Overview

The Campus Library Book Registry implements multi-layered security controls:

1. **Smart Contract Access Control** — onlyOwner modifier restricts sensitive operations
2. **Emergency Pause System** — Admin can immediately halt all user operations
3. **Event Logging** — All transactions logged immutably on-chain
4. **Automated Testing** — Comprehensive security test suite validates all controls
5. **Real-Time Monitoring** — Live alert system detects anomalies instantly
6. **Integration Testing** — End-to-end workflows verify system integrity

### ✅ Security Test Suite

Run the automated security tests to verify all access controls are functioning:

```bash
python artifacts/analytics/security_tests.py
```

**Test Coverage (9 tests across 5 groups):**

**[GROUP 1] Access Control** — Verify onlyOwner restrictions
- Only owner can add books
- Only owner can pause/resume  
- Only owner can transfer ownership

**[GROUP 2] Pause/Resume** — Verify emergency stop functionality
- Pause prevents borrow operations
- Resume restores normal operations

**[GROUP 3] Input Validation** — Verify boundary conditions
- Empty strings rejected in user registration
- Duplicate user registration handled correctly

**[GROUP 4] Event Logging** — Verify audit trail
- Events properly logged for user registration

**[GROUP 5] Coin Security** — Verify token access control
- Only admin can mint coins
- Zero-amount transfers rejected

**Expected Output:**
```
✓ PASS - TEST 1.1: Only owner can add books
✓ PASS - TEST 1.2: Only owner can pause/resume
✓ PASS - TEST 1.3: Only owner can transfer ownership
✓ PASS - TEST 2.1: Pause prevents borrow operations
✓ PASS - TEST 3.1: Empty strings are rejected
✓ PASS - TEST 3.2: User registration validation works
✓ PASS - TEST 4.1: Events are logged for audit trail
✓ PASS - TEST 5.1: Only admin can mint coins
✓ PASS - TEST 5.2: Zero-amount transfers are rejected

═══════════════════════════════════════════════════════════════
TEST SUMMARY
═══════════════════════════════════════════════════════════════
Total Tests:  9
Passed:       9
Failed:       0
Pass Rate:    100.0%

✓ ALL TESTS PASSED - SYSTEM SECURE
```

### 🚨 Live Alert Monitoring

Start the real-time event monitor in a separate terminal:

```bash
python artifacts/analytics/live_alert_monitor.py
```

The monitor watches for the following events:

| Event | Trigger | Alert Color |
|---|---|---|
| **BookBorrowed** | User borrows book | 🔵 Blue |
| **BookReturned** | User returns book | 🟢 Green |
| **UserRegistered** | New user registers | 🟢 Green |
| **OwnershipTransferred** | Admin ownership changes | 🔴 Red |
| **Paused** | System enters pause mode | 🔴 Red |
| **Resumed** | System resumes operation | 🟢 Green |
| **BookAdded** | New book added by admin | 🔵 Cyan |

**Live Monitor Output Example:**
```
[14:23:45] BORROW EVENT
  📚 Book ID: 1
  👤 User: 0x398137a...
  🔗 TxHash: 0x5d42b8fa...

[14:23:52] USER REGISTRATION
  👤 User: 0x398137a...
  📝 Name: Alice Smith
  🔗 TxHash: 0x8c91dd2...

───────────────────────────────────────────────────────────────
EVENT STATISTICS:
  📚 Books Borrowed: 2
  📚 Books Returned: 1
  👤 Users Registered: 1
  👑 Ownership Transfers: 0
  ⏸️  Pause Events: 0
  ▶️  Resume Events: 0
  📊 Total Events: 4
```

**Tips for Live Monitoring:**
- Open in a dedicated terminal window
- Leave running during end-to-end testing
- Verify event details match transactions
- Use to catch real-time anomalies

### 🧪 Integration Testing

Run complete end-to-end workflow tests:

```bash
python artifacts/analytics/integration_tests.py
```

**Workflow Coverage:**

**[WORKFLOW 1] User Onboarding** — Registration → Coin Distribution → Balance Verification
- User registers with display name
- Admin mints coins to user
- User has both ETH and LBRC

**[WORKFLOW 2] Borrow & Return** — Add Book → Borrow → Mark Unavailable → Return → Mark Available
- Admin adds test book
- User borrows book (book availability decreases)
- User returns book (book availability increases)

**[WORKFLOW 3] Admin Operations** — Add Books → Mint Coins → Pause/Resume
- Admin batch-adds books
- Admin mints coins to multiple users
- Admin pauses contract (operations blocked)
- Admin resumes contract (operations enabled)

**[WORKFLOW 4] Multi-User Activity** — Concurrent Borrowing
- Multiple users register simultaneously
- Each user borrows different book
- System handles concurrent operations

**[WORKFLOW 5] Activity History** — Event Queryability & Data Integrity
- Verify activity history queryable from blockchain
- Confirm event data includes all required fields

**Expected Pass Rate:** 100% (all workflows complete successfully)

### 🔐 Security Checklist

Before deploying to production, verify:

**Access Control:**
- [ ] Only admin can call `addBook()`
- [ ] Only admin can call `mint()`
- [ ] Only admin can call `pause()` / `resume()`
- [ ] Non-admin calls revert with "onlyOwner" error
- [ ] Ownership transfer properly revokes old admin rights

**State Management:**
- [ ] `pause()` flag correctly blocks user operations
- [ ] `resume()` restores full functionality
- [ ] Emergency stop works instantly
- [ ] No operations possible during pause

**Event Logging:**
- [ ] All events emitted with correct parameters
- [ ] Event logs retained on-chain permanently
- [ ] Event history queryable by any address
- [ ] No duplicate event entries

**Data Integrity:**
- [ ] Book availability counts remain accurate
- [ ] User balances never go negative
- [ ] Coin supply controlled (only admin can mint)
- [ ] Transaction hashes unique and immutable

**Input Validation:**
- [ ] Empty strings rejected in registration
- [ ] Invalid book IDs handled gracefully
- [ ] Zero-amount transfers rejected
- [ ] Duplicate registrations handled

### ⚠️ Security Warnings

⚠️ **Private Key Management**
- Never commit private keys to version control
- Store `ADMIN_PRIVATE_KEY` in environment variables
- Rotate admin key regularly
- Use hardware wallet for mainnet

⚠️ **Gas Limits**
- Set appropriate gas limits to prevent runaway transactions
- Default gas limit in tests: 100,000
- Monitor gas usage for batch operations

⚠️ **Contract Upgrades**
- Current contracts are immutable (no proxy pattern)
- Bug fixes require redeployment with new address
- Users must manually migrate to new contract
- Plan for this in production deployment

⚠️ **Known Limitations**
- Ganache test blockchain resets on restart
- Test data not persisted between sessions
- See "Troubleshooting" section for recovery steps

### 🔧 Troubleshooting Security Issues

**Problem: "onlyOwner" revert on admin functions**
- [ ] Verify you're using the admin account
- [ ] Check private key in `api.txt` matches account 0
- [ ] Confirm Ganache is running with `--deterministic` flag

**Problem: Events not appearing in monitor**
- [ ] Ensure blockchain transactions completed (check receipt status)
- [ ] Verify contract address in `api.txt` is correct
- [ ] Check RPC endpoint URL in `config/settings.py`
- [ ] Restart monitor if events stuck

**Problem: Security tests failing**
- [ ] Run `python scripts/deploy.py` to redeploy contracts
- [ ] Verify Ganache running on correct port (8545)
- [ ] Check all accounts have sufficient ETH balance
- [ ] Review contract ABI in `abi/` folder

**Problem: Integration tests hanging**
- [ ] Increase test timeout (default 60 seconds)
- [ ] Check Ganache isn't out of gas
- [ ] Verify network connectivity to 127.0.0.1:8545
- [ ] Try restarting Ganache completely

---

## Roles

### Admin (Privileged User)

The Admin is the account that deployed the contracts (`msg.sender` in the constructor). All sensitive functions are protected by the `onlyOwner` modifier.

When running the terminal app, choose the **"Admin Login"** option and enter the admin private key or password when prompted. This unlocks the hidden admin menu.

**Admin capabilities:**
- Add / batch-add books
- Mint and distribute Library Coin
- Pause / resume the entire system
- Transfer admin ownership to a new address
- View the admin dashboard

### Normal User (Standard User)

Any other account on the network is a Normal User. They interact with books through the standard menu and cannot access any admin functions — attempts to do so will be reverted by the contract.

**User capabilities:**
- Register a display name
- Browse, borrow, and return books
- Check Library Coin and ETH balances
- View personal activity history

---

## Smart Contracts

### `LibraryRegistry.sol`

The core contract. Stores a `Book` struct (id, title, author, isAvailable) in a `mapping(uint => Book)`. Handles borrow/return logic, the `onlyOwner` and `whenNotPaused` modifiers, user registration, batch operations, pause/resume, and ownership transfer.

### `LibraryCoin.sol`

A minimal ERC-20 token (symbol: `LBRC`) where only the Admin can call `mint()`. Implements `name`, `symbol`, `totalSupply`, `balanceOf`, `transfer`, and emits a `Transfer` event on every token movement.

---

## Team

| Member | Role | Responsibilities |
|---|---|---|
| Member 1 | Blockchain Engineer | Core contract, access control, batch ops, pause, ownership transfer |
| Member 2 | Coin & Deployment | ERC-20 coin, deploy script, user registration (Solidity), balance CSV, README |
| Member 3 | Terminal App | Terminal app, transaction sender, registration (UI), balance checker |
| Member 4 | Data & Analytics | Admin dashboard, history report, activity history, ownership transfer test |
| **Member 5** | **Security & Monitoring** | **🔒 Automated security tests, 🚨 Live alert system, 🧪 Integration tests, 📋 Demo guide** |

### Member 5 - Security & Monitoring Deliverables

**1. Automated Security Tests** (`artifacts/analytics/security_tests.py`)
- 9 comprehensive security checks across 5 groups
- Access control verification (onlyOwner restrictions)
- Pause/resume functionality testing
- Input validation checks
- Event logging audit trail
- Coin minting security
- Automated PASS/FAIL reporting

**2. Live Alert System** (`artifacts/analytics/live_alert_monitor.py`)
- Real-time blockchain event monitoring
- Color-coded alerts for 6 event types
- Transaction hash verification
- Live event statistics
- Deduplication of duplicate alerts
- 2-second polling interval (configurable)

**3. Integration Testing** (`artifacts/analytics/integration_tests.py`)
- 5 complete end-to-end workflow tests
- User onboarding flow
- Borrow & return cycle
- Admin operations
- Multi-user concurrent activity
- Activity history & audit trail verification

**4. Setup & Demo Guide** (`scripts/demo.py`)
- Complete Ganache configuration instructions
- Step-by-step deployment guide
- Testing checklist & verification procedures
- Full workflow execution guide
- Project structure overview
- Security verification matrix

---

*Technologies of Cryptocurrencies — Final Project*
