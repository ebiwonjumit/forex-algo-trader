# Quick Start Guide

This guide will help you get the Forex Algorithmic Trading System up and running in under 15 minutes.

## Prerequisites Checklist

- [ ] Python 3.9 or higher installed
- [ ] Git installed
- [ ] Text editor or IDE (VS Code, PyCharm, etc.)
- [ ] OANDA practice account (we'll create this together)

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/forex-algo-trader.git
cd forex-algo-trader
```

## Step 2: Set Up Python Environment

### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 3: Create OANDA Practice Accounts

### Account A: $1,000 Micro Account

1. Go to [OANDA Practice Account](https://www.oanda.com/us-en/trading/practice-account/)
2. Sign up for a free practice account
3. Set initial balance to **$1,000**
4. Once created, go to "Manage API Access"
5. Generate an API key and save it securely

### Account B: $5,000 Small Retail Account

1. Create a second practice account (or reset the first one)
2. Set initial balance to **$5,000**
3. Generate another API key

**Important**: Keep these API keys private! Never commit them to git.

## Step 4: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your credentials:
```bash
# Account A: Micro Account ($1,000)
OANDA_API_KEY_MICRO=your_1k_account_api_key_here
OANDA_ACCOUNT_ID_MICRO=your_1k_account_id_here

# Account B: Small Retail Account ($5,000)
OANDA_API_KEY_RETAIL=your_5k_account_api_key_here
OANDA_ACCOUNT_ID_RETAIL=your_5k_account_id_here

OANDA_ENVIRONMENT=practice
```

## Step 5: Test the Connection

Run the connection test script:
```bash
python -m src.api.test_connection
```

You should see:
```
✓ Successfully connected to OANDA API
✓ Account A (Micro): Balance $1,000.00
✓ Account B (Retail): Balance $5,000.00
```

## Step 6: Fetch Historical Data

Download some historical data for backtesting:
```bash
python -m src.data.fetch_historical --pair EUR_USD --days 365
```

## Step 7: Run Your First Backtest

Test the SMA crossover strategy on historical data:
```bash
python -m src.backtesting.backtest_engine --strategy sma_crossover --account micro
```

## Step 8: Start Paper Trading (Optional)

Once you're comfortable with backtesting results:

1. Review the strategy in `config/trading_config.yaml`
2. Enable trading in `.env`:
   ```
   TRADING_ENABLED=true
   ```
3. Start the trading bot:
   ```bash
   python -m src.main
   ```

**Note**: This will execute trades on your demo accounts based on live market data!

## Common Issues

### Issue: "Module not found" errors
**Solution**: Make sure your virtual environment is activated and all requirements are installed.

### Issue: API connection fails
**Solution**: 
- Verify your API keys are correct
- Check that you're using the practice environment
- Ensure OANDA_ENVIRONMENT=practice in `.env`

### Issue: "Permission denied" on venv activation (Windows)
**Solution**: Run PowerShell as administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Next Steps

1. Read through `GOALS.md` to understand the project roadmap
2. Explore the `config/trading_config.yaml` to customize parameters
3. Check out `docs/strategy_notes.md` for strategy documentation
4. Join our discussions and share your findings!

## Getting Help

- Check the [README.md](README.md) for detailed documentation
- Review [GOALS.md](GOALS.md) for project objectives
- Open an issue on GitHub for bugs or questions

## Safety Reminders

- ✅ Always use practice accounts
- ✅ Never commit API keys to git
- ✅ Start with small position sizes
- ✅ Test thoroughly before live trading
- ❌ Never use real money until you fully understand the risks

---

**You're all set!** Start exploring the codebase and happy algorithmic trading (in demo mode)! 🚀