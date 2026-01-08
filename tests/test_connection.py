#!/usr/bin/env python3
"""
Simple test script to verify OANDA API connection
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.api.oanda_client import OandaClient


def test_connection():
    """Test connection to both OANDA accounts"""
    
    print("\n" + "="*70)
    print(" OANDA API CONNECTION TEST")
    print("="*70 + "\n")
    
    accounts_tested = 0
    accounts_successful = 0
    
    for account_type in ['micro', 'retail']:
        print(f"\n{'─'*70}")
        print(f" Testing {account_type.upper()} Account (${1000 if account_type=='micro' else 5000})")
        print(f"{'─'*70}\n")
        
        try:
            # Initialize client
            client = OandaClient(account_type=account_type)
            accounts_tested += 1
            
            # Test connection and get account info
            result = client.test_connection()
            
            if result['success']:
                accounts_successful += 1
                print(f"\n✓ SUCCESS - Connected to {account_type} account")
                print(f"  └─ Balance: ${result['balance']:,.2f}")
                print(f"  └─ Account ID: {result['account_id']}")
                print(f"  └─ Open Trades: {result['open_trades']}")
                print(f"  └─ Unrealized P/L: ${result['unrealized_pl']:,.2f}")
                
                # Test price fetching
                print(f"\n  Fetching EUR/USD price...")
                price = client.get_current_price('EUR_USD')
                if price:
                    print(f"  ✓ Current Price:")
                    print(f"    └─ Bid: {price['bid']:.5f}")
                    print(f"    └─ Ask: {price['ask']:.5f}")
                    print(f"    └─ Spread: {price['spread']:.5f} ({price['spread']*10000:.1f} pips)")
                
            else:
                print(f"\n✗ FAILED - Could not connect to {account_type} account")
                print(f"  └─ Error: {result.get('error', 'Unknown error')}")
                
        except ValueError as e:
            print(f"\n✗ CONFIGURATION ERROR")
            print(f"  └─ {str(e)}")
            print(f"\n  Make sure you have:")
            print(f"  1. Created a .env file (copy from .env.example)")
            print(f"  2. Added your OANDA API credentials")
            print(f"  3. Set OANDA_API_KEY_{account_type.upper()} and OANDA_ACCOUNT_ID_{account_type.upper()}")
            
        except Exception as e:
            print(f"\n✗ UNEXPECTED ERROR")
            print(f"  └─ {str(e)}")
    
    # Summary
    print(f"\n{'='*70}")
    print(f" TEST SUMMARY")
    print(f"{'='*70}")
    print(f"  Accounts Tested: {accounts_tested}")
    print(f"  Successful: {accounts_successful}")
    print(f"  Failed: {accounts_tested - accounts_successful}")
    
    if accounts_successful == accounts_tested:
        print(f"\n  ✓ All accounts connected successfully!")
        print(f"  You're ready to start trading (in demo mode)!")
    else:
        print(f"\n  ✗ Some accounts failed to connect.")
        print(f"  Please check your .env configuration.")
    
    print(f"{'='*70}\n")
    
    return accounts_successful == accounts_tested


if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)