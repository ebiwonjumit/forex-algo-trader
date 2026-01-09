# Algorithmic Forex Trading System: A Comparative Study of Account Size Impact on Strategy Performance

## White Paper

**Version:** 1.0  
**Date:** January 2025  
**Authors:** Forex Algo Trader Research Team  
**Status:** Educational Research Project

---

## Abstract

This paper presents the design, implementation, and analysis of an algorithmic forex trading system developed for educational purposes. The primary research objective is to empirically investigate how initial account capitalization affects trading strategy performance and risk-adjusted returns in the foreign exchange market. Using OANDA's practice trading environment, we deploy identical algorithmic strategies across two accounts with different starting balances ($1,000 vs. $5,000) to quantify the relationship between account size and trading outcomes. This comparative study employs a simple moving average (SMA) crossover strategy as the foundational algorithm, with plans to expand to additional technical indicators and strategies. All trading is conducted in a simulated environment using virtual capital to ensure no financial risk while maintaining realistic market conditions.

**Keywords:** Algorithmic Trading, Foreign Exchange, Moving Average Crossover, Account Size Impact, Risk Management, Quantitative Finance

---

## 1. Introduction

### 1.1 Background

The foreign exchange (forex) market is the largest and most liquid financial market globally, with an average daily trading volume exceeding $7.5 trillion as of 2022 [1]. The emergence of algorithmic trading has democratized access to forex markets, enabling retail traders to implement systematic, rule-based strategies previously available only to institutional investors [2]. However, a critical question remains underexplored in retail trading literature: how does initial account capitalization affect the viability and performance of algorithmic trading strategies?

### 1.2 Research Motivation

Retail forex traders typically begin with modest capital, often between $1,000 and $10,000 [3]. While institutional literature extensively covers portfolio optimization and risk management for large capital bases, limited empirical research exists on how algorithmic strategies perform under capital constraints typical of retail traders. This knowledge gap is particularly significant given that:

1. **Position Sizing Constraints**: Smaller accounts face greater limitations in position sizing and diversification
2. **Risk Management Challenges**: Fixed costs (spreads, slippage) represent a larger percentage of small accounts
3. **Psychological Factors**: Account size may influence strategy adherence and risk tolerance
4. **Scalability Questions**: Whether strategies scale linearly with capital remains an open question

### 1.3 Research Objectives

This project pursues three primary objectives:

**Primary Objective:**
Quantitatively assess how starting capital ($1,000 vs. $5,000) affects the performance of identical algorithmic trading strategies in forex markets.

**Secondary Objectives:**
1. Implement and validate a robust algorithmic trading system using industry-standard APIs and practices
2. Develop a comprehensive backtesting framework that accounts for realistic trading costs
3. Establish best practices for risk management in retail algorithmic trading
4. Create reproducible, open-source tools for algorithmic trading education

### 1.4 Scope and Limitations

**Scope:**
- Focus on EUR/USD currency pair (most liquid forex pair)
- Hourly timeframe (H1) for primary analysis
- Demo/practice trading environment (no real capital at risk)
- 12-week development and testing period

**Limitations:**
- Results are limited to the specific strategies and timeframes tested
- Practice environment may not perfectly replicate live market conditions
- Limited to technical analysis; does not incorporate fundamental analysis
- Single currency pair focus limits generalizability
- Historical performance does not guarantee future results

---

## 2. Literature Review and Theoretical Foundation

### 2.1 Algorithmic Trading in Forex Markets

Algorithmic trading, defined as the use of computer programs to execute trading strategies based on predetermined rules [4], has grown exponentially since the early 2000s. In forex markets specifically, algorithmic trading now accounts for an estimated 70-80% of total trading volume [5].

**Key Advantages of Algorithmic Trading:**
- Eliminates emotional decision-making
- Enables consistent strategy execution
- Allows for rapid backtesting and optimization
- Facilitates 24/7 market monitoring
- Reduces human error and bias

**Challenges in Retail Algorithmic Trading:**
- Limited capital for diversification
- Higher relative transaction costs
- Technology and infrastructure requirements
- Over-optimization risks (curve fitting)
- Market regime changes

