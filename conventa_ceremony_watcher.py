#!/usr/bin/env python3
"""
Conventa Ceremony File Watcher
Purpose: Monitor conventa_entries and red_shield directories for changes
         and automatically process new ceremony entries
Author: Seedbringer Directive / Euystacio AI System
"""

import os
import time
import signal
import sys
from pathlib import Path
from datetime import datetime
from conventa_ceremony_automator import ConventaCeremonyAutomator

class CeremonyFileWatcher:
    def __init__(self, check_interval=30):
        self.automator = ConventaCeremonyAutomator()
        self.check_interval = check_interval
        self.running = True
        self.last_check_time = datetime.now()
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\nReceived signal {signum}. Shutting down ceremony file watcher...")
        self.running = False
    
    def log_event(self, message):
        """Log events with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def check_for_changes(self):
        """Check for new ceremony entries and process them"""
        try:
            new_entries = self.automator.detect_new_entries()
            
            if new_entries:
                self.log_event(f"Detected {len(new_entries)} new ceremony entries")
                
                processed_records = []
                for entry_file in new_entries:
                    try:
                        ceremony_record = self.automator.create_ceremony_record(entry_file)
                        if ceremony_record:
                            self.automator.log_ceremony_event(ceremony_record)
                            self.automator.integrate_with_sync_ledger(ceremony_record)
                            processed_records.append(ceremony_record)
                            self.log_event(f"Processed: {ceremony_record['event']} by {ceremony_record['performer']}")
                    except Exception as e:
                        self.log_event(f"Error processing {entry_file}: {e}")
                
                if processed_records:
                    # Generate transparency report after processing
                    self.automator.generate_transparency_report()
                    self.log_event(f"Updated transparency report with {len(processed_records)} new records")
            
        except Exception as e:
            self.log_event(f"Error during change detection: {e}")
    
    def watch(self):
        """Main watching loop"""
        self.log_event("Starting Conventa ceremony file watcher...")
        self.log_event(f"Monitoring {self.automator.conventa_dir} and {self.automator.red_shield_dir}")
        self.log_event(f"Check interval: {self.check_interval} seconds")
        
        try:
            while self.running:
                self.check_for_changes()
                
                # Sleep in small increments to allow for graceful shutdown
                sleep_count = 0
                while sleep_count < self.check_interval and self.running:
                    time.sleep(1)
                    sleep_count += 1
                    
        except KeyboardInterrupt:
            self.log_event("Received keyboard interrupt")
        except Exception as e:
            self.log_event(f"Unexpected error: {e}")
        finally:
            self.log_event("Ceremony file watcher stopped")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Conventa Ceremony File Watcher")
    parser.add_argument(
        '--interval', 
        type=int, 
        default=30,
        help='Check interval in seconds (default: 30)'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit (no continuous monitoring)'
    )
    
    args = parser.parse_args()
    
    if args.once:
        # Run once and exit
        print("Running ceremony automation once...")
        automator = ConventaCeremonyAutomator()
        processed_records = automator.process_all_new_entries()
        if processed_records:
            print(f"Processed {len(processed_records)} ceremony records")
            for record in processed_records:
                print(f"- {record['event']} by {record['performer']}")
        else:
            print("No new ceremony entries found")
    else:
        # Run continuous monitoring
        watcher = CeremonyFileWatcher(check_interval=args.interval)
        watcher.watch()

if __name__ == "__main__":
    main()