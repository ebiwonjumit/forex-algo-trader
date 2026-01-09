# Trading Strategies Module

## Overview

This module contains the trading strategy system for the forex algorithmic trader. All strategies inherit from the `BaseStrategy` class and implement specific trading logic.

## Architecture

```
src/strategies/
├── __init__.py
├── base_strategy.py       # Abstract base class + technical indicators
└── sma_crossover.py       # SMA crossover implementation
```

## Base Strategy

The `BaseStrategy` class provides:

- **Data Loading**: Load and validate OHLC data
- **Indicator Calculation**: Abstract method for calculating indicators
- **Signal Generation**: Abstract method for generating buy/sell signals
- **Signal Management**: Get latest signal, all signals, filtered signals
- **Performance Tracking**: Summary statistics and export functionality

### Technical Indicators

The `TechnicalIndicators` class provides static methods for common indicators:

- **SMA** - Simple Moving Average
- **EMA** - Exponential Moving Average
- **RSI** - Relative Strength Index
- **ATR** - Average True Range
- **Bollinger Bands**
- **MACD** - Moving Average Convergence Divergence

## SMA Crossover Strategy

### Strategy Logic

**Entry Signals:**
- **BUY (Golden Cross)**: Short MA crosses above Long MA
- **SELL (Death Cross)**: Short MA crosses below Long MA

**Default Parameters:**
- Short MA: 20 periods
- Long MA: 50 periods
- Confirmation: 1 candle after crossover

### Usage

```python
from src.strategies.sma_crossover import SMACrossoverStrategy
import pandas as pd

# Load historical data
data = pd.read_csv('data/historical/EUR_USD_H1_20250108.csv')

# Initialize strategy
strategy = SMACrossoverStrategy(
    short_period=20,
    long_period=50,
    min_candles_after_cross=1
)

# Run strategy
strategy.load_data(data)
strategy.run()

# Get latest signal
latest = strategy.get_latest_signal()
print(latest['message'])

# Get performance summary
perf = strategy.get_performance_summary()
print(f"Win Rate: {perf['win_rate']:.1f}%")
print(f"Total Pips: {perf['total_pips']:.1f}")
```

## Testing the Strategy

Use the test script to analyze strategy performance:

```bash
# Test with default parameters (SMA 20/50)
python scripts/test_strategy.py --pair EUR_USD

# Test with custom parameters
python scripts/test_strategy.py --pair EUR_USD --short 10 --long 30

# Export signals and trades
python scripts/test_strategy.py --pair EUR_USD --export
```

### Output

The test script provides:

1. **Signal List**: All buy/sell signals with prices and timestamps
2. **Trade Analysis**: Entry/exit pairs with profit/loss in pips
3. **Performance Summary**: 
   - Win rate
   - Total pips
   - Average pips per trade
   - Profit factor
   - Best/worst trades

### Example Output

```
================================================================================
 TRADING SIGNALS (showing 10 of 45)
================================================================================

1. 🟢 BUY 
   Time: 2024-03-15 14:00:00
   Price: 1.08450
   SMA20: 1.08472
   SMA50: 1.08455
   Signal Strength: 0.016%

2. 🔴 SELL
   Time: 2024-04-02 09:00:00
   Price: 1.07892
   SMA20: 1.07883
   SMA50: 1.07905
   Signal Strength: 0.020%

================================================================================
 PERFORMANCE SUMMARY
================================================================================

  Total Trades: 22
  Winning Trades: 12 (54.5%)
  Losing Trades: 10
  
  Total Pips: 345.2
  Average Pips/Trade: 15.7
  Best Trade: 89.3 pips
  Worst Trade: -34.7 pips
  
  Average Win: 42.1 pips
  Average Loss: -21.3 pips
  Profit Factor: 1.98
  
  Total Return: 3.18%
```

## Creating New Strategies

To create a new strategy:

1. **Inherit from BaseStrategy**:
```python
from .base_strategy import BaseStrategy, TechnicalIndicators

class MyStrategy(BaseStrategy):
    def __init__(self, param1, param2):
        parameters = {'param1': param1, 'param2': param2}
        super().__init__(name='My_Strategy', parameters=parameters)
```

2. **Implement calculate_indicators()**:
```python
def calculate_indicators(self) -> pd.DataFrame:
    # Calculate your indicators
    self.data['my_indicator'] = calculate_something(self.data['close'])
    return self.data
```

3. **Implement generate_signals()**:
```python
def generate_signals(self) -> pd.DataFrame:
    # Generate buy/sell signals
    self.data['signal'] = 0
    self.data.loc[buy_condition, 'signal'] = 1
    self.data.loc[sell_condition, 'signal'] = -1
    return self.data
```

## Signal Format

Signals use integer values:
- `1` = BUY signal
- `-1` = SELL signal
- `0` = HOLD (no action)

## Performance Metrics

### Key Metrics

- **Win Rate**: Percentage of profitable trades
- **Total Pips**: Sum of all trade profits/losses
- **Average Pips/Trade**: Mean profit per trade
- **Profit Factor**: Gross profit / Gross loss
- **Best/Worst Trade**: Highest gain and loss in pips

### Understanding Results

- **Win Rate > 50%**: Strategy has edge (for non-trending strategies)
- **Profit Factor > 1.5**: Good risk/reward ratio
- **Total Pips > 0**: Strategy is profitable on historical data
- **Avg Win > Avg Loss**: Favorable risk/reward

⚠️ **Important**: Past performance doesn't guarantee future results!

## Next Steps

1. ✅ Test SMA strategy on historical data
2. ⬜ Build backtesting engine with risk management
3. ⬜ Add more strategies (RSI, MACD, Bollinger)
4. ⬜ Implement position sizing
5. ⬜ Deploy to paper trading accounts

---

**Ready to test?** Run:
```bash
python scripts/test_strategy.py --pair EUR_USD --export
```