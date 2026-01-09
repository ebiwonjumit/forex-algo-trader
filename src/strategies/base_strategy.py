"""
Base Strategy Class
All trading strategies inherit from this class
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies
    
    All strategies must implement:
    - calculate_indicators()
    - generate_signals()
    """
    
    def __init__(self, name: str, parameters: Optional[Dict] = None):
        """
        Initialize strategy
        
        Args:
            name: Strategy name
            parameters: Strategy-specific parameters
        """
        self.name = name
        self.parameters = parameters or {}
        self.data = None
        self.signals = None
        
        logger.info(f"Initialized strategy: {name}")
        if self.parameters:
            logger.info(f"Parameters: {self.parameters}")
    
    def load_data(self, data: pd.DataFrame) -> None:
        """
        Load price data into the strategy
        
        Args:
            data: DataFrame with OHLC data (columns: time, open, high, low, close, volume)
        """
        required_columns = ['time', 'open', 'high', 'low', 'close', 'volume']
        
        # Validate data
        if not all(col in data.columns for col in required_columns):
            missing = [col for col in required_columns if col not in data.columns]
            raise ValueError(f"Data missing required columns: {missing}")
        
        # Make a copy and ensure time is datetime
        self.data = data.copy()
        if not pd.api.types.is_datetime64_any_dtype(self.data['time']):
            self.data['time'] = pd.to_datetime(self.data['time'])
        
        # Sort by time
        self.data = self.data.sort_values('time').reset_index(drop=True)
        
        logger.info(
            f"Loaded {len(self.data)} candles "
            f"from {self.data['time'].min()} to {self.data['time'].max()}"
        )
    
    @abstractmethod
    def calculate_indicators(self) -> pd.DataFrame:
        """
        Calculate technical indicators
        
        Must be implemented by each strategy
        
        Returns:
            DataFrame with indicators added
        """
        pass
    
    @abstractmethod
    def generate_signals(self) -> pd.DataFrame:
        """
        Generate trading signals based on indicators
        
        Must be implemented by each strategy
        
        Returns:
            DataFrame with signals column (1 = buy, -1 = sell, 0 = hold)
        """
        pass
    
    def run(self) -> pd.DataFrame:
        """
        Run the complete strategy: calculate indicators and generate signals
        
        Returns:
            DataFrame with indicators and signals
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        logger.info(f"Running strategy: {self.name}")
        
        # Calculate indicators
        self.data = self.calculate_indicators()
        
        # Generate signals
        self.signals = self.generate_signals()
        
        # Count signals
        buy_signals = (self.signals['signal'] == 1).sum()
        sell_signals = (self.signals['signal'] == -1).sum()
        
        logger.info(
            f"Strategy complete: {buy_signals} buy signals, "
            f"{sell_signals} sell signals"
        )
        
        return self.signals
    
    def get_latest_signal(self) -> Dict:
        """
        Get the most recent signal
        
        Returns:
            Dictionary with latest signal information
        """
        if self.signals is None or len(self.signals) == 0:
            return {
                'signal': 0,
                'time': None,
                'price': None,
                'message': 'No signals generated'
            }
        
        latest = self.signals.iloc[-1]
        
        signal_map = {
            1: 'BUY',
            -1: 'SELL',
            0: 'HOLD'
        }
        
        return {
            'signal': int(latest['signal']),
            'signal_name': signal_map.get(int(latest['signal']), 'UNKNOWN'),
            'time': latest['time'],
            'price': latest['close'],
            'message': self._format_signal_message(latest)
        }
    
    def _format_signal_message(self, row: pd.Series) -> str:
        """
        Format a human-readable signal message
        
        Args:
            row: DataFrame row with signal information
            
        Returns:
            Formatted message string
        """
        signal = int(row['signal'])
        
        if signal == 1:
            return f"BUY signal at {row['close']:.5f} on {row['time']}"
        elif signal == -1:
            return f"SELL signal at {row['close']:.5f} on {row['time']}"
        else:
            return f"HOLD at {row['close']:.5f} on {row['time']}"
    
    def get_all_signals(self, signal_type: Optional[int] = None) -> pd.DataFrame:
        """
        Get all signals or filter by type
        
        Args:
            signal_type: Filter by signal (1 = buy, -1 = sell, 0 = hold, None = all)
            
        Returns:
            DataFrame with filtered signals
        """
        if self.signals is None:
            return pd.DataFrame()
        
        if signal_type is not None:
            return self.signals[self.signals['signal'] == signal_type].copy()
        
        return self.signals[self.signals['signal'] != 0].copy()
    
    def get_summary(self) -> Dict:
        """
        Get strategy summary statistics
        
        Returns:
            Dictionary with summary statistics
        """
        if self.signals is None:
            return {}
        
        buy_signals = (self.signals['signal'] == 1).sum()
        sell_signals = (self.signals['signal'] == -1).sum()
        total_signals = buy_signals + sell_signals
        
        return {
            'strategy_name': self.name,
            'parameters': self.parameters,
            'data_points': len(self.data) if self.data is not None else 0,
            'date_range': {
                'start': self.data['time'].min() if self.data is not None else None,
                'end': self.data['time'].max() if self.data is not None else None
            },
            'signals': {
                'total': total_signals,
                'buy': buy_signals,
                'sell': sell_signals,
                'buy_percentage': (buy_signals / total_signals * 100) if total_signals > 0 else 0,
                'sell_percentage': (sell_signals / total_signals * 100) if total_signals > 0 else 0
            }
        }
    
    def export_signals(self, filepath: str) -> None:
        """
        Export signals to CSV file
        
        Args:
            filepath: Path to save CSV file
        """
        if self.signals is None:
            raise ValueError("No signals to export. Run the strategy first.")
        
        # Only export rows with actual signals (not holds)
        signal_data = self.signals[self.signals['signal'] != 0].copy()
        signal_data.to_csv(filepath, index=False)
        
        logger.info(f"Exported {len(signal_data)} signals to {filepath}")
    
    def __repr__(self) -> str:
        """String representation of strategy"""
        return f"{self.__class__.__name__}(name='{self.name}', parameters={self.parameters})"


class TechnicalIndicators:
    """
    Collection of common technical indicators
    Static methods that can be used by any strategy
    """
    
    @staticmethod
    def sma(data: pd.Series, period: int) -> pd.Series:
        """
        Simple Moving Average
        
        Args:
            data: Price series (usually close price)
            period: Number of periods
            
        Returns:
            SMA series
        """
        return data.rolling(window=period, min_periods=period).mean()
    
    @staticmethod
    def ema(data: pd.Series, period: int) -> pd.Series:
        """
        Exponential Moving Average
        
        Args:
            data: Price series
            period: Number of periods
            
        Returns:
            EMA series
        """
        return data.ewm(span=period, adjust=False, min_periods=period).mean()
    
    @staticmethod
    def rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """
        Relative Strength Index
        
        Args:
            data: Price series
            period: Number of periods (default: 14)
            
        Returns:
            RSI series
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Average True Range
        
        Args:
            high: High price series
            low: Low price series
            close: Close price series
            period: Number of periods (default: 14)
            
        Returns:
            ATR series
        """
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period, min_periods=period).mean()
        
        return atr
    
    @staticmethod
    def bollinger_bands(data: pd.Series, period: int = 20, num_std: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Bollinger Bands
        
        Args:
            data: Price series
            period: Number of periods (default: 20)
            num_std: Number of standard deviations (default: 2.0)
            
        Returns:
            Tuple of (middle_band, upper_band, lower_band)
        """
        middle_band = data.rolling(window=period, min_periods=period).mean()
        std = data.rolling(window=period, min_periods=period).std()
        
        upper_band = middle_band + (std * num_std)
        lower_band = middle_band - (std * num_std)
        
        return middle_band, upper_band, lower_band
    
    @staticmethod
    def macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        MACD (Moving Average Convergence Divergence)
        
        Args:
            data: Price series
            fast: Fast EMA period (default: 12)
            slow: Slow EMA period (default: 26)
            signal: Signal line period (default: 9)
            
        Returns:
            Tuple of (macd_line, signal_line, histogram)
        """
        ema_fast = data.ewm(span=fast, adjust=False).mean()
        ema_slow = data.ewm(span=slow, adjust=False).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram