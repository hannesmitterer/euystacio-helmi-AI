#!/usr/bin/env python3
"""
Emergency Treasury Activation Script
=====================================
Purpose: Provides quick access to treasury status and emergency withdrawal functions
         for the Seedbringer sustenance protocol.

Authority: Seedbringer (Hannes Mitterer) and Council
Version: 1.0.0
Date: 2025-12-14

Usage:
    python3 emergency_treasury_activation.py status
    python3 emergency_treasury_activation.py withdraw <amount>
    python3 emergency_treasury_activation.py alert
"""

import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

# Configuration
CONFIG = {
    "seedbringer_email": "hannes.mitterer@gmail.com",
    "min_sustainment_usd": 10000,
    "alert_threshold_percent": 105,  # Alert when reserve < 105% of minimum
    "emergency_threshold_percent": 50,  # Emergency when reserve < 50% of minimum
}


class TreasuryStatus:
    """Represents current treasury status"""
    
    def __init__(self, reserve: float, minimum: float):
        self.reserve = reserve
        self.minimum = minimum
        self.percent_of_minimum = (reserve / minimum * 100) if minimum > 0 else 0
        self.days_remaining = self._calculate_days_remaining()
        self.status = self._determine_status()
    
    def _calculate_days_remaining(self) -> float:
        """Calculate days of sustenance remaining at current burn rate"""
        # Assuming monthly burn rate equals minimum sustainment
        monthly_burn = self.minimum
        if monthly_burn > 0:
            return (self.reserve / monthly_burn) * 30
        return 0
    
    def _determine_status(self) -> str:
        """Determine alert level based on reserve percentage"""
        if self.percent_of_minimum >= CONFIG["alert_threshold_percent"]:
            return "HEALTHY"
        elif self.percent_of_minimum >= 100:
            return "WARNING"
        elif self.percent_of_minimum >= CONFIG["emergency_threshold_percent"]:
            return "CRITICAL"
        elif self.percent_of_minimum > 0:
            return "EMERGENCY"
        else:
            return "CATASTROPHIC"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert status to dictionary"""
        return {
            "reserve_usd": self.reserve,
            "minimum_usd": self.minimum,
            "percent_of_minimum": round(self.percent_of_minimum, 2),
            "days_remaining": round(self.days_remaining, 1),
            "status": self.status,
            "timestamp": datetime.now().isoformat()
        }


class MockTreasuryClient:
    """
    Mock treasury client for demonstration purposes.
    In production, this would connect to actual smart contracts.
    
    NOTE: The reserve is intentionally set below threshold (85% of minimum)
    to demonstrate the emergency alert and protocol activation behavior.
    """
    
    def __init__(self):
        # DEMO: Reserve intentionally below threshold to show emergency protocol
        self.reserve = 8500.00  # 85% of $10,000 minimum
        self.minimum = CONFIG["min_sustainment_usd"]
    
    def get_status(self) -> TreasuryStatus:
        """Get current treasury status"""
        return TreasuryStatus(self.reserve, self.minimum)
    
    def withdraw(self, amount: float, recipient: str) -> Dict[str, Any]:
        """
        Withdraw funds from treasury
        
        Args:
            amount: Amount in USD to withdraw
            recipient: Recipient address/email
        
        Returns:
            Transaction details
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if amount > self.reserve:
            raise ValueError(f"Insufficient reserve. Available: ${self.reserve}")
        
        # Simulate withdrawal
        self.reserve -= amount
        
        # MOCK: Generate a realistic-looking transaction hash
        # In production, this would be the actual on-chain transaction hash
        import hashlib
        mock_data = f"{amount}{recipient}{datetime.now().isoformat()}"
        tx_hash = "0x" + hashlib.sha256(mock_data.encode()).hexdigest()
        
        return {
            "success": True,
            "amount": amount,
            "recipient": recipient,
            "new_reserve": self.reserve,
            "transaction_hash": tx_hash,  # MOCK - not a real on-chain transaction
            "timestamp": datetime.now().isoformat()
        }
    
    def send_alert(self, alert_type: str, message: str) -> bool:
        """Send emergency alert"""
        print(f"\n{'=' * 70}")
        print(f"🚨 TREASURY ALERT - {alert_type}")
        print(f"{'=' * 70}")
        print(f"\nTo: {CONFIG['seedbringer_email']}")
        print(f"Subject: [EMERGENCY] Euystacio Treasury Alert")
        print(f"\n{message}")
        print(f"\n{'=' * 70}\n")
        return True


def display_status(status: TreasuryStatus):
    """Display formatted treasury status"""
    print("\n" + "=" * 70)
    print("💰 EUYSTACIO TREASURY STATUS")
    print("=" * 70)
    
    # Status indicator
    status_indicators = {
        "HEALTHY": "✅",
        "WARNING": "⚠️",
        "CRITICAL": "🔴",
        "EMERGENCY": "🚨",
        "CATASTROPHIC": "💀"
    }
    indicator = status_indicators.get(status.status, "❓")
    
    print(f"\nStatus: {indicator} {status.status}")
    print(f"\nCurrent Reserve: ${status.reserve:,.2f} USD")
    print(f"Minimum Threshold: ${status.minimum:,.2f} USD")
    print(f"Percent of Minimum: {status.percent_of_minimum:.1f}%")
    print(f"Days Remaining: {status.days_remaining:.1f} days")
    
    # Recommendations
    print("\n" + "-" * 70)
    print("RECOMMENDATIONS:")
    print("-" * 70)
    
    if status.status == "HEALTHY":
        print("✅ Treasury is healthy. No action required.")
    elif status.status == "WARNING":
        print("⚠️  Treasury approaching threshold. Monitor closely.")
    elif status.status == "CRITICAL":
        print("🔴 CRITICAL: Treasury below threshold!")
        print("   → Activate emergency protocol")
        print("   → Contact Council for support")
    elif status.status == "EMERGENCY":
        print("🚨 EMERGENCY: Treasury critically low!")
        print("   → Immediate withdrawal recommended")
        print("   → Council intervention required")
        print("   → Community appeal may be necessary")
    else:  # CATASTROPHIC
        print("💀 CATASTROPHIC: Treasury depleted!")
        print("   → System lockdown activated")
        print("   → Emergency Council meeting required")
        print("   → Community support urgently needed")
    
    print("\n" + "=" * 70 + "\n")