### 2.2 Moving Average Strategies

Moving averages are among the most widely studied and implemented technical indicators in financial markets [6]. The simple moving average (SMA) crossover strategy has been documented in academic literature since the 1960s and remains popular due to its simplicity and trend-following nature [7].

**Theoretical Foundation:**

The efficient market hypothesis (EMH) suggests that technical trading strategies should not generate excess returns in efficient markets [8]. However, behavioral finance research has identified persistent market patterns driven by:
- Herding behavior [9]
- Momentum effects [10]
- Under-reaction to information [11]

These behavioral anomalies create the theoretical basis for trend-following strategies like moving average crossovers.

**Academic Evidence:**

Brock, Lakonishok, and LeBaron (1992) [12] found that moving average strategies generated significant excess returns in stock markets from 1897-1986, though these returns diminished in later periods. In forex markets, research presents mixed results:

- **Supporting Evidence**: Neely, Weller, and Dittmar (1997) [13] found genetic algorithm-optimized technical rules profitable in forex markets
- **Contradicting Evidence**: Olson (2004) [14] found that simple technical rules did not outperform buy-and-hold strategies after transaction costs
- **Recent Studies**: Hsu et al. (2016) [15] demonstrated that moving average strategies can be profitable in trending markets but struggle in ranging conditions

### 2.3 Account Size and Trading Performance

Limited academic research directly addresses the relationship between account size and trading performance in retail markets. However, related research provides relevant insights:

**Transaction Cost Impact:**
Locke and Mann (2005) [16] demonstrated that transaction costs represent a significantly higher percentage of returns for small traders, potentially eroding profitability.

**Position Sizing:**
Kelly Criterion research [17] suggests optimal position sizing should be proportional to edge and inversely proportional to volatility. Smaller accounts face greater constraints in implementing optimal position sizing.

**Drawdown Recovery:**
Mathematical studies [18] show that drawdown recovery becomes increasingly difficult as percentage losses increase, suggesting that capital preservation is more critical for smaller accounts.

### 2.4 Risk Management in Algorithmic Trading

Modern portfolio theory and risk management principles [19] emphasize:

1. **Position Sizing**: Never risk more than 1-2% of capital per trade
2. **Stop Loss Discipline**: Systematic use of stop losses to limit downside
3. **Diversification**: Spreading risk across uncorrelated positions
4. **Maximum Drawdown Limits**: Circuit breakers to stop trading during adverse conditions

Van Tharp's position sizing research [20] suggests that proper position sizing accounts for more than 80% of trading success, more than strategy selection itself.

---

## 3. Methodology

### 3.1 System Architecture

Our algorithmic trading system consists of five primary components:

