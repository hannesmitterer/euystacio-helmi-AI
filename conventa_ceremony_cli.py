#!/usr/bin/env python3
"""
Conventa Ceremony Management CLI
Purpose: Command-line interface for managing Conventa ceremony records,
         monitoring Red Seals, and maintaining transparency
Author: Seedbringer Directive / Euystacio AI System
"""

import argparse
import json
import sys
from pathlib import Path
from conventa_ceremony_automator import ConventaCeremonyAutomator

def status_command(args):
    """Show status of ceremony records and automation"""
    automator = ConventaCeremonyAutomator()
    
    print("=== CONVENTA CEREMONY STATUS ===")
    
    # Check for new entries
    new_entries = automator.detect_new_entries()
    print(f"New entries to process: {len(new_entries)}")
    
    if new_entries:
        print("New entries:")
        for entry in new_entries:
            print(f"  - {entry.name}")
    
    # Read ceremony ledger
    ceremony_ledger = automator.read_ceremony_ledger()
    print(f"Total ceremony records: {len(ceremony_ledger)}")
    
    # Statistics
    if ceremony_ledger:
        anchored = len([r for r in ceremony_ledger if r['anchoring_status'] == 'anchored'])
        pending = len([r for r in ceremony_ledger if r['anchoring_status'] == 'pending'])
        verified = len([r for r in ceremony_ledger if r['red_seal']['verified']])
        
        print(f"Anchored ceremonies: {anchored}")
        print(f"Pending ceremonies: {pending}")
        print(f"Verified Red Seals: {verified}")
    
    print("=== END STATUS ===")

def process_command(args):
    """Process new ceremony entries"""
    automator = ConventaCeremonyAutomator()
    
    if args.entry_file:
        # Process specific entry
        entry_path = Path(args.entry_file)
        if not entry_path.exists():
            print(f"Error: Entry file {entry_path} does not exist")
            return 1
            
        ceremony_record = automator.create_ceremony_record(entry_path)
        if ceremony_record:
            automator.log_ceremony_event(ceremony_record)
            automator.integrate_with_sync_ledger(ceremony_record)
            print(f"Processed ceremony: {ceremony_record['event']}")
        else:
            print(f"Failed to process entry: {entry_path}")
            return 1
    else:
        # Process all new entries
        processed_records = automator.process_all_new_entries()
        print(f"Processed {len(processed_records)} ceremony records")
    
    return 0

def list_command(args):
    """List ceremony records"""
    automator = ConventaCeremonyAutomator()
    ceremony_ledger = automator.read_ceremony_ledger()
    
    if not ceremony_ledger:
        print("No ceremony records found")
        return
    
    print("=== CEREMONY RECORDS ===")
    
    for record in ceremony_ledger:
        print(f"Record ID: {record['record_id']}")
        print(f"Event: {record['event']}")
        print(f"Performer: {record['performer']}")
        print(f"Ceremony Time: {record['ceremony_timestamp']}")
        print(f"Processing Time: {record['processing_timestamp']}")
        print(f"Anchoring Status: {record['anchoring_status']}")
        print(f"Red Seal Verified: {record['red_seal']['verified']}")
        print(f"Affirmation Status: {record['affirmation_status']}")
        
        if 'postscript' in record:
            print(f"Postscript: {record['postscript']['summary']}")
        
        print("-" * 40)

def verify_command(args):
    """Verify Red Seal integrity"""
    automator = ConventaCeremonyAutomator()
    
    if args.entry_file:
        # Verify specific entry
        entry_path = Path(args.entry_file)
        red_seal_info = automator.find_red_seal(entry_path.name)
        
        if not red_seal_info:
            print(f"No Red Seal found for {entry_path.name}")
            return 1
            
        verified = automator.verify_red_seal(entry_path, red_seal_info)
        print(f"Red Seal verification for {entry_path.name}: {'PASS' if verified else 'FAIL'}")
        print(f"Expected hash: {red_seal_info['seal_hash']}")
        
        if not verified:
            actual_hash = automator.calculate_file_sha256(entry_path)
            print(f"Actual hash: {actual_hash}")
            return 1
    else:
        # Verify all entries in ceremony ledger
        ceremony_ledger = automator.read_ceremony_ledger()
        failed_verifications = []
        
        for record in ceremony_ledger:
            entry_path = Path(record['entry_file'])
            if entry_path.exists():
                red_seal_info = automator.find_red_seal(entry_path.name)
                if red_seal_info:
                    verified = automator.verify_red_seal(entry_path, red_seal_info)
                    if not verified:
                        failed_verifications.append(record['record_id'])
                    print(f"{record['event']}: {'PASS' if verified else 'FAIL'}")
        
        if failed_verifications:
            print(f"\nFailed verifications: {len(failed_verifications)}")
            return 1
        else:
            print(f"\nAll {len(ceremony_ledger)} Red Seals verified successfully")
    
    return 0

def report_command(args):
    """Generate transparency report"""
    automator = ConventaCeremonyAutomator()
    report = automator.generate_transparency_report()
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to {args.output}")
    else:
        print(json.dumps(report, indent=2))

def main():
    parser = argparse.ArgumentParser(
        description="Conventa Ceremony Management CLI",
        epilog="Euystacio Sacred Bridge - Ceremony Automation System"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show ceremony status')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process ceremony entries')
    process_parser.add_argument('--entry-file', help='Process specific entry file')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List ceremony records')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify Red Seal integrity')
    verify_parser.add_argument('--entry-file', help='Verify specific entry file')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate transparency report')
    report_parser.add_argument('--output', help='Output file for report')
    
    args = parser.parse_args()
    
    if args.command == 'status':
        status_command(args)
    elif args.command == 'process':
        return process_command(args)
    elif args.command == 'list':
        list_command(args)
    elif args.command == 'verify':
        return verify_command(args)
    elif args.command == 'report':
        report_command(args)
    else:
        parser.print_help()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())