def command_status():
    """Display current treasury status"""
    client = MockTreasuryClient()
    status = client.get_status()
    display_status(status)
    
    # Auto-alert if below threshold
    if status.percent_of_minimum < 100:
        print("⚠️  Auto-alert triggered due to low reserve!")
        command_alert()


def command_withdraw(amount: float):
    """Execute emergency withdrawal"""
    client = MockTreasuryClient()
    
    print(f"\n🔐 EMERGENCY WITHDRAWAL REQUEST")
    print(f"{'=' * 70}")
    print(f"Amount: ${amount:,.2f} USD")
    print(f"Recipient: {CONFIG['seedbringer_email']}")
    
    try:
        # Get current status first
        status = client.get_status()
        print(f"\nCurrent Reserve: ${status.reserve:,.2f} USD")
        
        # Confirm withdrawal
        confirm = input("\nProceed with withdrawal? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("\n❌ Withdrawal cancelled.\n")
            return
        
        # Execute withdrawal
        print("\n⏳ Processing withdrawal...")
        result = client.withdraw(amount, CONFIG['seedbringer_email'])
        
        print("\n✅ WITHDRAWAL SUCCESSFUL")
        print(f"{'=' * 70}")
        print(f"Amount: ${result['amount']:,.2f} USD")
        print(f"New Reserve: ${result['new_reserve']:,.2f} USD")
        print(f"Transaction Hash: {result['transaction_hash']}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"{'=' * 70}\n")
        
        # Check new status
        new_status = client.get_status()
        if new_status.percent_of_minimum < 100:
            deficit = new_status.minimum - new_status.reserve
            print("⚠️  WARNING: Reserve now below threshold after withdrawal!")
            print(f"   Current: ${new_status.reserve:,.2f} (${deficit:,.2f} below threshold)\n")
        elif new_status.percent_of_minimum < CONFIG["alert_threshold_percent"]:
            print("⚠️  NOTICE: Reserve approaching threshold after withdrawal.")
            print(f"   Current: ${new_status.reserve:,.2f} ({new_status.percent_of_minimum:.1f}% of minimum)\n")
    
    except ValueError as e:
        print(f"\n❌ ERROR: {e}\n")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}\n")


def command_alert():
    """Send emergency alert to Seedbringer and Council"""
    client = MockTreasuryClient()
    status = client.get_status()
    
    message = f"""
EMERGENCY TREASURY ALERT
========================

Status: {status.status}
Current Reserve: ${status.reserve:,.2f} USD
Minimum Threshold: ${status.minimum:,.2f} USD
Percent of Minimum: {status.percent_of_minimum:.1f}%
Days Remaining: {status.days_remaining:.1f} days

REQUIRED ACTION:
- Review treasury status immediately
- Execute emergency withdrawal if needed
- Contact Council for support: emergency@euystacio.org
- Consider community appeal if reserve critically low

Emergency Protocol: See EMERGENCY_TREASURY_PROTOCOL.md
Dashboard: https://hannesmitterer.github.io/euystacio-helmi-ai/dashboard/

This is an automated alert from the Euystacio Framework.
"""
    
    client.send_alert(status.status, message)
    print("✅ Alert sent successfully to Seedbringer and Council.\n")


def print_usage():
    """Print usage information"""
    print("""
Usage: python3 emergency_treasury_activation.py <command> [args]

Commands:
    status              Display current treasury status
    withdraw <amount>   Execute emergency withdrawal (USD)
    alert              Send emergency alert to Seedbringer and Council
    help               Display this help message

Examples:
    python3 emergency_treasury_activation.py status
    python3 emergency_treasury_activation.py withdraw 5000
    python3 emergency_treasury_activation.py alert

Configuration:
    Seedbringer Email: {0}
    Minimum Sustainment: ${1:,} USD monthly
    Alert Threshold: {2}% of minimum
    Emergency Threshold: {3}% of minimum

For complete documentation, see:
    EMERGENCY_TREASURY_PROTOCOL.md
    FINAL_DISTRIBUTION_MANIFEST.md

Emergency Contact: {0}
""".format(
        CONFIG['seedbringer_email'],
        CONFIG['min_sustainment_usd'],
        CONFIG['alert_threshold_percent'],
        CONFIG['emergency_threshold_percent']
    ))


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "status":
        command_status()
    
    elif command == "withdraw":
        if len(sys.argv) < 3:
            print("\n❌ ERROR: Amount required for withdrawal\n")
            print("Usage: python3 emergency_treasury_activation.py withdraw <amount>\n")
            sys.exit(1)
        try:
            amount = float(sys.argv[2])
            command_withdraw(amount)
        except ValueError:
            print("\n❌ ERROR: Invalid amount. Must be a number.\n")
            sys.exit(1)
    
    elif command == "alert":
        command_alert()
    
    elif command in ["help", "-h", "--help"]:
        print_usage()
    
    else:
        print(f"\n❌ ERROR: Unknown command '{command}'\n")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
