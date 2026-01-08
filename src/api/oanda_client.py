"""
OANDA API Client
Handles all interactions with the OANDA v20 REST API
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json

import oandapyV20
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.positions as positions

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OandaClient:
    """
    OANDA API client for algorithmic trading
    
    Attributes:
        account_type: 'micro' or 'retail' to specify which account to use
        api_key: OANDA API token
        account_id: OANDA account ID
        environment: 'practice' or 'live'
        client: oandapyV20 API client instance
    """
    
    def __init__(self, account_type: str = 'micro'):
        """
        Initialize OANDA API client
        
        Args:
            account_type: 'micro' for $1k account or 'retail' for $5k account
        """
        self.account_type = account_type.lower()
        
        # Load credentials based on account type
        if self.account_type == 'micro':
            self.api_key = os.getenv('OANDA_API_KEY_MICRO')
            self.account_id = os.getenv('OANDA_ACCOUNT_ID_MICRO')
        elif self.account_type == 'retail':
            self.api_key = os.getenv('OANDA_API_KEY_RETAIL')
            self.account_id = os.getenv('OANDA_ACCOUNT_ID_RETAIL')
        else:
            raise ValueError("account_type must be 'micro' or 'retail'")
        
        # Validate credentials
        if not self.api_key or not self.account_id:
            raise ValueError(
                f"Missing OANDA credentials for {account_type} account. "
                "Please check your .env file."
            )
        
        # Get environment (practice or live)
        self.environment = os.getenv('OANDA_ENVIRONMENT', 'practice').lower()
        
        # Initialize API client
        self.client = API(
            access_token=self.api_key,
            environment=self.environment
        )
        
        logger.info(
            f"Initialized OANDA client for {account_type} account "
            f"in {self.environment} environment"
        )
    
    def test_connection(self) -> Dict:
        """
        Test API connection and retrieve account information
        
        Returns:
            Dictionary with account details
        """
        try:
            # Request account details
            r = accounts.AccountDetails(accountID=self.account_id)
            response = self.client.request(r)
            
            account_info = response['account']
            
            logger.info(
                f"✓ Successfully connected to OANDA API\n"
                f"  Account ID: {account_info['id']}\n"
                f"  Balance: ${float(account_info['balance']):,.2f}\n"
                f"  Currency: {account_info['currency']}\n"
                f"  Open Trades: {len(account_info.get('trades', []))}\n"
                f"  Open Positions: {len(account_info.get('positions', []))}"
            )
            
            return {
                'success': True,
                'account_id': account_info['id'],
                'balance': float(account_info['balance']),
                'currency': account_info['currency'],
                'open_trades': len(account_info.get('trades', [])),
                'open_positions': len(account_info.get('positions', [])),
                'unrealized_pl': float(account_info.get('unrealizedPL', 0)),
                'nav': float(account_info.get('NAV', 0))
            }
            
        except V20Error as e:
            logger.error(f"✗ Failed to connect to OANDA API: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"✗ Unexpected error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_account_summary(self) -> Dict:
        """
        Get detailed account summary
        
        Returns:
            Dictionary with account summary
        """
        try:
            r = accounts.AccountSummary(accountID=self.account_id)
            response = self.client.request(r)
            return response['account']
        except V20Error as e:
            logger.error(f"Error fetching account summary: {e}")
            return {}
    
    def get_current_price(self, instrument: str = 'EUR_USD') -> Optional[Dict]:
        """
        Get current bid/ask prices for an instrument
        
        Args:
            instrument: Currency pair (e.g., 'EUR_USD')
            
        Returns:
            Dictionary with bid, ask, and mid prices
        """
        try:
            params = {
                'instruments': instrument
            }
            r = pricing.PricingInfo(accountID=self.account_id, params=params)
            response = self.client.request(r)
            
            price_data = response['prices'][0]
            
            return {
                'instrument': instrument,
                'time': price_data['time'],
                'bid': float(price_data['bids'][0]['price']),
                'ask': float(price_data['asks'][0]['price']),
                'mid': (float(price_data['bids'][0]['price']) + 
                       float(price_data['asks'][0]['price'])) / 2,
                'spread': float(price_data['asks'][0]['price']) - 
                         float(price_data['bids'][0]['price'])
            }
            
        except V20Error as e:
            logger.error(f"Error fetching price for {instrument}: {e}")
            return None
    
    def get_candles(
        self, 
        instrument: str = 'EUR_USD',
        granularity: str = 'H1',
        count: int = 500,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None
    ) -> List[Dict]:
        """
        Fetch historical candlestick data
        
        Args:
            instrument: Currency pair (e.g., 'EUR_USD')
            granularity: Timeframe (S5, M1, M5, M15, M30, H1, H4, D, W, M)
            count: Number of candles to fetch (max 5000)
            from_time: Start time in RFC3339 format
            to_time: End time in RFC3339 format
            
        Returns:
            List of candle dictionaries
        """
        try:
            params = {
                'granularity': granularity,
                'count': min(count, 5000)  # OANDA max is 5000
            }
            
            if from_time:
                params['from'] = from_time
            if to_time:
                params['to'] = to_time
            
            r = instruments.InstrumentsCandles(instrument=instrument, params=params)
            response = self.client.request(r)
            
            candles = []
            for candle in response['candles']:
                if candle['complete']:  # Only use complete candles
                    candles.append({
                        'time': candle['time'],
                        'volume': int(candle['volume']),
                        'open': float(candle['mid']['o']),
                        'high': float(candle['mid']['h']),
                        'low': float(candle['mid']['l']),
                        'close': float(candle['mid']['c'])
                    })
            
            logger.info(
                f"Fetched {len(candles)} candles for {instrument} "
                f"({granularity})"
            )
            
            return candles
            
        except V20Error as e:
            logger.error(f"Error fetching candles: {e}")
            return []
    
    def place_market_order(
        self,
        instrument: str,
        units: int,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None
    ) -> Dict:
        """
        Place a market order
        
        Args:
            instrument: Currency pair (e.g., 'EUR_USD')
            units: Number of units (positive for buy, negative for sell)
            stop_loss: Stop loss price
            take_profit: Take profit price
            
        Returns:
            Order response dictionary
        """
        try:
            order_data = {
                'order': {
                    'type': 'MARKET',
                    'instrument': instrument,
                    'units': str(units),
                    'timeInForce': 'FOK',  # Fill or Kill
                    'positionFill': 'DEFAULT'
                }
            }
            
            # Add stop loss if specified
            if stop_loss:
                order_data['order']['stopLossOnFill'] = {
                    'price': str(stop_loss)
                }
            
            # Add take profit if specified
            if take_profit:
                order_data['order']['takeProfitOnFill'] = {
                    'price': str(take_profit)
                }
            
            r = orders.OrderCreate(accountID=self.account_id, data=order_data)
            response = self.client.request(r)
            
            logger.info(
                f"Order placed: {units} units of {instrument} "
                f"(Order ID: {response['orderFillTransaction']['id']})"
            )
            
            return {
                'success': True,
                'order_id': response['orderFillTransaction']['id'],
                'instrument': instrument,
                'units': units,
                'price': float(response['orderFillTransaction']['price']),
                'time': response['orderFillTransaction']['time']
            }
            
        except V20Error as e:
            logger.error(f"Error placing order: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_open_trades(self) -> List[Dict]:
        """
        Get all open trades
        
        Returns:
            List of open trade dictionaries
        """
        try:
            r = trades.OpenTrades(accountID=self.account_id)
            response = self.client.request(r)
            
            open_trades = []
            for trade in response.get('trades', []):
                open_trades.append({
                    'id': trade['id'],
                    'instrument': trade['instrument'],
                    'price': float(trade['price']),
                    'open_time': trade['openTime'],
                    'current_units': int(trade['currentUnits']),
                    'unrealized_pl': float(trade['unrealizedPL']),
                    'initial_units': int(trade['initialUnits'])
                })
            
            return open_trades
            
        except V20Error as e:
            logger.error(f"Error fetching open trades: {e}")
            return []
    
    def close_trade(self, trade_id: str) -> Dict:
        """
        Close an open trade
        
        Args:
            trade_id: Trade ID to close
            
        Returns:
            Close response dictionary
        """
        try:
            r = trades.TradeClose(accountID=self.account_id, tradeID=trade_id)
            response = self.client.request(r)
            
            logger.info(f"Trade {trade_id} closed")
            
            return {
                'success': True,
                'trade_id': trade_id,
                'realized_pl': float(
                    response['orderFillTransaction']['pl']
                )
            }
            
        except V20Error as e:
            logger.error(f"Error closing trade {trade_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_open_positions(self) -> List[Dict]:
        """
        Get all open positions
        
        Returns:
            List of position dictionaries
        """
        try:
            r = positions.OpenPositions(accountID=self.account_id)
            response = self.client.request(r)
            
            positions_list = []
            for position in response.get('positions', []):
                positions_list.append({
                    'instrument': position['instrument'],
                    'long_units': int(position['long']['units']),
                    'long_pl': float(position['long']['unrealizedPL']),
                    'short_units': int(position['short']['units']),
                    'short_pl': float(position['short']['unrealizedPL']),
                    'total_pl': float(position['unrealizedPL'])
                })
            
            return positions_list
            
        except V20Error as e:
            logger.error(f"Error fetching positions: {e}")
            return []


def main():
    """
    Test the OANDA client connection
    """
    print("=" * 60)
    print("OANDA API Connection Test")
    print("=" * 60)
    
    # Test both accounts
    for account_type in ['micro', 'retail']:
        print(f"\n{'='*60}")
        print(f"Testing {account_type.upper()} Account")
        print(f"{'='*60}\n")
        
        try:
            client = OandaClient(account_type=account_type)
            
            # Test connection
            result = client.test_connection()
            
            if result['success']:
                print(f"✓ Connection successful!")
                print(f"  Balance: ${result['balance']:,.2f}")
                print(f"  Currency: {result['currency']}")
                print(f"  NAV: ${result['nav']:,.2f}")
                
                # Get current EUR/USD price
                print("\nFetching current EUR/USD price...")
                price = client.get_current_price('EUR_USD')
                if price:
                    print(f"  Bid: {price['bid']:.5f}")
                    print(f"  Ask: {price['ask']:.5f}")
                    print(f"  Spread: {price['spread']:.5f}")
                
                # Fetch some historical data
                print("\nFetching last 5 H1 candles...")
                candles = client.get_candles('EUR_USD', 'H1', count=5)
                if candles:
                    print(f"  Retrieved {len(candles)} candles")
                    latest = candles[-1]
                    print(f"  Latest close: {latest['close']:.5f}")
                    print(f"  Time: {latest['time']}")
                
            else:
                print(f"✗ Connection failed: {result.get('error')}")
                
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print(f"\n{'='*60}")
    print("Test Complete!")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()