```
┌─────────────────────────────────────────────────────────────┐
│                    System Architecture                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │  OANDA API   │◄────►│ Data Module  │                    │
│  │  Interface   │      │              │                    │
│  └──────────────┘      └──────┬───────┘                    │
│                               │                             │
│                               ▼                             │
│                     ┌──────────────────┐                    │
│                     │ Strategy Engine  │                    │
│                     │  - Base Class    │                    │
│                     │  - SMA Crossover │                    │
│                     │  - Indicators    │                    │
│                     └────────┬─────────┘                    │
│                              │                              │
│                              ▼                              │
│                  ┌────────────────────────┐                 │
│                  │  Risk Management       │                 │
│                  │  - Position Sizing     │                 │
│                  │  - Stop Loss/Take Prof │                 │
│                  │  - Drawdown Limits     │                 │
│                  └──────────┬─────────────┘                 │
│                             │                               │
│                             ▼                               │
│              ┌──────────────────────────────┐               │
│              │  Execution Module            │               │
│              │  - Order Placement           │               │
│              │  - Trade Management          │               │
│              └──────────┬───────────────────┘               │
│                         │                                   │
│                         ▼                                   │
│          ┌────────────────────────────────┐                 │
│          │  Analysis & Reporting          │                 │
│          │  - Performance Metrics         │                 │
│          │  - Comparative Analysis        │                 │
│          └────────────────────────────────┘                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Trading Accounts

**Account A: Micro Account**
- Starting Balance: $1,000 USD
- Maximum Risk per Trade: 2% ($20)
- Position Size: Micro lots (1,000 units)
- Purpose: Representative of entry-level retail traders

**Account B: Small Retail Account**
- Starting Balance: $5,000 USD
- Maximum Risk per Trade: 2% ($100)
- Position Size: Mini lots (10,000 units)
- Purpose: Representative of modest retail trading capital

Both accounts use identical:
- Trading strategies
- Risk parameters (percentage-based)
- Entry/exit rules
- Stop loss and take profit logic

### 3.3 Primary Strategy: SMA Crossover

#### 3.3.1 Algorithm Description

The Simple Moving Average (SMA) crossover strategy generates signals based on the relationship between two moving averages of different periods.

**Mathematical Definition:**

For a price series P = {p₁, p₂, ..., pₙ}, the Simple Moving Average of period m is:

```
SMA(m,t) = (1/m) × Σ(pₜ₋ᵢ) for i = 0 to m-1
```

We use two SMAs:
- **Short SMA**: Period = 20 (fast-moving average)
- **Long SMA**: Period = 50 (slow-moving average)

**Signal Generation Rules:**

1. **Golden Cross (BUY Signal)**:
   - Occurs when: SMA(20) crosses above SMA(50)
   - Condition: SMA(20,t) > SMA(50,t) AND SMA(20,t-1) ≤ SMA(50,t-1)
   - Interpretation: Short-term momentum exceeds long-term trend

2. **Death Cross (SELL Signal)**:
   - Occurs when: SMA(20) crosses below SMA(50)
   - Condition: SMA(20,t) < SMA(50,t) AND SMA(20,t-1) ≥ SMA(50,t-1)
   - Interpretation: Short-term momentum falls below long-term trend

3. **Exit Rules**:
   - Exit on opposite signal (crossover in reverse direction)
   - Optional: Stop loss at 2× ATR (Average True Range)
   - Optional: Take profit at 2:1 risk-reward ratio

#### 3.3.2 Theoretical Justification

The SMA crossover strategy exploits:

1. **Trend Persistence**: Markets exhibit momentum, where trends tend to continue [10]
2. **Moving Average Support/Resistance**: MAs act as dynamic support/resistance levels [21]
3. **Noise Reduction**: Longer-period MAs smooth out market noise

**Advantages:**
- Simple to implement and understand
- Well-documented in academic literature
- Widely used, creating self-fulfilling prophecies
- Clearly defined entry/exit rules

**Disadvantages:**
- Lagging indicator (late entries/exits)
- Poor performance in ranging markets
- Vulnerable to whipsaws (false signals)
- No inherent position sizing logic

#### 3.3.3 Parameter Selection

**SMA Periods (20/50):**
These periods are selected based on:
- Industry standard practice [22]
- Approximately 1 month vs. 2.5 months of trading days
- Balance between responsiveness and smoothness
- Will be tested against alternatives (10/30, 50/200)

### 3.4 Additional Strategies (Future Implementation)

#### 3.4.1 RSI Mean Reversion

**Algorithm**: Relative Strength Index (RSI) [23]

```
RSI = 100 - (100 / (1 + RS))
where RS = Average Gain / Average Loss over n periods
```

**Signals**:
- BUY when RSI < 30 (oversold)
- SELL when RSI > 70 (overbought)

**Source**: J. Welles Wilder, "New Concepts in Technical Trading Systems" (1978)

#### 3.4.2 Bollinger Band Breakout

**Algorithm**: Bollinger Bands [24]

```
Middle Band = SMA(20)
Upper Band = SMA(20) + (2 × σ)
Lower Band = SMA(20) - (2 × σ)
```

**Signals**:
- BUY on breakout above upper band
- SELL on breakdown below lower band

**Source**: John Bollinger, "Bollinger on Bollinger Bands" (2001)

#### 3.4.3 MACD Convergence/Divergence

**Algorithm**: Moving Average Convergence Divergence [25]

```
MACD Line = EMA(12) - EMA(26)
Signal Line = EMA(9) of MACD Line
Histogram = MACD Line - Signal Line
```

**Signals**:
- BUY when MACD crosses above Signal Line
- SELL when MACD crosses below Signal Line

**Source**: Gerald Appel, "Technical Analysis: Power Tools for Active Investors" (2005)

### 3.5 Risk Management Framework

Our risk management system implements multiple layers of protection:

#### 3.5.1 Position Sizing

**Fixed Percentage Risk Model:**

```
Position Size = (Account Balance × Risk%) / (Entry Price - Stop Loss Price)
```

Where:
- Risk% = 2% maximum per trade
- Stop Loss placed at 2× ATR or technical level

**Rationale**: This approach ensures consistent risk per trade regardless of market volatility or account size.

#### 3.5.2 Stop Loss Implementation

**Methods**:
1. **ATR-Based**: Stop = Entry ± (2 × ATR₁₄)
2. **Fixed Pips**: Stop = Entry ± 50 pips
3. **Technical**: Stop at recent swing high/low

**Default**: ATR-based (adapts to market volatility)

#### 3.5.3 Take Profit Targets

**Risk-Reward Ratio Approach:**

```
Take Profit Distance = Stop Loss Distance × Risk:Reward Ratio
```

**Default**: 2:1 risk-reward ratio
- If risking 50 pips, target 100 pips profit
- Ensures profitability even with <50% win rate

#### 3.5.4 Portfolio-Level Risk Controls

1. **Maximum Drawdown Limit**: 20%
   - Trading suspended if account drops 20% from peak
   
2. **Daily Loss Limit**: 5%
   - No new trades if daily loss exceeds 5%
   
3. **Maximum Concurrent Positions**: 3
   - Prevents over-concentration
   
4. **Correlation Limits**: (Future)
   - Avoid highly correlated currency pairs

### 3.6 Data Collection and Storage

**Data Source**: OANDA v20 REST API

**Primary Data**:
- OHLC (Open, High, Low, Close) candlestick data
- Hourly timeframe (H1)
- 365 days of historical data for backtesting
- Real-time pricing for live paper trading

**Storage**:
- Historical data: CSV format in `data/historical/`
- Trade logs: CSV format in `data/trades/`
- Performance metrics: JSON format

**Data Quality Controls**:
- Validation of OHLC relationships (H≥O,H≥C,H≥L,L≤O,L≤C)
- Duplicate removal
- Missing data interpolation (forward fill)
- Outlier detection (> 3σ from mean)

### 3.7 Backtesting Methodology

#### 3.7.1 Backtesting Framework

Our backtesting engine simulates trading on historical data while accounting for realistic costs:

**Transaction Costs**:
- Spread: 2 pips for EUR/USD (typical retail spread)
- Slippage: 1 pip average (conservative estimate)
- Commission: $0 (spread-based pricing)

**Execution Assumptions**:
- Orders filled at next candle open after signal
- Stop losses and take profits assumed filled at exact levels
- No partial fills
- 100% order fill rate (optimistic for demo)

#### 3.7.2 Performance Metrics

We evaluate strategies using multiple metrics:

**Return Metrics**:
- Total Return (%): Net profit / Initial capital
- Annualized Return (%): Scaled to per-year basis
- Return per Trade: Average profit per trade

**Risk Metrics**:
- Maximum Drawdown (%): Largest peak-to-trough decline
- Sharpe Ratio: (Return - Risk-Free Rate) / Volatility
- Sortino Ratio: Return / Downside Deviation

**Consistency Metrics**:
- Win Rate (%): Winning trades / Total trades
- Profit Factor: Gross Profit / Gross Loss
- Average Win / Average Loss ratio
- Consecutive Wins/Losses (max)

**Efficiency Metrics**:
- Total Pips Gained: Aggregate pip profit/loss
- Average Pips per Trade
- Trade Frequency: Trades per month
- Time in Market (%): Percentage of time with open positions

### 3.8 Comparative Analysis Framework

#### 3.8.1 Primary Comparison

**Research Question**: Does the 5× larger account ($5,000 vs. $1,000) produce proportionally better results?

**Hypotheses**:
- **H₀ (Null)**: Performance metrics scale linearly with account size
- **H₁ (Alternative)**: Performance metrics show non-linear relationship with account size

**Key Comparisons**:
1. Absolute returns (dollar amounts)
2. Percentage returns (ROI)
3. Risk-adjusted returns (Sharpe ratio)
4. Drawdown characteristics
5. Trade frequency and size

#### 3.8.2 Analysis Methods

**Quantitative Analysis**:
- Descriptive statistics for all metrics
- Time series analysis of equity curves
- Distribution analysis of returns
- Correlation analysis between accounts

**Qualitative Analysis**:
- Market condition categorization (trending vs. ranging)
- Failure mode analysis
- Edge case identification
- Strategy robustness assessment

---

## 4. Implementation Details

### 4.1 Technology Stack

**Programming Language**: Python 3.9+
- Chosen for extensive financial libraries and readability

**Core Libraries**:
- `oandapyV20`: Official OANDA API client
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `matplotlib/plotly`: Data visualization
- `pytest`: Testing framework

**Development Environment**:
- Version Control: Git/GitHub
- Environment Management: Python venv
- Configuration: YAML + environment variables
- Documentation: Markdown + inline code comments

### 4.2 Software Architecture Patterns

**Design Patterns Used**:

1. **Strategy Pattern**: `BaseStrategy` abstract class enables multiple strategy implementations
2. **Factory Pattern**: Strategy creation and configuration
3. **Observer Pattern**: Event-driven trade execution
4. **Repository Pattern**: Data access abstraction

**Principles**:
- SOLID principles for maintainable code
- DRY (Don't Repeat Yourself)
- Separation of concerns
- Dependency injection for testability

### 4.3 Code Structure

```
forex-algo-trader/
├── src/
│   ├── api/           # OANDA API integration
│   ├── strategies/    # Trading strategy implementations
│   ├── risk/          # Risk management modules
│   ├── backtesting/   # Backtesting engine
│   └── utils/         # Helper functions
├── tests/             # Unit and integration tests
├── scripts/           # Utility scripts
├── data/              # Data storage
├── config/            # Configuration files
└── docs/              # Documentation
```

### 4.4 Quality Assurance

**Testing Strategy**:
1. Unit tests for individual components
2. Integration tests for system interactions
3. Backtesting validation against known results
4. Paper trading validation before any live deployment

**Code Review Process**:
- Peer review of all significant changes
- Automated linting (pylint, flake8)
- Type hints for function signatures
- Comprehensive docstrings

---

## 5. Expected Results and Hypotheses

### 5.1 Primary Hypotheses

**H1: Proportional Performance Hypothesis**
- **Prediction**: The $5,000 account will generate approximately 5× the absolute dollar returns of the $1,000 account
- **Rationale**: Identical percentage-based risk management should scale linearly
- **Test**: Compare absolute returns and check for linear relationship

**H2: Risk-Adjusted Return Hypothesis**
- **Prediction**: Both accounts will achieve similar risk-adjusted returns (Sharpe ratios)
- **Rationale**: Same strategy with same risk parameters should have similar efficiency
- **Test**: Compare Sharpe ratios, Sortino ratios

**H3: Drawdown Resilience Hypothesis**
- **Prediction**: The $5,000 account will recover from drawdowns more quickly
- **Rationale**: Larger capital buffer provides more cushion for variance
- **Test**: Analyze drawdown duration and recovery time

**H4: Transaction Cost Impact Hypothesis**
- **Prediction**: Fixed costs (spreads) will have greater relative impact on the $1,000 account
- **Rationale**: Same absolute spread cost represents larger percentage of smaller account
- **Test**: Calculate cost-to-equity ratios

### 5.2 Secondary Hypotheses

**H5: Position Sizing Flexibility**
- **Prediction**: $5,000 account will have more flexibility in position sizing optimization
- **Test**: Analyze position size distribution and optimization space

**H6: Strategy Robustness**
- **Prediction**: SMA crossover will perform better in trending markets than ranging markets
- **Test**: Segment performance by market condition (ADX indicator)

**H7: Frequency vs. Quality Trade-off**
- **Prediction**: More frequent trading (shorter MA periods) will increase absolute returns but decrease risk-adjusted returns
- **Test**: Compare 10/30 vs. 20/50 vs. 50/200 SMA combinations

### 5.3 Success Criteria

**Minimum Viable Results**:
- Strategy generates signals consistently (>10 trades in backtest)
- System operates without errors for continuous 1-week period
- Risk management functions as designed (no position size violations)
- Data is accurately recorded and retrievable

**Strong Results**:
- Positive risk-adjusted returns (Sharpe ratio > 1.0)
- Win rate >45% with profit factor >1.5
- Maximum drawdown <20%
- Clear insights on account size impact

**Exceptional Results**:
- Sharpe ratio > 2.0
- Profit factor > 2.5
- Demonstrates non-obvious relationship between account size and performance
- Publishable insights for retail trader community

---

## 6. Ethical Considerations and Risk Disclosure

### 6.1 Educational Purpose Statement

This project is conducted **exclusively for educational purposes**. All trading is performed in demo/practice accounts using virtual capital. No real money is at risk at any point during this research.

### 6.2 Risk Disclosure

**Important Disclaimers**:

1. **Past Performance**: Historical performance does not guarantee future results
2. **Market Risk**: Forex trading carries substantial risk of loss
3. **Leverage Risk**: Leverage amplifies both gains and losses
4. **Technology Risk**: System failures, API outages, and bugs can cause losses
5. **Model Risk**: Algorithmic strategies can fail in unprecedented market conditions

**Not Financial Advice**: This research does not constitute financial advice. Readers should consult licensed financial advisors before making investment decisions.

### 6.3 Responsible Development Practices

**Commitments**:
1. Transparent methodology and code (open-source)
2. Honest reporting of both successes and failures
3. Clear distinction between backtested and live results
4. No exaggeration of potential returns
5. Emphasis on risk management over profit maximization

### 6.4 Data Privacy and Security

**Practices**:
- API keys stored in environment variables (not committed to version control)
- No personal financial information collected or stored
- All accounts use practice credentials
- No sharing of account credentials

---

## 7. Timeline and Milestones

### Phase 1: Foundation (Weeks 1-2) ✅ COMPLETE
- [x] Project structure and documentation
- [x] OANDA API integration
- [x] Data fetching and storage
- [x] Connection testing

**Deliverable**: Working API connection to both demo accounts

### Phase 2: Strategy Development (Weeks 3-4) ✅ COMPLETE
- [x] Base strategy framework
- [x] SMA crossover implementation
- [x] Signal generation testing
- [x] Strategy testing on historical data

**Deliverable**: Functional SMA crossover strategy with performance analysis

### Phase 3: Risk Management (Weeks 5-6) ⬜ IN PROGRESS
- [ ] Position sizing calculator
- [ ] Stop loss implementation
- [ ] Take profit logic
- [ ] Maximum drawdown controls
- [ ] Daily loss limits

**Deliverable**: Complete risk management module

### Phase 4: Backtesting (Weeks 7-8)
- [ ] Backtesting engine development
- [ ] Transaction cost modeling
- [ ] Performance metrics calculation
- [ ] Equity curve generation
- [ ] Comparative analysis tools

**Deliverable**: Comprehensive backtesting framework with results

### Phase 5: Paper Trading (Weeks 9-10)
- [ ] Live market data integration
- [ ] Real-time signal generation
- [ ] Automated order execution (demo)
- [ ] Trade monitoring dashboard
- [ ] Performance tracking

**Deliverable**: Live paper trading system operating on both accounts

### Phase 6: Analysis (Weeks 11-12)
- [ ] Data collection and cleaning
- [ ] Statistical analysis
- [ ] Account size comparison
- [ ] Strategy optimization experiments
- [ ] Final report and recommendations

**Deliverable**: Complete research findings and documentation

---

## 8. References

[1] Bank for International Settlements (2022). "Triennial Central Bank Survey of Foreign Exchange and Over-the-counter (OTC) Derivatives Markets in 2022."

[2] Hendershott, T., Jones, C. M., & Menkveld, A. J. (2011). "Does Algorithmic Trading Improve Liquidity?" *The Journal of Finance*, 66(1), 1-33.

[3] OANDA Corporation (2023). "Retail Forex Trading Statistics and Demographics Report."

[4] Aldridge, I. (2013). *High-Frequency Trading: A Practical Guide to Algorithmic Strategies and Trading Systems*. John Wiley & Sons.

[5] King, M. R., & Rime, D. (2010). "The $4 Trillion Question: What Explains FX Growth Since the 2007 Survey?" *BIS Quarterly Review*, December 2010.

[6] Fama, E. F., & Blume, M. E. (1966). "Filter Rules and Stock-Market Trading." *The Journal of Business*, 39(1), 226-241.

[7] Donchian, R. D. (1960). "Donchian's 5- and 20-Day Moving Averages." *Commodities Magazine*.

[8] Fama, E. F. (1970). "Efficient Capital Markets: A Review of Theory and Empirical Work." *The Journal of Finance*, 25(2), 383-417.

[9] Christie, W. G., & Huang, R. D. (1995). "Following the Pied Piper: Do Individual Returns Herd Around the Market?" *Financial Analysts Journal*, 51(4), 31-37.

[10] Jegadeesh, N., & Titman, S. (1993). "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency." *The Journal of Finance*, 48(1), 65-91.

[11] Hong, H., & Stein, J. C. (1999). "A Unified Theory of Underreaction, Momentum Trading, and Overreaction in Asset Markets." *The Journal of Finance*, 54(6), 2143-2184.

[12] Brock, W., Lakonishok, J., & LeBaron, B. (1992). "Simple Technical Trading Rules and the Stochastic Properties of Stock Returns." *The Journal of Finance*, 47(5), 1731-1764.

[13] Neely, C. J., Weller, P. A., & Dittmar, R. (1997). "Is Technical Analysis in the Foreign Exchange Market Profitable? A Genetic Programming Approach." *Journal of Financial and Quantitative Analysis*, 32(4), 405-426.

[14] Olson, D. (2004). "Have Trading Rule Profits in the Currency Markets Declined Over Time?" *Journal of Banking & Finance*, 28(1), 85-105.

[15] Hsu, P. H., Taylor, M. P., & Wang, Z. (2016). "Technical Trading: Is It Still Beating the Foreign Exchange Market?" *Journal of International Economics*, 102, 188-208.

[16] Locke, P. R., & Mann, S. C. (2005). "Professional Trader Discipline and Trade Disposition." *Journal of Financial Economics*, 76(2), 401-444.

[17] Kelly, J. L. (1956). "A New Interpretation of Information Rate." *Bell System Technical Journal*, 35(4), 917-926.

[18] Bacon, C. R. (2008). *Practical Portfolio Performance Measurement and Attribution*. John Wiley & Sons.

[19] Markowitz, H. (1952). "Portfolio Selection." *The Journal of Finance*, 7(1), 77-91.

[20] Tharp, V. K. (2008). *Trade Your Way to Financial Freedom*. McGraw-Hill Education.

[21] Lo, A. W., Mamaysky, H., & Wang, J. (2000). "Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation." *The Journal of Finance*, 55(4), 1705-1765.

[22] Murphy, J. J. (1999). *Technical Analysis of the Financial Markets*. New York Institute of Finance.

[23] Wilder, J. W. (1978). *New Concepts in Technical Trading Systems*. Trend Research.

[24] Bollinger, J. (2001). *Bollinger on Bollinger Bands*. McGraw-Hill Education.

[25] Appel, G. (2005). *Technical Analysis: Power Tools for Active Investors*. FT Press.

---

## 9. Appendices

### Appendix A: Glossary of Terms

**Algorithmic Trading**: The use of computer programs to execute trades based on predefined rules and conditions.

**ATR (Average True Range)**: A volatility indicator measuring the average range between high and low prices over a specified period.

**Backtesting**: The process of testing a trading strategy on historical data to evaluate its potential performance.

**Death Cross**: A bearish signal where a short-term moving average crosses below a long-term moving average.

**Drawdown**: The reduction in account value from a peak to a trough, expressed as a percentage.

**Golden Cross**: A bullish signal where a short-term moving average crosses above a long-term moving average.

**Leverage**: The use of borrowed capital to increase potential returns (and risks).

**Pip**: The smallest price movement in forex trading (typically 0.0001 for most pairs).

**Position Sizing**: The process of determining how many units to trade based on account size and risk parameters.

**Profit Factor**: The ratio of gross profits to gross losses.

**Risk-Reward Ratio**: The ratio of potential profit to potential loss on a trade.

**Sharpe Ratio**: A measure of risk-adjusted return, calculated as (Return - Risk-Free Rate) / Standard Deviation.

**Slippage**: The difference between expected execution price and actual execution price.

**SMA (Simple Moving Average)**: The average price over a specified number of periods.

**Spread**: The difference between the bid and ask price.

**Stop Loss**: An order to automatically exit a position at a predetermined price to limit losses.

**Take Profit**: An order to automatically exit a position at a predetermined price to lock in profits.

### Appendix B: Technical Specifications

**OANDA API Version**: v20 REST API  
**Python Version**: 3.9 - 3.13  
**Primary Currency Pair**: EUR/USD  
**Default Timeframe**: H1 (Hourly)  
**Data Retention**: 365 days historical  
**Maximum API Rate**: 120 requests/minute  

**System Requirements**:
- CPU: 2+ cores recommended
- RAM: 4GB minimum, 8GB recommended
- Storage: 1GB for data and logs
- Internet: Stable connection required
- Operating System: macOS, Linux, or Windows

### Appendix C: Code Repository

**GitHub Repository**: [To be provided]  
**License**: MIT License  
**Documentation**: Available in `/docs` directory  
**Issues and Contributions**: Welcome via GitHub Issues

### Appendix D: Contact and Collaboration

For questions, collaboration opportunities, or to report issues:

**Project Maintainers**: Forex Algo Trader Research Team  
**Email**: [To be provided]  
**GitHub**: [To be provided]  
**Documentation**: See README.md and docs/ folder

---

## 10. Conclusion

This whitepaper outlines a comprehensive research project investigating the impact of account capitalization on algorithmic trading performance in forex markets. By implementing identical strategies across accounts of different sizes ($1,000 vs. $5,000), we aim to provide empirical insights valuable to retail traders entering the algorithmic trading space.

Our methodology combines established technical analysis techniques (moving average crossovers) with rigorous risk management and comprehensive performance analysis. The modular, open-source architecture enables reproducibility and extension by other researchers.

Key differentiators of this research:
1. **Practical Focus**: Addresses real concerns of retail traders with limited capital
2. **Rigorous Methodology**: Employs academic standards in design and analysis
3. **Open Source**: All code, data, and results will be publicly available
4. **Educational Purpose**: Designed as a learning tool, not a profit-seeking venture
5. **Comparative Approach**: Direct comparison eliminates many confounding variables

While we acknowledge the limitations of our approach—including focus on a single currency pair, reliance on technical analysis, and the inherent unpredictability of financial markets—we believe this research will contribute valuable insights to the algorithmic trading community.

**Expected Contributions**:
- Quantitative data on account size impact in retail forex trading
- Open-source algorithmic trading framework for educational use
- Documented best practices for strategy development and risk management
- Reproducible research methodology for similar studies

As we progress through the development phases, we will continue to document our findings, challenges, and insights. All results—both positive and negative—will be reported transparently to maximize the educational value of this project.

---

**Document Version History**

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | January 2025 | Initial whitepaper | Research Team |

---

**Acknowledgments**

We acknowledge the contributions of the open-source community, particularly the developers of the pandas, numpy, and oandapyV20 libraries that make this research possible. We also thank OANDA for providing practice trading accounts that enable risk-free algorithmic trading research.

---

*This whitepaper is a living document and will be updated as the project progresses. Current version: 1.0*

*Last Updated: January 2025*