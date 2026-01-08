# Forex Algorithmic Trading System

An educational forex trading algorithm built for academic investigation and learning. This project uses demo accounts to explore algorithmic trading strategies, risk management, and quantitative finance concepts without real financial risk.

## ⚠️ Disclaimer

This project is for **educational and research purposes only**. It uses demo/paper trading accounts with virtual money. This is not financial advice, and any strategies implemented here should never be used with real money without proper testing, validation, and understanding of risks involved.

## 🎯 Project Overview

This algorithmic trading system runs parallel experiments on two demo accounts:
- **Account A (Micro)**: $1,000 starting balance - testing viability for small retail traders
- **Account B (Small Retail)**: $5,000 starting balance - more breathing room for strategy execution

### Key Objectives

1. Build a functional algorithmic trading system from scratch
2. Understand forex market dynamics through hands-on development
3. Implement proper risk management and position sizing
4. Compare strategy performance across different account sizes
5. Learn real-time API integration and data handling
6. Develop backtesting and performance analytics capabilities

## 🏗️ Project Structure

```
forex-algo-trader/
├── README.md                 # This file
├── GOALS.md                  # Detailed project goals and milestones
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore rules
│
├── src/                     # Source code
│   ├── __init__.py
│   ├── api/                 # Broker API integrations
│   │   ├── __init__.py
│   │   └── oanda_client.py
│   ├── strategies/          # Trading strategies
│   │   ├── __init__.py
│   │   └── base_strategy.py
│   ├── risk/                # Risk management
│   │   ├── __init__.py
│   │   └── position_sizer.py
│   ├── backtesting/         # Backtesting framework
│   │   ├── __init__.py
│   │   └── backtest_engine.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── logger.py
│
├── data/                    # Historical and live data
│   ├── historical/
│   └── trades/
│
├── tests/                   # Unit tests
│   └── __init__.py
│
├── notebooks/               # Jupyter notebooks for analysis
│   └── exploratory_analysis.ipynb
│
├── config/                  # Configuration files
│   └── trading_config.yaml
│
├── logs/                    # Application logs
│
└── docs/                    # Additional documentation
    └── strategy_notes.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Git
- OANDA Practice Account (free)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/forex-algo-trader.git
cd forex-algo-trader
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OANDA practice account credentials
```

### Configuration

Create accounts at [OANDA Practice](https://www.oanda.com/us-en/trading/practice-account/) and obtain API credentials for both demo accounts.

Add credentials to `.env`:
```
OANDA_API_KEY_MICRO=your_api_key_here
OANDA_ACCOUNT_ID_MICRO=your_account_id_here
OANDA_API_KEY_RETAIL=your_api_key_here
OANDA_ACCOUNT_ID_RETAIL=your_account_id_here
OANDA_ENVIRONMENT=practice
```

## 📊 Usage

### Running the Trading System

```bash
python -m src.main
```

### Backtesting a Strategy

```bash
python -m src.backtesting.backtest_engine --strategy momentum --start 2024-01-01 --end 2024-12-31
```

### Running Tests

```bash
pytest tests/
```

## 🎓 Learning Objectives

This project serves as a hands-on learning platform for:

- **Quantitative Finance**: Understanding market indicators, technical analysis, and trading signals
- **Software Engineering**: Building robust, modular Python applications
- **API Integration**: Working with financial data APIs in real-time
- **Risk Management**: Implementing position sizing, stop losses, and portfolio management
- **Data Analysis**: Analyzing trading performance and making data-driven improvements
- **Version Control**: Professional Git workflow and documentation practices

## 📈 Current Status

- [x] Project structure and documentation
- [ ] OANDA API integration
- [ ] Basic data fetching and storage
- [ ] Simple moving average strategy
- [ ] Risk management module
- [ ] Backtesting framework
- [ ] Performance analytics dashboard
- [ ] Live paper trading execution

## 🤝 Contributing

This is primarily an educational project, but suggestions and improvements are welcome! Please open an issue to discuss potential changes.

## 📝 License

MIT License - See LICENSE file for details

## 📚 Resources

- [OANDA API Documentation](https://developer.oanda.com/rest-live-v20/introduction/)
- [Algorithmic Trading Guide](https://www.investopedia.com/articles/active-trading/101014/basics-algorithmic-trading-concepts-and-examples.asp)
- [Risk Management in Trading](https://www.investopedia.com/articles/trading/09/risk-management.asp)

## ⚡ Tech Stack

- **Python 3.9+**: Primary programming language
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **oandapyV20**: OANDA API client
- **pytest**: Testing framework
- **matplotlib/plotly**: Data visualization
- **PyYAML**: Configuration management

---

**Remember**: This is a learning project. Never trade with real money until you thoroughly understand the risks and have extensively tested any strategy.