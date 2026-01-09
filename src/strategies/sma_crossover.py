"""
SMA Crossover Strategy

A simple trend-following strategy based on moving average crossovers:
- BUY when short MA crosses above long MA (golden cross)
- SELL when short MA crosses below long MA (death cross)
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Optional

from .base_strategy import BaseStrategy, TechnicalIndicators

logger = logging.getLogger(__name__)


class SMACrossoverStrategy(BaseStrategy):
    """
    Simple Moving Average Crossover Strategy
    
    Parameters:
        short_period: Period for short-term moving average (default: 20)
        long_period: Period for long-term moving average (default: 50)
        min_candles_after_cross: Minimum candles to wait after crossover (default: 1)
    """
    
    def __init__(
        self,
        short_period: int = 20,
        long_period: int = 50,
        min_candles_after_cross: int = 1
    ):
        """
        Initialize SMA Crossover Strategy
        
        Args:
            short_period: Short MA period
            long_period: Long MA period
            min_candles_after_cross: Confirmation candles after crossover
        """
        parameters = {
            'short_period': short_period,
            'long_period': long_period,
            'min_candles_after_cross': min_candles_after_cross
        }
        
        super().__init__(name='SMA_Crossover', parameters=parameters)
        
        self.short_period = short_period
        self.long_period = long_period
        self.min_candles_after_cross = min_candles_after_cross
        
        # Validate parameters
        if short_period >= long_period:
            raise ValueError(
                f"Short period ({short_period}) must be less than "
                f"long period ({long_period})"
            )
    
    def calculate_indicators(self) -> pd.DataFrame:
        """
        Calculate SMAs and identify crossovers
        
        Returns:
            DataFrame with SMA columns added
        """
        logger.info("Calculating SMA indicators...")
        
        # Calculate short and long SMAs
        self.data['sma_short'] = TechnicalIndicators.sma(
            self.data['close'],
            self.short_period
        )
        
        self.data['sma_long'] = TechnicalIndicators.sma(
            self.data['close'],
            self.long_period
        )
        
        # Calculate the difference (for identifying crossovers)
        self.data['sma_diff'] = self.data['sma_short'] - self.data['sma_long']
        
        # Identify crossover points
        # Crossover = when diff changes sign
        self.data['crossover'] = 0
        
        # Golden cross: short MA crosses above long MA (bullish)
        self.data.loc[
            (self.data['sma_diff'] > 0) & 
            (self.data['sma_diff'].shift(1) <= 0),
            'crossover'
        ] = 1
        
        # Death cross: short MA crosses below long MA (bearish)
        self.data.loc[
            (self.data['sma_diff'] < 0) & 
            (self.data['sma_diff'].shift(1) >= 0),
            'crossover'
        ] = -1
        
        logger.info(
            f"Calculated SMAs: {self.short_period}-period and {self.long_period}-period"
        )
        
        return self.data
    
    def generate_signals(self) -> pd.DataFrame:
        """
        Generate trading signals based on MA crossovers
        
        Returns:
            DataFrame with signal column
        """
        logger.info("Generating trading signals...")
        
        # Initialize signal column
        self.data['signal'] = 0
        
        # Generate signals at crossover points
        # We can add confirmation by waiting min_candles_after_cross
        if self.min_candles_after_cross > 1:
            # Wait for confirmation
            for i in range(len(self.data)):
                if self.data.loc[i, 'crossover'] != 0:
                    # Check if we have enough future candles
                    if i + self.min_candles_after_cross < len(self.data):
                        # Confirm the crossover is still valid
                        future_idx = i + self.min_candles_after_cross
                        
                        if self.data.loc[i, 'crossover'] == 1:
                            # Golden cross - confirm short still above long
                            if self.data.loc[future_idx, 'sma_short'] > self.data.loc[future_idx, 'sma_long']:
                                self.data.loc[future_idx, 'signal'] = 1
                        
                        elif self.data.loc[i, 'crossover'] == -1:
                            # Death cross - confirm short still below long
                            if self.data.loc[future_idx, 'sma_short'] < self.data.loc[future_idx, 'sma_long']:
                                self.data.loc[future_idx, 'signal'] = -1
        else:
            # No confirmation needed, use crossover directly
            self.data['signal'] = self.data['crossover']
        
        # Add signal strength (distance between MAs as percentage)
        self.data['signal_strength'] = (
            abs(self.data['sma_diff']) / self.data['close'] * 100
        )
        
        # Count valid signals (non-zero)
        buy_signals = (self.data['signal'] == 1).sum()
        sell_signals = (self.data['signal'] == -1).sum()
        
        logger.info(f"Generated {buy_signals} BUY and {sell_signals} SELL signals")
        
        return self.data
    
    def get_entry_exit_pairs(self) -> pd.DataFrame:
        """
        Match entry signals with their corresponding exit signals
        
        Returns:
            DataFrame with entry/exit pairs and potential profit
        """
        signals = self.data[self.data['signal'] != 0].copy()
        
        if len(signals) == 0:
            return pd.DataFrame()
        
        trades = []
        position = None
        entry_price = None
        entry_time = None
        entry_idx = None
        
        for idx, row in signals.iterrows():
            if position is None:
                # No open position - any signal can be an entry
                if row['signal'] == 1:
                    position = 'long'
                    entry_price = row['close']
                    entry_time = row['time']
                    entry_idx = idx
                elif row['signal'] == -1:
                    position = 'short'
                    entry_price = row['close']
                    entry_time = row['time']
                    entry_idx = idx
            
            else:
                # Have open position - check for exit
                if position == 'long' and row['signal'] == -1:
                    # Exit long position
                    pips_profit = (row['close'] - entry_price) * 10000
                    trades.append({
                        'entry_time': entry_time,
                        'entry_price': entry_price,
                        'exit_time': row['time'],
                        'exit_price': row['close'],
                        'position_type': 'long',
                        'pips_profit': pips_profit,
                        'percent_profit': ((row['close'] - entry_price) / entry_price) * 100
                    })
                    position = 'short'  # Reverse position
                    entry_price = row['close']
                    entry_time = row['time']
                    entry_idx = idx
                
                elif position == 'short' and row['signal'] == 1:
                    # Exit short position
                    pips_profit = (entry_price - row['close']) * 10000
                    trades.append({
                        'entry_time': entry_time,
                        'entry_price': entry_price,
                        'exit_time': row['time'],
                        'exit_price': row['close'],
                        'position_type': 'short',
                        'pips_profit': pips_profit,
                        'percent_profit': ((entry_price - row['close']) / entry_price) * 100
                    })
                    position = 'long'  # Reverse position
                    entry_price = row['close']
                    entry_time = row['time']
                    entry_idx = idx
        
        trades_df = pd.DataFrame(trades)
        
        if len(trades_df) > 0:
            logger.info(
                f"Found {len(trades_df)} complete trades. "
                f"Total pips: {trades_df['pips_profit'].sum():.1f}"
            )
        
        return trades_df
    
    def get_performance_summary(self) -> Dict:
        """
        Get detailed performance summary of the strategy
        
        Returns:
            Dictionary with performance metrics
        """
        trades = self.get_entry_exit_pairs()
        
        if len(trades) == 0:
            return {
                'total_trades': 0,
                'message': 'No complete trades found'
            }
        
        winning_trades = trades[trades['pips_profit'] > 0]
        losing_trades = trades[trades['pips_profit'] < 0]
        
        return {
            'total_trades': len(trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': len(winning_trades) / len(trades) * 100 if len(trades) > 0 else 0,
            'total_pips': trades['pips_profit'].sum(),
            'average_pips_per_trade': trades['pips_profit'].mean(),
            'best_trade_pips': trades['pips_profit'].max(),
            'worst_trade_pips': trades['pips_profit'].min(),
            'average_win_pips': winning_trades['pips_profit'].mean() if len(winning_trades) > 0 else 0,
            'average_loss_pips': losing_trades['pips_profit'].mean() if len(losing_trades) > 0 else 0,
            'profit_factor': abs(winning_trades['pips_profit'].sum() / losing_trades['pips_profit'].sum()) 
                           if len(losing_trades) > 0 and losing_trades['pips_profit'].sum() != 0 else float('inf'),
            'total_return_percent': trades['percent_profit'].sum()
        }
    
    def _format_signal_message(self, row: pd.Series) -> str:
        """
        Format signal message with SMA-specific information
        
        Args:
            row: DataFrame row
            
        Returns:
            Formatted message
        """
        signal = int(row['signal'])
        
        if signal == 1:
            return (
                f"BUY signal (Golden Cross): "
                f"SMA{self.short_period}={row['sma_short']:.5f} crossed above "
                f"SMA{self.long_period}={row['sma_long']:.5f} at price {row['close']:.5f}"
            )
        elif signal == -1:
            return (
                f"SELL signal (Death Cross): "
                f"SMA{self.short_period}={row['sma_short']:.5f} crossed below "
                f"SMA{self.long_period}={row['sma_long']:.5f} at price {row['close']:.5f}"
            )
        else:
            return f"No signal at {row['close']:.5f}"