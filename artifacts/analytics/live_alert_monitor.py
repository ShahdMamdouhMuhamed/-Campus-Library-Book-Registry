"""
MEMBER 5 - SECURITY & MONITORING
Live Event Alert System for Campus Library Book Registry
Monitors: Book Borrowed, Book Returned, User Registration, Ownership Transfer, Pause/Resume
Real-time polling with color-coded notifications
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from threading import Thread, Event
from web3 import Web3

sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import GANACHE_URL, LIBRARY_ABI_PATH, LIBRARY_ADDRESS

# Color codes
RESET = '\033[0m'
BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BLUE = '\033[94m'

class LiveAlertMonitor:
    def __init__(self, poll_interval=2):
        """
        Initialize the live alert monitor
        poll_interval: seconds between blockchain checks
        """
        self.web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
        self.poll_interval = poll_interval
        self.running = False
        self.stop_event = Event()
        
        # Load contract ABI
        with open(LIBRARY_ABI_PATH) as f:
            abi_data = json.load(f)
            library_abi = abi_data if isinstance(abi_data, list) else abi_data.get('abi', abi_data)
        
        # Get library address from config
        self.library_address = LIBRARY_ADDRESS
        self.library = self.web3.eth.contract(address=self.library_address, abi=library_abi)
        
        # Track processed events
        self.processed_events = set()
        self.last_block = None
        self.event_counts = {
            'borrowed': 0,
            'returned': 0,
            'registered': 0,
            'ownership_transferred': 0,
            'paused': 0,
            'resumed': 0
        }
        
        self.print_header()

    def print_header(self):
        """Print system header"""
        print(f"\n{BOLD}{CYAN}{'='*80}")
        print(f"  LIVE EVENT ALERT SYSTEM - Campus Library Book Registry")
        print(f"  Real-time Blockchain Monitoring")
        print(f"{'='*80}{RESET}\n")
        print(f"Library Contract: {self.library_address}")
        print(f"RPC Endpoint: {GANACHE_URL}")
        print(f"Poll Interval: {self.poll_interval} seconds")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n{MAGENTA}Listening for events... (Press Ctrl+C to stop){RESET}\n")
        print(f"{BOLD}{'─'*80}{RESET}\n")

    def get_event_signature(self, event_name, event_data):
        """Create unique signature for event"""
        return f"{event_name}_{event_data.get('transactionHash')}_{event_data.get('logIndex')}"

    def format_alert(self, event_type, event_data):
        """Format event as alert message"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        if event_type == 'BookBorrowed':
            user = event_data['args']['user']
            book_id = event_data['args']['bookId']
            return (
                f"{BLUE}[{timestamp}] BORROW EVENT{RESET}\n"
                f"  📚 Book ID: {book_id}\n"
                f"  👤 User: {user}\n"
                f"  🔗 TxHash: {event_data['transactionHash'].hex()[:16]}..."
            )
        
        elif event_type == 'BookReturned':
            user = event_data['args']['user']
            book_id = event_data['args']['bookId']
            return (
                f"{GREEN}[{timestamp}] RETURN EVENT{RESET}\n"
                f"  📚 Book ID: {book_id}\n"
                f"  👤 User: {user}\n"
                f"  🔗 TxHash: {event_data['transactionHash'].hex()[:16]}..."
            )
        
        elif event_type == 'UserRegistered':
            user = event_data['args']['user']
            name = event_data['args'].get('name', 'Unknown')
            return (
                f"{GREEN}[{timestamp}] USER REGISTRATION{RESET}\n"
                f"  👤 User: {user}\n"
                f"  📝 Name: {name}\n"
                f"  🔗 TxHash: {event_data['transactionHash'].hex()[:16]}..."
            )
        
        elif event_type == 'OwnershipTransferred':
            old_owner = event_data['args'].get('previousOwner', 'Unknown')
            new_owner = event_data['args']['newOwner']
            return (
                f"{RED}[{timestamp}] OWNERSHIP TRANSFER{RESET}\n"
                f"  👑 Previous Owner: {old_owner[:10]}...\n"
                f"  👑 New Owner: {new_owner[:10]}...\n"
                f"  🔗 TxHash: {event_data['transactionHash'].hex()[:16]}..."
            )
        
        elif event_type == 'Paused':
            return (
                f"{RED}[{timestamp}] EMERGENCY PAUSE{RESET}\n"
                f"  ⚠️  System has been paused\n"
                f"  🔗 TxHash: {event_data['transactionHash'].hex()[:16]}..."
            )
        
        elif event_type == 'Resumed':
            return (
                f"{GREEN}[{timestamp}] SYSTEM RESUMED{RESET}\n"
                f"  ✓ System is now operational\n"
                f"  🔗 TxHash: {event_data['transactionHash'].hex()[:16]}..."
            )
        
        elif event_type == 'BookAdded':
            title = event_data['args'].get('title', 'Unknown')
            book_id = event_data['args']['bookId']
            return (
                f"{CYAN}[{timestamp}] NEW BOOK ADDED{RESET}\n"
                f"  📚 Book ID: {book_id}\n"
                f"  📖 Title: {title}\n"
                f"  🔗 TxHash: {event_data['transactionHash'].hex()[:16]}..."
            )

    def check_events(self):
        """Check for new events since last check"""
        try:
            current_block = self.web3.eth.block_number
            
            if self.last_block is None:
                self.last_block = max(0, current_block - 10)  # Start from last 10 blocks
            
            # Get all events since last check
            events_found = False
            
            # Check BookBorrowed events
            try:
                borrow_events = self.library.events.BookBorrowed.get_logs(
                    from_block=self.last_block,
                    to_block=current_block
                )
                for event in borrow_events:
                    sig = self.get_event_signature('BookBorrowed', event)
                    if sig not in self.processed_events:
                        self.processed_events.add(sig)
                        print(self.format_alert('BookBorrowed', event))
                        print()
                        self.event_counts['borrowed'] += 1
                        events_found = True
            except Exception:
                pass
            
            # Check BookReturned events
            try:
                return_events = self.library.events.BookReturned.get_logs(
                    from_block=self.last_block,
                    to_block=current_block
                )
                for event in return_events:
                    sig = self.get_event_signature('BookReturned', event)
                    if sig not in self.processed_events:
                        self.processed_events.add(sig)
                        print(self.format_alert('BookReturned', event))
                        print()
                        self.event_counts['returned'] += 1
                        events_found = True
            except Exception:
                pass
            
            # Check UserRegistered events
            try:
                register_events = self.library.events.UserRegistered.get_logs(
                    from_block=self.last_block,
                    to_block=current_block
                )
                for event in register_events:
                    sig = self.get_event_signature('UserRegistered', event)
                    if sig not in self.processed_events:
                        self.processed_events.add(sig)
                        print(self.format_alert('UserRegistered', event))
                        print()
                        self.event_counts['registered'] += 1
                        events_found = True
            except Exception:
                pass
            
            # Check OwnershipTransferred events
            try:
                ownership_events = self.library.events.OwnershipTransferred.get_logs(
                    from_block=self.last_block,
                    to_block=current_block
                )
                for event in ownership_events:
                    sig = self.get_event_signature('OwnershipTransferred', event)
                    if sig not in self.processed_events:
                        self.processed_events.add(sig)
                        print(self.format_alert('OwnershipTransferred', event))
                        print()
                        self.event_counts['ownership_transferred'] += 1
                        events_found = True
            except Exception:
                pass
            
            # Check Paused events
            try:
                pause_events = self.library.events.Paused.get_logs(
                    from_block=self.last_block,
                    to_block=current_block
                )
                for event in pause_events:
                    sig = self.get_event_signature('Paused', event)
                    if sig not in self.processed_events:
                        self.processed_events.add(sig)
                        print(self.format_alert('Paused', event))
                        print()
                        self.event_counts['paused'] += 1
                        events_found = True
            except Exception:
                pass
            
            # Check Resumed events
            try:
                resume_events = self.library.events.Resumed.get_logs(
                    from_block=self.last_block,
                    to_block=current_block
                )
                for event in resume_events:
                    sig = self.get_event_signature('Resumed', event)
                    if sig not in self.processed_events:
                        self.processed_events.add(sig)
                        print(self.format_alert('Resumed', event))
                        print()
                        self.event_counts['resumed'] += 1
                        events_found = True
            except Exception:
                pass
            
            # Check BookAdded events
            try:
                book_events = self.library.events.BookAdded.get_logs(
                    from_block=self.last_block,
                    to_block=current_block
                )
                for event in book_events:
                    sig = self.get_event_signature('BookAdded', event)
                    if sig not in self.processed_events:
                        self.processed_events.add(sig)
                        print(self.format_alert('BookAdded', event))
                        print()
                        events_found = True
            except Exception:
                pass
            
            self.last_block = current_block
            
            # Print status line
            if not events_found:
                status_time = datetime.now().strftime('%H:%M:%S')
                print(f"{YELLOW}[{status_time}] No new events • Blocks: {self.last_block}{RESET}", end='\r')
        
        except Exception as e:
            print(f"{RED}Error checking events: {e}{RESET}")

    def print_stats(self):
        """Print event statistics"""
        total = sum(self.event_counts.values())
        print(f"\n{BOLD}{'─'*80}{RESET}")
        print(f"EVENT STATISTICS:")
        print(f"  📚 Books Borrowed: {self.event_counts['borrowed']}")
        print(f"  📚 Books Returned: {self.event_counts['returned']}")
        print(f"  👤 Users Registered: {self.event_counts['registered']}")
        print(f"  👑 Ownership Transfers: {self.event_counts['ownership_transferred']}")
        print(f"  ⏸️  Pause Events: {self.event_counts['paused']}")
        print(f"  ▶️  Resume Events: {self.event_counts['resumed']}")
        print(f"  📊 Total Events: {total}")
        print(f"Stopped: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{BOLD}{'─'*80}\n{RESET}")

    def run(self):
        """Start monitoring (blocking)"""
        self.running = True
        try:
            while self.running and not self.stop_event.is_set():
                self.check_events()
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop monitoring gracefully"""
        print("\n")
        self.running = False
        self.stop_event.set()
        self.print_stats()


def main():
    monitor = LiveAlertMonitor(poll_interval=2)
    try:
        monitor.run()
    except KeyboardInterrupt:
        monitor.stop()
    except Exception as e:
        print(f"{RED}Fatal error: {e}{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
