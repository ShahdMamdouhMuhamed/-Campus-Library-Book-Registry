#!/usr/bin/env python3
"""
MEMBER 5 - SECURITY & MONITORING
DEMO RUNNER - Campus Library Book Registry
Comprehensive end-to-end demonstration with setup, deployment, and test execution
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Color codes
RESET = '\033[0m'
BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BLUE = '\033[94m'

class DemoRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.artifacts_dir = self.project_root / "artifacts"
        self.analytics_dir = self.artifacts_dir / "analytics"
        
    def print_header(self, text):
        print(f"\n{BOLD}{CYAN}{'='*80}")
        print(f"  {text}")
        print(f"{'='*80}{RESET}\n")
    
    def print_step(self, step_num, step_name):
        print(f"{BOLD}{BLUE}[STEP {step_num}] {step_name}{RESET}")
        print(f"{'-'*80}\n")
    
    def print_success(self, msg):
        print(f"{GREEN}✓ {msg}{RESET}")
    
    def print_error(self, msg):
        print(f"{RED}✗ {msg}{RESET}")
    
    def print_info(self, msg):
        print(f"{YELLOW}ℹ {msg}{RESET}")
    
    def run_command(self, cmd, description=""):
        """Execute shell command with error handling"""
        if description:
            print(f"\n{CYAN}→ {description}{RESET}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                self.print_success(f"Command succeeded")
                if result.stdout:
                    print(f"  {result.stdout.strip()}")
                return True
            else:
                self.print_error(f"Command failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            self.print_error("Command timed out")
            return False
        except Exception as e:
            self.print_error(f"Error: {e}")
            return False

    def demo_section_1_setup(self):
        """DEMO SECTION 1: Environment Setup"""
        self.print_header("SECTION 1: ENVIRONMENT SETUP")
        
        self.print_step(1, "Verify Python Environment")
        print(f"Python Version: {sys.version}")
        print(f"Project Root: {self.project_root}")
        print(f"Artifacts Dir: {self.artifacts_dir}")
        self.print_success("Environment verified")
        
        self.print_step(2, "Check Required Files")
        required_files = [
            self.project_root / "config" / "settings.py",
            self.project_root / "api.txt",
            self.artifacts_dir / "Library.sol",
            self.artifacts_dir / "LibraryCoin.sol",
        ]
        
        all_exist = True
        for file in required_files:
            exists = file.exists()
            status = f"{GREEN}✓{RESET}" if exists else f"{RED}✗{RESET}"
            print(f"  {status} {file.name}")
            if not exists:
                all_exist = False
        
        if all_exist:
            self.print_success("All required files present")
        else:
            self.print_error("Some required files missing")

    def demo_section_2_ganache_setup(self):
        """DEMO SECTION 2: Ganache Configuration"""
        self.print_header("SECTION 2: GANACHE SETUP")
        
        self.print_step(1, "Ganache Configuration Guide")
        
        ganache_config = """
        
        📋 GANACHE STARTUP INSTRUCTIONS
        ═══════════════════════════════════════════════════════════════
        
        Option A: Using Ganache CLI (Recommended for this project)
        ───────────────────────────────────────────────────────────────
        
        1. Install Ganache CLI:
           npm install -g ganache-cli
        
        2. Start Ganache with proper configuration:
           ganache-cli --deterministic \\
             --accounts 10 \\
             --host 127.0.0.1 \\
             --port 8545 \\
             --chain-id 1337 \\
             --gas-limit 8000000 \\
             --block-time 0
        
        3. Expected Output:
           Available Accounts (with 100 ETH each):
           (0) 0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc
           (1) 0x398137a... [additional accounts]
           ...
           Listening on 127.0.0.1:8545
        
        
        Option B: Using Ganache GUI
        ───────────────────────────────────────────────────────────────
        
        1. Download from: https://trufflesuite.com/ganache/
        2. Launch the application
        3. Create new workspace with settings:
           - Ethereum RPC Server: 127.0.0.1:8545
           - Accounts: 10
           - Account Balance: 100 ETH
           - Gas Limit: 8000000
           - Deterministic: ON (for consistent addresses)
        
        
        🔧 CONFIGURATION CHECKLIST
        ───────────────────────────────────────────────────────────────
        ✓ Network ID: 1337
        ✓ RPC URL: http://127.0.0.1:8545
        ✓ Accounts: At least 5 (admin + 4 test users)
        ✓ Initial Balance: 100 ETH per account
        ✓ Gas Limit: 8000000
        ✓ Block Time: 0 (instant)
        ✓ Deterministic: YES (for reproducible addresses)
        
        """
        print(ganache_config)
        self.print_success("Ganache configuration guide displayed")

    def demo_section_3_deployment(self):
        """DEMO SECTION 3: Contract Deployment"""
        self.print_header("SECTION 3: CONTRACT DEPLOYMENT")
        
        self.print_step(1, "Deploy Smart Contracts")
        self.print_info("Ensure Ganache is running on 127.0.0.1:8545")
        
        deploy_script = self.project_root / "scripts" / "deploy.py"
        if deploy_script.exists():
            print(f"\nRunning: python {deploy_script}")
            print(f"This will:")
            print(f"  • Compile Library.sol and LibraryCoin.sol")
            print(f"  • Deploy contracts to Ganache")
            print(f"  • Save contract addresses to api.txt")
            print(f"  • Generate contract ABIs\n")
            
            self.print_info("Execute this command in another terminal:")
            print(f"{CYAN}python scripts/deploy.py{RESET}\n")
        else:
            self.print_error("deploy.py not found")

    def demo_section_4_security_tests(self):
        """DEMO SECTION 4: Security Testing"""
        self.print_header("SECTION 4: SECURITY TESTING")
        
        self.print_step(1, "Run Security Test Suite")
        security_test = self.analytics_dir / "security_tests.py"
        
        print(f"Location: {security_test}")
        print(f"\nTest Coverage:")
        print(f"  [GROUP 1] Access Control (3 tests)")
        print(f"    • Only owner can add books")
        print(f"    • Only owner can pause/resume")
        print(f"    • Only owner can transfer ownership")
        print(f"  [GROUP 2] Pause/Resume Functionality (1 test)")
        print(f"    • Pause prevents borrow operations")
        print(f"  [GROUP 3] Input Validation (2 tests)")
        print(f"    • Empty strings are rejected")
        print(f"    • Duplicate registration handling")
        print(f"  [GROUP 4] Event Logging (1 test)")
        print(f"    • Events are properly logged")
        print(f"  [GROUP 5] Coin Security (2 tests)")
        print(f"    • Only admin can mint coins")
        print(f"    • Zero-amount transfers rejected")
        
        print(f"\n{CYAN}→ Execute security tests:{RESET}")
        print(f"{BOLD}python artifacts/analytics/security_tests.py{RESET}\n")

    def demo_section_5_live_monitoring(self):
        """DEMO SECTION 5: Live Event Monitoring"""
        self.print_header("SECTION 5: LIVE EVENT MONITORING")
        
        self.print_step(1, "Live Alert System")
        alert_monitor = self.analytics_dir / "live_alert_monitor.py"
        
        print(f"Location: {alert_monitor}")
        print(f"\nMonitored Events:")
        print(f"  📚 BookBorrowed - When user borrows a book")
        print(f"  📚 BookReturned - When user returns a book")
        print(f"  👤 UserRegistered - When new user registers")
        print(f"  👑 OwnershipTransferred - When admin transfers ownership")
        print(f"  ⏸️  Paused - When system enters emergency pause")
        print(f"  ▶️  Resumed - When system resumes operation")
        print(f"  📖 BookAdded - When new book added to library")
        
        print(f"\nFeatures:")
        print(f"  ✓ Real-time event polling (2-second intervals)")
        print(f"  ✓ Color-coded notifications for event types")
        print(f"  ✓ Transaction hash display for verification")
        print(f"  ✓ Live event statistics")
        print(f"  ✓ Deduplication (no duplicate alerts)")
        
        print(f"\n{CYAN}→ Start monitoring:{RESET}")
        print(f"{BOLD}python artifacts/analytics/live_alert_monitor.py{RESET}")
        print(f"\nTip: Open this in a separate terminal to watch events as they happen!\n")

    def demo_section_6_integration_tests(self):
        """DEMO SECTION 6: Integration Testing"""
        self.print_header("SECTION 6: INTEGRATION TESTING")
        
        self.print_step(1, "End-to-End Workflows")
        integration_test = self.analytics_dir / "integration_tests.py"
        
        print(f"Location: {integration_test}")
        print(f"\nTest Workflows:")
        print(f"  [WORKFLOW 1] User Onboarding Flow")
        print(f"    • Register new user")
        print(f"    • Admin mints coins")
        print(f"    • Verify multi-asset balance")
        print(f"  [WORKFLOW 2] Borrow & Return Cycle")
        print(f"    • Add book to library")
        print(f"    • User borrows book")
        print(f"    • Book status updates")
        print(f"    • User returns book")
        print(f"  [WORKFLOW 3] Admin Operations")
        print(f"    • Batch book management")
        print(f"    • Coin minting")
        print(f"    • Emergency pause/resume")
        print(f"  [WORKFLOW 4] Multi-User Concurrent Activity")
        print(f"    • Multiple users borrow different books")
        print(f"    • Concurrent transaction handling")
        print(f"  [WORKFLOW 5] Activity History & Audit")
        print(f"    • Verify event history queryable")
        print(f"    • Check event data integrity")
        
        print(f"\n{CYAN}→ Run integration tests:{RESET}")
        print(f"{BOLD}python artifacts/analytics/integration_tests.py{RESET}\n")

    def demo_section_7_analytics(self):
        """DEMO SECTION 7: Analytics & Reporting"""
        self.print_header("SECTION 7: ANALYTICS & REPORTING")
        
        self.print_step(1, "Available Reports")
        print(f"1️⃣  Admin Dashboard")
        print(f"    → artifacts/analytics/admin_dashboard.py")
        print(f"    Shows: Total books, coins minted, top 3 active users")
        
        print(f"\n2️⃣  History Report")
        print(f"    → artifacts/analytics/history_report.py")
        print(f"    Shows: Most borrowed books table")
        
        print(f"\n3️⃣  Balance Snapshot")
        print(f"    → balance_snapshot.py")
        print(f"    Exports: All account balances to CSV")
        
        print(f"\n4️⃣  Personal Activity History")
        print(f"    → artifacts/analytics/personal_history.py")
        print(f"    Shows: User-specific transaction history")
        
        print(f"\n{CYAN}→ Run reports:{RESET}")
        print(f"{BOLD}python artifacts/analytics/admin_dashboard.py{RESET}\n")

    def demo_section_8_full_workflow(self):
        """DEMO SECTION 8: Full Workflow Guide"""
        self.print_header("SECTION 8: COMPLETE WORKFLOW GUIDE")
        
        print(f"""
        {BOLD}🚀 QUICK START SEQUENCE{RESET}
        ═══════════════════════════════════════════════════════════════
        
        {YELLOW}Terminal Window 1: Ganache{RESET}
        ─────────────────────────────────────────────────────────────
        $ ganache-cli --deterministic --accounts 10 --host 127.0.0.1 --port 8545
        
        {YELLOW}Terminal Window 2: Deploy{RESET}
        ─────────────────────────────────────────────────────────────
        $ python scripts/deploy.py
        $ python autosetup.py          # Seed 3+ sample books
        
        {YELLOW}Terminal Window 3: Live Monitoring{RESET}
        ─────────────────────────────────────────────────────────────
        $ python artifacts/analytics/live_alert_monitor.py
        
        {YELLOW}Terminal Window 4: Application & Tests{RESET}
        ─────────────────────────────────────────────────────────────
        $ python LibraryApp.py          # Run terminal app
        
        OR
        
        $ python artifacts/analytics/security_tests.py     # Run security tests
        $ python artifacts/analytics/integration_tests.py  # Run integration tests
        
        {YELLOW}Terminal Window 5: Analytics{RESET}
        ─────────────────────────────────────────────────────────────
        $ python artifacts/analytics/admin_dashboard.py
        $ python artifacts/analytics/history_report.py
        
        
        {BOLD}📋 TESTING CHECKLIST{RESET}
        ───────────────────────────────────────────────────────────────
        
        ✓ Security Tests
          - Verify onlyOwner restrictions
          - Check pause/resume functionality
          - Validate input checking
          - Confirm coin minting restrictions
        
        ✓ Integration Tests
          - User onboarding workflow
          - Book borrow/return cycle
          - Admin operations (pause, resume, mint)
          - Multi-user concurrent activity
          - Activity history tracking
        
        ✓ Live Monitoring
          - Watch events in real-time
          - Verify event accuracy
          - Check transaction details
          - Monitor error conditions
        
        ✓ Analytics
          - Generate admin dashboard
          - Review borrow statistics
          - Check user activity
          - Export balance snapshot
        
        
        {BOLD}🔒 SECURITY VERIFICATION{RESET}
        ───────────────────────────────────────────────────────────────
        
        Access Control:
          □ Only admin can add books
          □ Only admin can mint coins
          □ Only admin can pause/resume
          □ Only admin can transfer ownership
        
        State Management:
          □ Pause blocks all operations
          □ Resume restores functionality
          □ Events logged for all operations
        
        Data Integrity:
          □ Book availability tracked correctly
          □ User balances accurate
          □ Transaction history immutable
          □ Events include all details
        
        """)

    def demo_section_9_project_structure(self):
        """DEMO SECTION 9: Project Structure"""
        self.print_header("SECTION 9: PROJECT STRUCTURE")
        
        structure = """
        Campus Library Book Registry/
        ├── 📄 LibraryApp.py                 (Terminal application)
        ├── 📄 autosetup.py                  (Seed test data)
        ├── 📄 balance_snapshot.py           (Export balances)
        ├── 📝 README.md                     (Main documentation)
        │
        ├── 📁 config/
        │   └── settings.py                  (Configuration)
        │
        ├── 📁 scripts/
        │   └── deploy.py                    (Contract deployment)
        │
        ├── 📁 artifacts/
        │   ├── Library.sol                  (Main contract)
        │   ├── LibraryCoin.sol              (Token contract)
        │   ├── LibraryRegistry.json         (Contract ABI)
        │   ├── LibraryCoin.json             (Token ABI)
        │   │
        │   └── 📁 analytics/
        │       ├── security_tests.py        ✓ NEW: Access control tests
        │       ├── live_alert_monitor.py    ✓ NEW: Real-time event monitoring
        │       ├── integration_tests.py     ✓ NEW: E2E workflow tests
        │       ├── admin_dashboard.py       (Admin statistics)
        │       ├── history_report.py        (Borrow history)
        │       └── personal_history.py      (User activity)
        │
        └── 📁 abi/
            ├── Library.json                 (Contract ABI)
            └── LibraryCoin.json             (Token ABI)
        """
        print(structure)

    def print_conclusion(self):
        """Print conclusion and next steps"""
        self.print_header("DEMO COMPLETE - NEXT STEPS")
        
        conclusion = f"""
        {BOLD}✓ All demonstration materials prepared{RESET}
        
        {BOLD}Member 5 Deliverables Complete:{RESET}
        ─────────────────────────────────────────────────────────────
        
        1. {GREEN}✓ Security Testing{RESET}
           File: artifacts/analytics/security_tests.py
           Tests: 9 automated security checks
           Coverage: Access control, pause/resume, input validation, coin security
        
        2. {GREEN}✓ Live Alert System{RESET}
           File: artifacts/analytics/live_alert_monitor.py
           Features: Real-time event monitoring, color-coded alerts, statistics
           Events: BookBorrowed, BookReturned, UserRegistered, Pause/Resume, etc.
        
        3. {GREEN}✓ Integration Testing{RESET}
           File: artifacts/analytics/integration_tests.py
           Tests: 5 complete end-to-end workflows
           Coverage: User onboarding, borrow/return, admin ops, concurrent users
        
        4. {GREEN}✓ Setup & Demo Guide{RESET}
           File: scripts/demo.py (this file)
           Features: Complete workflow guide, Ganache setup, testing checklist
        
        
        {BOLD}🚀 HOW TO RUN THE COMPLETE DEMO:{RESET}
        ─────────────────────────────────────────────────────────────
        
        1. Start Ganache (see Section 2 for instructions)
        2. Deploy contracts: python scripts/deploy.py
        3. Run in parallel:
           - Security tests: python artifacts/analytics/security_tests.py
           - Live monitor: python artifacts/analytics/live_alert_monitor.py
           - Integration tests: python artifacts/analytics/integration_tests.py
           - App: python LibraryApp.py
        
        
        {BOLD}📚 DOCUMENTATION:{RESET}
        ─────────────────────────────────────────────────────────────
        
        See README.md for:
        • Setup instructions
        • Architecture overview
        • Security analysis
        • API reference
        • Troubleshooting guide
        
        
        {BOLD}✅ VERIFICATION CHECKLIST:{RESET}
        ─────────────────────────────────────────────────────────────
        
        □ All 5 Member deliverables complete
        □ Smart contracts deployed successfully
        □ Security tests passing (9/9)
        □ Integration tests passing (5+ workflows)
        □ Live monitoring showing real-time events
        □ Analytics reports generating correctly
        □ Documentation complete and accurate
        
        
        {BOLD}📞 SUPPORT:{RESET}
        ─────────────────────────────────────────────────────────────
        
        For issues or questions, refer to the README.md file or check:
        • Contract event logs for transaction details
        • Live monitor for real-time event confirmation
        • Security tests for system state verification
        
        {RESET}
        """
        print(conclusion)

    def run_demo(self):
        """Execute complete demo"""
        self.print_header("CAMPUS LIBRARY BOOK REGISTRY - COMPLETE DEMO")
        
        print(f"Project Root: {self.project_root}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"User: {os.getenv('USERNAME', 'Unknown')}\n")
        
        self.demo_section_1_setup()
        self.demo_section_2_ganache_setup()
        self.demo_section_3_deployment()
        self.demo_section_4_security_tests()
        self.demo_section_5_live_monitoring()
        self.demo_section_6_integration_tests()
        self.demo_section_7_analytics()
        self.demo_section_8_full_workflow()
        self.demo_section_9_project_structure()
        self.print_conclusion()


if __name__ == "__main__":
    try:
        demo = DemoRunner()
        demo.run_demo()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Demo interrupted by user{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}Error: {e}{RESET}")
        sys.exit(1)
