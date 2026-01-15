#!/usr/bin/env python3
"""
lex_amoris_cli.py - Command-line interface for Lex Amoris Security System

This CLI tool allows you to interact with the Lex Amoris security enhancements.
"""

import argparse
import json
import sys
from lex_amoris_security import LexAmorisSecuritySystem


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='Lex Amoris Security System CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Process a packet
  %(prog)s process --data '{"message": "hello"}' --source 192.168.1.1
  
  # Get system status
  %(prog)s status
  
  # Create configuration backup
  %(prog)s backup
  
  # Check lazy security status
  %(prog)s lazy-status
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process a data packet')
    process_parser.add_argument('--data', required=True, help='JSON data packet')
    process_parser.add_argument('--source', required=True, help='Source IP address')
    
    # Status command
    subparsers.add_parser('status', help='Get complete system status')
    
    # Backup command
    subparsers.add_parser('backup', help='Create configuration backup')
    
    # Lazy security status
    subparsers.add_parser('lazy-status', help='Get lazy security status')
    
    # Blacklist command
    blacklist_parser = subparsers.add_parser('blacklist', help='Manage blacklist')
    blacklist_parser.add_argument('--list', action='store_true', help='List blocked sources')
    
    # Rescue command
    rescue_parser = subparsers.add_parser('rescue', help='Send rescue message')
    rescue_parser.add_argument('--source', required=True, help='Source to rescue')
    rescue_parser.add_argument('--reason', default='manual_rescue', help='Rescue reason')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize security system
    security = LexAmorisSecuritySystem()
    
    try:
        if args.command == 'process':
            # Process packet
            try:
                data = json.loads(args.data)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON data: {e}", file=sys.stderr)
                return 1
            
            result = security.process_packet(data, args.source)
            
            print(json.dumps(result, indent=2))
            
            if result["accepted"]:
                print("\n✓ Packet ACCEPTED", file=sys.stderr)
                return 0
            else:
                print("\n✗ Packet REJECTED", file=sys.stderr)
                return 1
        
        elif args.command == 'status':
            # Get system status
            status = security.get_system_status()
            print(json.dumps(status, indent=2))
            return 0
        
        elif args.command == 'backup':
            # Create backup
            manifest = security.create_configuration_backup()
            print(json.dumps(manifest, indent=2))
            
            files_count = len(manifest.get('files', {}))
            print(f"\n✓ Backed up {files_count} configuration files", file=sys.stderr)
            return 0
        
        elif args.command == 'lazy-status':
            # Get lazy security status
            status = security.lazy_security.get_status()
            print(json.dumps(status, indent=2))
            
            if status['is_active']:
                print("\n⚡ Security ACTIVE - high environmental pressure", file=sys.stderr)
            else:
                print("\n💤 Security INACTIVE - energy conservation mode", file=sys.stderr)
            return 0
        
        elif args.command == 'blacklist':
            if args.list:
                # List blacklisted sources
                blacklist = security.blacklist.get_blacklist()
                
                if blacklist:
                    print("Blocked sources:")
                    for source in blacklist:
                        print(f"  - {source}")
                    print(f"\nTotal: {len(blacklist)} sources blocked")
                else:
                    print("No sources currently blocked")
                return 0
        
        elif args.command == 'rescue':
            # Send rescue message
            message = security.rescue_channel.send_rescue_message(
                args.source,
                args.reason
            )
            print(json.dumps(message, indent=2))
            print(f"\n💖 Rescue message sent to {args.source}", file=sys.stderr)
            return 0
        
        else:
            parser.print_help()
            return 1
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
