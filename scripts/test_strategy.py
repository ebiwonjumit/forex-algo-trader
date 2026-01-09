#!/usr/bin/env python3
"""
Test SMA Crossover Strategy on Historical Data

This script loads historical data and runs the SMA crossover strategy
to generate and analyze trading signals.
"""

import sys
import os
import argparse
from pathlib import Path
import pandas as pd
import json

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.strategies.sma_crossover import SMACrossoverStrategy


def find_latest_data_file(instrument: str = 'EUR_USD') -> Path:
    """
    Find the most recent data file for an instrument
    
    Args:
        instrument: Currency pair
        
    Returns:
        Path to the latest data file
    """
    data_dir = Path('data/historical')
    
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")
    
    # Find all files matching the instrument
    files = list(data_dir.glob(f"{instrument}_*.csv"))
    
    if not files:
        raise FileNotFoundError(
            f"No data files found for {instrument}. "
            f"Run 'python scripts/fetch_data.py' first."
        )
    
    # Return the most recent file
    latest = max(files, key=lambda p: p.stat().st_mtime)
    return latest


def load_data(filepath: Path) -> pd.DataFrame:
    """
    Load historical data from CSV
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        DataFrame with OHLC data
    """
    print(f"\nLoading data from: {filepath}")
    
    df = pd.read_csv(filepath)
    df['time'] = pd.to_datetime(df['time'])
    
    print(f"  ✓ Loaded {len(df)} candles")
    print(f"  Date range: {df['time'].min()} to {df['time'].max()}")
    print(f"  Price range: {df['close'].min():.5f} to {df['close'].max():.5f}")
    
    return df


def print_signals(strategy: SMACrossoverStrategy, max_display: int = 10):
    """
    Print trading signals in a readable format
    
    Args:
        strategy: Strategy instance
        max_display: Maximum number of signals to display
    """
    signals = strategy.get_all_signals()
    
    if len(signals) == 0:
        print("\n  No signals generated!")
        return
    
    print(f"\n{'='*80}")
    print(f" TRADING SIGNALS (showing {min(max_display, len(signals))} of {len(signals)})")
    print(f"{'='*80}\n")
    
    for i, (idx, row) in enumerate(signals.head(max_display).iterrows()):
        signal_type = "🟢 BUY " if row['signal'] == 1 else "🔴 SELL"
        print(f"{i+1}. {signal_type}")
        print(f"   Time: {row['time']}")
        print(f"   Price: {row['close']:.5f}")
        print(f"   SMA{strategy.short_period}: {row['sma_short']:.5f}")
        print(f"   SMA{strategy.long_period}: {row['sma_long']:.5f}")
        print(f"   Signal Strength: {row['signal_strength']:.3f}%")
        print()


def print_trade_analysis(strategy: SMACrossoverStrategy):
    """
    Print analysis of completed trades
    
    Args:
        strategy: Strategy instance
    """
    trades = strategy.get_entry_exit_pairs()
    
    if len(trades) == 0:
        print("\n  No complete trades found")
        return
    
    print(f"\n{'='*80}")
    print(f" TRADE ANALYSIS")
    print(f"{'='*80}\n")
    
    # Show first few trades
    print(f"Sample Trades (first 5):\n")
    for i, (idx, trade) in enumerate(trades.head(5).iterrows()):
        profit_emoji = "✅" if trade['pips_profit'] > 0 else "❌"
        print(f"{i+1}. {profit_emoji} {trade['position_type'].upper()}")
        print(f"   Entry:  {trade['entry_time']} @ {trade['entry_price']:.5f}")
        print(f"   Exit:   {trade['exit_time']} @ {trade['exit_price']:.5f}")
        print(f"   Profit: {trade['pips_profit']:.1f} pips ({trade['percent_profit']:.2f}%)")
        print()
    
    # Performance summary
    perf = strategy.get_performance_summary()
    
    print(f"\n{'─'*80}")
    print(f" PERFORMANCE SUMMARY")
    print(f"{'─'*80}\n")
    print(f"  Total Trades: {perf['total_trades']}")
    print(f"  Winning Trades: {perf['winning_trades']} ({perf['win_rate']:.1f}%)")
    print(f"  Losing Trades: {perf['losing_trades']}")
    print(f"  \n  Total Pips: {perf['total_pips']:.1f}")
    print(f"  Average Pips/Trade: {perf['average_pips_per_trade']:.1f}")
    print(f"  Best Trade: {perf['best_trade_pips']:.1f} pips")
    print(f"  Worst Trade: {perf['worst_trade_pips']:.1f} pips")
    print(f"  \n  Average Win: {perf['average_win_pips']:.1f} pips")
    print(f"  Average Loss: {perf['average_loss_pips']:.1f} pips")
    
    if perf['profit_factor'] != float('inf'):
        print(f"  Profit Factor: {perf['profit_factor']:.2f}")
    else:
        print(f"  Profit Factor: ∞ (no losing trades)")
    
    print(f"  \n  Total Return: {perf['total_return_percent']:.2f}%")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Test SMA Crossover Strategy on Historical Data'
    )
    parser.add_argument(
        '--pair',
        type=str,
        default='EUR_USD',
        help='Currency pair (default: EUR_USD)'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Specific data file to use (otherwise uses latest)'
    )
    parser.add_argument(
        '--short',
        type=int,
        default=20,
        help='Short MA period (default: 20)'
    )
    parser.add_argument(
        '--long',
        type=int,
        default=50,
        help='Long MA period (default: 50)'
    )
    parser.add_argument(
        '--export',
        action='store_true',
        help='Export signals and trades to CSV'
    )
    
    args = parser.parse_args()
    
    print("="*80)
    print(" SMA CROSSOVER STRATEGY TESTER")
    print("="*80)
    
    try:
        # Load data
        if args.file:
            filepath = Path(args.file)
        else:
            filepath = find_latest_data_file(args.pair)
        
        data = load_data(filepath)
        
        # Initialize strategy
        print(f"\nInitializing strategy...")
        print(f"  Short MA: {args.short} periods")
        print(f"  Long MA: {args.long} periods")
        
        strategy = SMACrossoverStrategy(
            short_period=args.short,
            long_period=args.long,
            min_candles_after_cross=1
        )
        
        # Load data and run strategy
        strategy.load_data(data)
        strategy.run()
        
        # Display results
        print_signals(strategy, max_display=10)
        print_trade_analysis(strategy)
        
        # Export if requested
        if args.export:
            output_dir = Path('data/trades')
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Export signals
            signals_file = output_dir / f"{args.pair}_signals_SMA{args.short}_{args.long}.csv"
            strategy.export_signals(str(signals_file))
            print(f"\n  ✓ Signals exported to: {signals_file}")
            
            # Export trades
            trades = strategy.get_entry_exit_pairs()
            if len(trades) > 0:
                trades_file = output_dir / f"{args.pair}_trades_SMA{args.short}_{args.long}.csv"
                trades.to_csv(trades_file, index=False)
                print(f"  ✓ Trades exported to: {trades_file}")
            
            # Export performance summary
            perf = strategy.get_performance_summary()
            perf_file = output_dir / f"{args.pair}_performance_SMA{args.short}_{args.long}.json"
            with open(perf_file, 'w') as f:
                json.dump(perf, f, indent=2, default=str)
            print(f"  ✓ Performance summary exported to: {perf_file}")
        
        print("\n" + "="*80)
        print(" STRATEGY TEST COMPLETE")
        print("="*80 + "\n")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease run this first:")
        print(f"  python scripts/fetch_data.py --pair {args.pair}")
        return 1
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())