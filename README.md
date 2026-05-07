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
│   ├── admin_dashboard.py         # Print system summary from blockchain
│   ├── data_history_report.py     # Most-borrowed books report
│   ├── balance_snapshot.py        # Export all balances to CSV
│   ├── alert_monitor.py           # Live background alert system
│   ├── security_test.py           # Automated onlyOwner revert test
│   └── ownership_transfer_test.py # Transfer ownership + re-test script
│
├── app/                           # Terminal application
│   ├── main.py                    # Entry point
│   ├── menu.py                    # Menu loop + admin gate
│   ├── tx_sender.py               # Transaction wrappers (send + receipt)
│   ├── user_profile.py            # Registration + activity history
│   └── balance_checker.py         # Coin & ETH balance display
│
├── abi/                           # Auto-generated after deployment (do not edit)
│   ├── LibraryRegistry.json
│   └── LibraryCoin.json
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
GANACHE_URL = "http://127.0.0.1:8545"
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
| Member 5 | Security & Monitoring | Security tests, live alert monitor, integration tests, demo prep |

---

*Technologies of Cryptocurrencies — Final Project*
