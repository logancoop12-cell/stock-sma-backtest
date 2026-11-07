#!/usr/bin/env python3
"""
Dual SMA Crossover Backtest
---------------------------
Uses free Yahoo Finance data + backtesting.py library.
No QuantConnect / Lean required.
"""

import argparse
from datetime import datetime

import pandas as pd
import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA


class DualSMACrossover(Strategy):
    """
    Classic dual moving-average crossover.
    Long when fast SMA > slow SMA, flat otherwise.
    """
    fast = 50
    slow = 200

    def init(self):
        close = self.data.Close
        self.fast_sma = self.I(SMA, close, self.fast)
        self.slow_sma = self.I(SMA, close, self.slow)

    def next(self):
        if crossover(self.fast_sma, self.slow_sma):
            self.buy()
        elif crossover(self.slow_sma, self.fast_sma):
            self.position.close()


def download_data(symbol: str, start: str = "2010-01-01", end: str = None) -> pd.DataFrame:
    """Download OHLCV data from Yahoo Finance."""
    if end is None:
        end = datetime.now().strftime("%Y-%m-%d")

    print(f"Downloading {symbol} data from {start} to {end}...")
    df = yf.download(symbol, start=start, end=end, progress=False, auto_adjust=True)

    if df.empty:
        raise ValueError(f"No data returned for {symbol}. Check the ticker symbol.")

    # yfinance sometimes returns MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Ensure we have the required columns
    required = ["Open", "High", "Low", "Close", "Volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = df[required].dropna()
    print(f"Downloaded {len(df)} bars.")
    return df


def run_backtest(
    symbol: str = "SPY",
    fast: int = 50,
    slow: int = 200,
    cash: float = 100_000,
    commission: float = 0.001,  # 0.1%
    start: str = "2010-01-01",
):
    data = download_data(symbol, start=start)

    # Pass parameters to the strategy class
    DualSMACrossover.fast = fast
    DualSMACrossover.slow = slow

    bt = Backtest(
        data,
        DualSMACrossover,
        cash=cash,
        commission=commission,
        exclusive_orders=True,
        trade_on_close=True,
    )

    print("\nRunning backtest...")
    stats = bt.run()

    print("\n" + "=" * 60)
    print(f"  RESULTS  |  {symbol}  |  SMA({fast}/{slow})")
    print("=" * 60)
    print(stats)
    print("=" * 60)

    # Open interactive plot
    print("\nOpening interactive equity curve + trades chart...")
    bt.plot()

    return stats


def main():
    parser = argparse.ArgumentParser(description="Dual SMA Crossover Backtest")
    parser.add_argument("--symbol", default="SPY", help="Ticker symbol (default: SPY)")
    parser.add_argument("--fast", type=int, default=50, help="Fast SMA period (default: 50)")
    parser.add_argument("--slow", type=int, default=200, help="Slow SMA period (default: 200)")
    parser.add_argument("--cash", type=float, default=100000, help="Starting cash (default: 100000)")
    parser.add_argument("--start", default="2010-01-01", help="Start date YYYY-MM-DD")
    parser.add_argument("--commission", type=float, default=0.001, help="Commission rate (default: 0.001 = 0.1%)")

    args = parser.parse_args()

    if args.fast >= args.slow:
        print("Warning: fast period should be smaller than slow period for classic crossover.")

    run_backtest(
        symbol=args.symbol,
        fast=args.fast,
        slow=args.slow,
        cash=args.cash,
        commission=args.commission,
        start=args.start,
    )


if __name__ == "__main__":
    main()
