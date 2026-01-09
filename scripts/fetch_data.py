#!/usr/bin/env python3
"""
Fetch historical data from OANDA and save to CSV
"""

import sys
import os
import argparse
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.api.oanda_client import OandaClient


def fetch_historical_data(
    instrument: str = 'EUR_USD',
    granularity: str = 'H1',
    days: int = 365,
    account_type: str = 'micro'
) -> pd.DataFrame:
    """
    Fetch historical candlestick data from OANDA
    
    Args:
        instrument: Currency pair
        granularity: Timeframe (H1, H4, D, etc.)
        days: Number of days of history to fetch
        account_type: Which account to use
        
    Returns:
        DataFrame with OHLC data
    """
    print(f"\nFetching {days} days of {instrument} data ({granularity})...")
    
    client = OandaClient(account_type=account_type)
    
    # OANDA allows max 5000 candles per request
    # Calculate how many requests we need
    candles_per_day = {
        'M1': 1440,   # 1 minute
        'M5': 288,    # 5 minutes
        'M15': 96,    # 15 minutes
        'M30': 48,    # 30 minutes
        'H1': 24,     # 1 hour
        'H4': 6,      # 4 hours
        'D': 1,       # Daily
        'W': 1/7,     # Weekly
        'M': 1/30     # Monthly
    }
    
    total_candles_needed = int(days * candles_per_day.get(granularity, 24))
    max_per_request = 5000
    
    all_candles = []
    
    if total_candles_needed <= max_per_request:
        # Single request
        candles = client.get_candles(
            instrument=instrument,
            granularity=granularity,
            count=total_candles_needed
        )
        all_candles.extend(candles)
    else:
        # Multiple requests needed
        num_requests = (total_candles_needed // max_per_request) + 1
        print(f"  Need {num_requests} requests to fetch all data...")
        
        # Start from today and go backwards
        to_time = datetime.utcnow()
        
        for i in range(num_requests):
            from_time = to_time - timedelta(days=days/num_requests)
            
            candles = client.get_candles(
                instrument=instrument,
                granularity=granularity,
                count=max_per_request,
                from_time=from_time.isoformat() + 'Z',
                to_time=to_time.isoformat() + 'Z'
            )
            
            all_candles.extend(candles)
            to_time = from_time
            
            print(f"  Progress: {i+1}/{num_requests} requests complete")
    
    if not all_candles:
        print("  ✗ No data fetched!")
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(all_candles)
    df['time'] = pd.to_datetime(df['time'])
    df = df.sort_values('time').reset_index(drop=True)
    
    # Remove duplicates (can happen at request boundaries)
    df = df.drop_duplicates(subset=['time']).reset_index(drop=True)
    
    print(f"  ✓ Fetched {len(df)} candles")
    print(f"  Date range: {df['time'].min()} to {df['time'].max()}")
    
    return df


def save_to_csv(df: pd.DataFrame, instrument: str, granularity: str):
    """
    Save DataFrame to CSV file
    
    Args:
        df: DataFrame with OHLC data
        instrument: Currency pair
        granularity: Timeframe
    """
    # Create data directory if it doesn't exist
    data_dir = Path('data/historical')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    filename = f"{instrument}_{granularity}_{datetime.now().strftime('%Y%m%d')}.csv"
    filepath = data_dir / filename
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    
    print(f"\n  ✓ Saved to: {filepath}")
    print(f"  File size: {filepath.stat().st_size / 1024:.1f} KB")
    
    return filepath


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Fetch historical forex data from OANDA'
    )
    parser.add_argument(
        '--pair',
        type=str,
        default='EUR_USD',
        help='Currency pair (default: EUR_USD)'
    )
    parser.add_argument(
        '--granularity',
        type=str,
        default='H1',
        choices=['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D', 'W', 'M'],
        help='Timeframe (default: H1)'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=365,
        help='Number of days to fetch (default: 365)'
    )
    parser.add_argument(
        '--account',
        type=str,
        default='micro',
        choices=['micro', 'retail'],
        help='Account type to use (default: micro)'
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print(" OANDA HISTORICAL DATA FETCHER")
    print("="*70)
    print(f"\nParameters:")
    print(f"  Currency Pair: {args.pair}")
    print(f"  Granularity: {args.granularity}")
    print(f"  Days: {args.days}")
    print(f"  Account: {args.account}")
    
    try:
        # Fetch data
        df = fetch_historical_data(
            instrument=args.pair,
            granularity=args.granularity,
            days=args.days,
            account_type=args.account
        )
        
        if df.empty:
            print("\n✗ Failed to fetch data")
            return 1
        
        # Display sample
        print(f"\nSample data (first 5 rows):")
        print(df.head().to_string())
        
        print(f"\nSample data (last 5 rows):")
        print(df.tail().to_string())
        
        # Save to CSV
        filepath = save_to_csv(df, args.pair, args.granularity)
        
        print("\n" + "="*70)
        print(" SUCCESS!")
        print("="*70)
        print(f"\nData successfully fetched and saved.")
        print(f"You can now use this data for backtesting.\n")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())