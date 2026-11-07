# Stock SMA Crossover Backtest

A fully self-contained dual moving-average crossover strategy backtest.

**No QuantConnect account required.**  
Uses free data from Yahoo Finance + the popular `backtesting.py` library.

## Strategy
- **Asset**: SPY (S&P 500 ETF)
- **Logic**: Go long when the fast SMA crosses above the slow SMA (Golden Cross).  
  Exit to cash when the fast SMA crosses below the slow SMA (Death Cross).
- Default periods: **50 / 200** (classic trend-following)

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/logancoop12-cell/stock-sma-backtest.git
cd stock-sma-backtest
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the backtest
```bash
python backtest.py
```

That's it. Results (equity curve, stats, trades) will print in the terminal and a interactive HTML chart will open.

### Optional: Change parameters
```bash
python backtest.py --fast 20 --slow 50 --symbol SPY --cash 100000
```

## What you get
- Total Return, CAGR, Sharpe Ratio, Max Drawdown, Win Rate, etc.
- Interactive equity curve + trades plot (HTML)
- Trade list

## Requirements
- Python 3.8+
- Internet connection (to download price data)

## Files
- `backtest.py` – Main script
- `requirements.txt` – Dependencies
- `README.md` – This file

Enjoy testing strategies without any paid platform.
