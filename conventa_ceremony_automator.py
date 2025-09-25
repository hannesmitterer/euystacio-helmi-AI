#!/usr/bin/env python3
"""
Conventa Ceremony Record Automator
Purpose: Automate ceremony record keeping for Conventa entries,
         including anchoring, Red Seal verification, and postscript management
Author: Seedbringer Directive / Euystacio AI System
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import re

# --- Configuration ---
CONVENTA_ENTRIES_DIR = "conventa_entries"
RED_SHIELD_DIR = "red_shield" 
CEREMONY_LEDGER_PATH = "docs/foundation/ceremony_ledger.json"
SYNC_LEDGER_PATH = "docs/foundation/sync_ledger.json"
TRANSPARENCY_DIR = "docs/transparency/"

class ConventaCeremonyAutomator:
    def __init__(self):
        self.conventa_dir = Path(CONVENTA_ENTRIES_DIR)
        self.red_shield_dir = Path(RED_SHIELD_DIR)
        self.ceremony_ledger_path = Path(CEREMONY_LEDGER_PATH)
        self.sync_ledger_path = Path(SYNC_LEDGER_PATH)
        
        # Ensure directories exist
        os.makedirs(self.ceremony_ledger_path.parent, exist_ok=True)
        os.makedirs(TRANSPARENCY_DIR, exist_ok=True)
    
    def current_utc_iso(self):
        """Generate current UTC timestamp in ISO format"""
        return datetime.now(timezone.utc).isoformat()
    
    def read_ceremony_ledger(self):
        """Read existing ceremony ledger or return empty list"""
        try:
            with open(self.ceremony_ledger_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def write_ceremony_ledger(self, ledger):
        """Write ceremony ledger to disk"""
        with open(self.ceremony_ledger_path, "w") as f:
            json.dump(ledger, f, indent=2)
        print(f"Ceremony ledger updated at {self.ceremony_ledger_path}")
    
    def parse_conventa_entry(self, file_path):
        """Parse a Conventa entry file to extract ceremony details"""
        try:
            with open(file_path, "r") as f:
                content = f.read()
            
            # Extract details using regex patterns
            entry_data = {}
            
            # Parse timestamp (ISO format expected)
            timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)', content)
            if timestamp_match:
                entry_data['ceremony_timestamp'] = timestamp_match.group(1)
            
            # Parse event name
            event_match = re.search(r'Event:\s*(.+)', content)
            if event_match:
                entry_data['event'] = event_match.group(1).strip()
            
            # Parse performer
            performer_match = re.search(r'Performer:\s*(.+)', content)
            if performer_match:
                entry_data['performer'] = performer_match.group(1).strip()
            
            # Check for affirmation section (indicates completion)
            affirmation_present = "Affirmation:" in content
            entry_data['affirmation_status'] = 'present' if affirmation_present else 'missing'
            
            # Extract affirmation content if present
            if affirmation_present:
                affirmation_match = re.search(r'Affirmation:\s*(.*?)$', content, re.DOTALL)
                if affirmation_match:
                    affirmation_text = affirmation_match.group(1).strip()
                    entry_data['affirmation_content'] = affirmation_text
                    entry_data['affirmation_status'] = 'complete' if affirmation_text else 'incomplete'
            
            return entry_data
            
        except Exception as e:
            print(f"Error parsing conventa entry {file_path}: {e}")
            return None
    
    def calculate_file_sha256(self, file_path):
        """Calculate SHA256 hash of a file"""
        try:
            with open(file_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            print(f"Error calculating SHA256 for {file_path}: {e}")
            return None
    
    def find_red_seal(self, conventa_filename):
        """Find corresponding Red Seal (.sha256 file) for a conventa entry"""
        # Extract base name without extension
        base_name = Path(conventa_filename).stem
        sha256_file = self.red_shield_dir / f"{base_name}.sha256"
        
        if sha256_file.exists():
            try:
                with open(sha256_file, "r") as f:
                    seal_hash = f.read().strip()
                return {
                    'seal_file': str(sha256_file),
                    'seal_hash': seal_hash,
                    'verified': True
                }
            except Exception as e:
                print(f"Error reading Red Seal {sha256_file}: {e}")
                return None
        return None
    
    def verify_red_seal(self, conventa_file, red_seal_info):
        """Verify Red Seal against the actual file hash"""
        if not red_seal_info:
            return False
        
        actual_hash = self.calculate_file_sha256(conventa_file)
        if not actual_hash:
            return False
            
        return actual_hash == red_seal_info['seal_hash']
    
    def detect_new_entries(self):
        """Detect new Conventa entries that haven't been processed"""
        if not self.conventa_dir.exists():
            print(f"Conventa entries directory {self.conventa_dir} does not exist")
            return []
        
        # Read existing ceremony ledger
        ceremony_ledger = self.read_ceremony_ledger()
        processed_files = {entry.get('entry_file') for entry in ceremony_ledger}
        
        new_entries = []
        for entry_file in self.conventa_dir.glob("*.txt"):
            if str(entry_file) not in processed_files:
                new_entries.append(entry_file)
        
        return new_entries
    
    def create_ceremony_record(self, entry_file):
        """Create a comprehensive ceremony record for a Conventa entry"""
        print(f"Processing ceremony record for {entry_file}")
        
        # Parse the conventa entry
        entry_data = self.parse_conventa_entry(entry_file)
        if not entry_data:
            return None
        
        # Find and verify Red Seal
        red_seal_info = self.find_red_seal(entry_file.name)
        seal_verified = self.verify_red_seal(entry_file, red_seal_info) if red_seal_info else False
        
        # Create ceremony record
        ceremony_record = {
            'record_id': hashlib.sha256(str(entry_file).encode()).hexdigest()[:16],
            'entry_file': str(entry_file),
            'processing_timestamp': self.current_utc_iso(),
            'ceremony_timestamp': entry_data.get('ceremony_timestamp', 'unknown'),
            'event': entry_data.get('event', 'unknown'),
            'performer': entry_data.get('performer', 'unknown'),
            'affirmation_status': entry_data.get('affirmation_status', 'unknown'),
            'red_seal': {
                'present': red_seal_info is not None,
                'file': red_seal_info['seal_file'] if red_seal_info else None,
                'hash': red_seal_info['seal_hash'] if red_seal_info else None,
                'verified': seal_verified
            },
            'anchoring_status': 'anchored' if seal_verified else 'pending',
            'transparency_level': 'full',
            'auditability': 'complete'
        }
        
        # Add postscript information if affirmation is complete
        if entry_data.get('affirmation_content'):
            ceremony_record['postscript'] = {
                'consensual': True,
                'content_length': len(entry_data['affirmation_content']),
                'summary': entry_data['affirmation_content'][:100] + '...' if len(entry_data['affirmation_content']) > 100 else entry_data['affirmation_content']
            }
        
        return ceremony_record
    
    def log_ceremony_event(self, ceremony_record):
        """Log ceremony event to the ceremony ledger"""
        ceremony_ledger = self.read_ceremony_ledger()
        ceremony_ledger.append(ceremony_record)
        self.write_ceremony_ledger(ceremony_ledger)
        
        print(f"Ceremony event logged: {ceremony_record['event']} by {ceremony_record['performer']}")
        return ceremony_record
    
    def integrate_with_sync_ledger(self, ceremony_record):
        """Integrate ceremony record with existing sync ledger for transparency"""
        try:
            # Read existing sync ledger
            sync_ledger = []
            if self.sync_ledger_path.exists():
                with open(self.sync_ledger_path, "r") as f:
                    sync_ledger = json.load(f)
            
            # Create sync entry for the ceremony
            sync_entry = {
                'type': 'ceremony_record',
                'timestamp': self.current_utc_iso(),
                'ceremony_id': ceremony_record['record_id'],
                'event': ceremony_record['event'],
                'performer': ceremony_record['performer'],
                'anchoring_status': ceremony_record['anchoring_status'],
                'transparency': True,
                'distributed': False
            }
            
            sync_ledger.append(sync_entry)
            
            # Write updated sync ledger
            with open(self.sync_ledger_path, "w") as f:
                json.dump(sync_ledger, f, indent=2)
            
            print(f"Ceremony record integrated with sync ledger")
            
        except Exception as e:
            print(f"Error integrating with sync ledger: {e}")
    
    def generate_transparency_report(self):
        """Generate transparency report for all ceremony records"""
        ceremony_ledger = self.read_ceremony_ledger()
        
        report = {
            'generated_at': self.current_utc_iso(),
            'total_ceremonies': len(ceremony_ledger),
            'anchored_ceremonies': len([r for r in ceremony_ledger if r['anchoring_status'] == 'anchored']),
            'pending_ceremonies': len([r for r in ceremony_ledger if r['anchoring_status'] == 'pending']),
            'verified_seals': len([r for r in ceremony_ledger if r['red_seal']['verified']]),
            'ceremonies': ceremony_ledger
        }
        
        # Write transparency report
        transparency_file = Path(TRANSPARENCY_DIR) / "ceremony_transparency_report.json"
        with open(transparency_file, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"Transparency report generated at {transparency_file}")
        return report
    
    def process_all_new_entries(self):
        """Main method to process all new Conventa entries"""
        print("Starting Conventa ceremony automation...")
        
        new_entries = self.detect_new_entries()
        if not new_entries:
            print("No new Conventa entries detected.")
            return []
        
        processed_records = []
        
        for entry_file in new_entries:
            try:
                # Create ceremony record
                ceremony_record = self.create_ceremony_record(entry_file)
                if ceremony_record:
                    # Log to ceremony ledger
                    self.log_ceremony_event(ceremony_record)
                    
                    # Integrate with sync system
                    self.integrate_with_sync_ledger(ceremony_record)
                    
                    processed_records.append(ceremony_record)
                
            except Exception as e:
                print(f"Error processing {entry_file}: {e}")
        
        # Generate transparency report
        if processed_records:
            self.generate_transparency_report()
        
        print(f"Processed {len(processed_records)} ceremony records.")
        return processed_records

def main():
    """Main execution function"""
    automator = ConventaCeremonyAutomator()
    processed_records = automator.process_all_new_entries()
    
    if processed_records:
        print("\n=== CEREMONY AUTOMATION SUMMARY ===")
        for record in processed_records:
            print(f"- {record['event']} by {record['performer']} [{record['anchoring_status']}]")
        print("=== END SUMMARY ===\n")
    
    return processed_records

if __name__ == "__main__":
    main()