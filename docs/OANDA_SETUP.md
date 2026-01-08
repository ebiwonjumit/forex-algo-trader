# Setting Up OANDA API Connection

## What We've Built

You now have a complete OANDA API client that can:

✅ Connect to both demo accounts (micro and retail)  
✅ Fetch account information and balances  
✅ Get real-time prices  
✅ Retrieve historical candlestick data  
✅ Place market orders (buy/sell)  
✅ Manage open trades and positions  

## Files Created

1. **`src/api/oanda_client.py`** - Main OANDA API client
2. **`tests/test_connection.py`** - Connection test script
3. **`scripts/fetch_data.py`** - Historical data downloader

## Setup Steps

### Step 1: Get Your OANDA API Credentials

1. Go to https://www.oanda.com/us-en/trading/practice-account/
2. Sign up or log in
3. Create **TWO** demo accounts:
   
   **Account A (Micro - $1,000)**:
   - Click "Create Demo Account" or similar
   - Set balance to $1,000
   - Go to Settings → API Access → Generate Token
   - Copy your API Token and Account ID
   
   **Account B (Retail - $5,000)**:
   - Create a second demo account
   - Set balance to $5,000
   - Generate another API Token
   - Copy your API Token and Account ID

### Step 2: Configure Your Environment

Create a `.env` file in your project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your credentials:

```
# Account A: Micro Account ($1,000)
OANDA_API_KEY_MICRO=abc123your_api_key_here_micro
OANDA_ACCOUNT_ID_MICRO=123-456-7890123-001

# Account B: Small Retail Account ($5,000)
OANDA_API_KEY_RETAIL=xyz789your_api_key_here_retail
OANDA_ACCOUNT_ID_RETAIL=123-456-7890123-002

# Environment (ALWAYS use practice!)
OANDA_ENVIRONMENT=practice

# Risk Management Settings
MAX_RISK_PER_TRADE_PCT=0.02
MAX_DAILY_LOSS_PCT=0.05
MAX_OPEN_POSITIONS=3

# Trading Settings
DEFAULT_CURRENCY_PAIR=EUR_USD
TRADING_ENABLED=false

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/trading.log
```

**⚠️ IMPORTANT**: 
- Never commit this file to git (it's already in .gitignore)
- Always use `practice` environment, never `live`!

### Step 3: Install Dependencies

```bash
# Activate your virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 4: Test Your Connection

Run the connection test:

```bash
python tests/test_connection.py
```

You should see output like:

```
======================================================================
 OANDA API CONNECTION TEST
======================================================================

──────────────────────────────────────────────────────────────────────
 Testing MICRO Account ($1000)
──────────────────────────────────────────────────────────────────────

✓ SUCCESS - Connected to micro account
  └─ Balance: $1,000.00
  └─ Account ID: 123-456-7890123-001
  └─ Open Trades: 0
  └─ Unrealized P/L: $0.00

  Fetching EUR/USD price...
  ✓ Current Price:
    └─ Bid: 1.08234
    └─ Ask: 1.08248
    └─ Spread: 0.00014 (1.4 pips)

──────────────────────────────────────────────────────────────────────
 Testing RETAIL Account ($5000)
──────────────────────────────────────────────────────────────────────

✓ SUCCESS - Connected to retail account
  └─ Balance: $5,000.00
  └─ Account ID: 123-456-7890123-002
  └─ Open Trades: 0
  └─ Unrealized P/L: $0.00

  Fetching EUR/USD price...
  ✓ Current Price:
    └─ Bid: 1.08234
    └─ Ask: 1.08248
    └─ Spread: 0.00014 (1.4 pips)

======================================================================
 TEST SUMMARY
======================================================================
  Accounts Tested: 2
  Successful: 2
  Failed: 0

  ✓ All accounts connected successfully!
  You're ready to start trading (in demo mode)!
======================================================================
```

### Step 5: Fetch Historical Data

Download historical data for backtesting:

```bash
# Fetch 1 year of hourly EUR/USD data
python scripts/fetch_data.py --pair EUR_USD --granularity H1 --days 365

# Or fetch daily data
python scripts/fetch_data.py --pair EUR_USD --granularity D --days 365

# Fetch data for a different pair
python scripts/fetch_data.py --pair GBP_USD --granularity H1 --days 180
```

This will save CSV files to `data/historical/`.

## Testing the API Client

You can also test the client directly in Python:

```python
from src.api.oanda_client import OandaClient

# Initialize client for micro account
client = OandaClient(account_type='micro')

# Test connection
result = client.test_connection()
print(f"Balance: ${result['balance']}")

# Get current price
price = client.get_current_price('EUR_USD')
print(f"EUR/USD: {price['bid']} / {price['ask']}")

# Get historical data
candles = client.get_candles('EUR_USD', 'H1', count=100)
print(f"Fetched {len(candles)} candles")
```

## Troubleshooting

### Error: "Missing OANDA credentials"

**Solution**: Make sure your `.env` file exists and contains all required variables.

### Error: "V20Error: Unauthorized"

**Solution**: 
- Check that your API key is correct
- Verify you're using the practice environment
- Make sure the API key matches the account ID

### Error: "Unable to fetch data"

**Solution**:
- Check your internet connection
- Verify the instrument name (use underscore: EUR_USD, not EUR/USD)
- Ensure the market is open (forex markets close on weekends)

### Error: "ModuleNotFoundError: No module named 'oandapyV20'"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

## What's Next?

Now that you have a working API connection, you can:

1. **Explore the API** - Try different methods in `oanda_client.py`
2. **Analyze Historical Data** - Load CSV files and visualize patterns
3. **Build Trading Strategy** - Start implementing the SMA crossover strategy (Phase 2)
4. **Backtest** - Test your strategy on historical data
5. **Paper Trade** - Deploy to live demo accounts

## Security Reminders

🔒 **Keep Your Credentials Safe**:
- Never share your API keys
- Never commit `.env` to git
- Use practice accounts only for this project
- Regenerate keys if you suspect they're compromised

---

**Ready to build your first trading strategy?** Let's move to Phase 2! 🚀