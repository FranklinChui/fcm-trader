# 1. Specification: Weekly Trend-Based Rotational Strategy

## 1.1. Overview

This strategy systematically rotates among highly liquid ETFs and spot FX using weekly composite trend signals, enhanced by a macro relative-strength overlay. It generates low-frequency (weekly) trade signals for manual execution, prioritizing disciplined entries, measured allocations, and robust exit mechanisms to withstand whipsaw.

## 1.2. Business Objective

The primary objective is to achieve consistent, risk-adjusted returns by capturing medium-term trends while minimizing exposure during volatile, non-trending periods. Success will be measured by the strategy's Sharpe ratio, win/loss ratio, and maximum drawdown over a 12-month backtesting period.

---

## 2. Asset Universe

- **Core Instruments**:
  - S&P 500 ETF (e.g., SPY)
  - EUR/USD spot FX
  - Broad-market bond ETF
  - Gold ETF (commodity)
  - Utilities ETF
- **Cyclical ETFs** (generally negatively correlated to Utilities):
  - Technology ETF (e.g., XLK)
  - Industrials ETF (e.g., XLI)
  - Consumer Discretionary ETF (e.g., XLY)

---

## 3. Tactical Composite Entry Signal (Weekly)

Trigger a **Buy** or **Sell** entry when **all** below conditions are met within a 3-week window and no counter-signal appears:

- **MACD line**:
  - Above 75 → **Sell**
  - Below 25 → **Buy**
- **RSI**:
  - Above 70 → **Sell**
  - Below 30 → **Buy**
- **Full Stochastic Slow**:
  - FastStoch > SlowStoch and above 75 → **Sell**
  - FastStoch < SlowStoch and below 25 → **Buy**
- **Candlestick vs. SMA**:
  - Non-doji close above SMA of **HIGH** → trend shifts up (Buy)
  - Non-doji close below SMA of **LOW** → trend shifts down (Sell)
- **Trend Force (SMA Close)**:
  - SMA(Close, 20) > SMA(Close, 50) → **Uptrend**
  - SMA(Close, 20) < SMA(Close, 50) → **Downtrend**

---

## 4. Macro Overlay: Relative Strength Gauge

- For each instrument pair, compute the **Price Series Ratio** (e.g. XLK/XLU).
- **Normalize** this ratio series (e.g., via rolling z-score).
- Calculate its **Rate of Change (ROC)**—this is the **ROC Differential**.
- When multiple instruments qualify for entry, **rank by ROC Differential** to prioritize allocation.

---

## 5. Position Sizing & Allocation (USD 5,000 Portfolio)

- **Equal-Weighted Allocation**: Allocate capital equally across qualifiers—for simplicity and diversification.
- **Optional Tiered Allocation**: Assign higher weight to instruments with stronger ROC differential (e.g., 60% to top, rest equally split among others).

---

## 6. Exit Strategy: Layered Approach to Combat Whipsaw

### 6.1. ATR-Based Trailing Stop

- **ATR Period**: 21 days (weekly equivalent)
- **Multiplier**: 3x ATR (default for trend systems)
- **Logic**:
  - **Long position**: Stop = Highest Price - (3 * ATR)
  - **Short position**: Stop = Lowest Price + (3 * ATR)
  - Stop only tightens in favor of the trend, never loosens.

### 6.2. Relative-Strength "Cast-Off" Retention

- Maintain positions **while instrument remains in the top 25%** of relative strength (ROC Differential).
- Exit when it drops below the 75th percentile—lets winners run; removes laggards early.

### 6.3. Time-Based Safety Exit

- **Maximum Holding Period**: 4 weeks.
- Exit positions that haven’t triggered counter-signals or exit criteria within this timeframe—limits stale trades.

---

## 7. Data & Implementation Notes

- **Data Sources**: Requires daily and weekly OHLCV (Open, High, Low, Close, Volume) data for all instruments from a reliable provider (e.g., financial data API).
- **Indicator Calculation**: All indicators (MACD, RSI, Stochastics, SMA) are to be calculated based on weekly closing data.
- **Technology Stack**: To be defined in the Architecture Document. The system must be capable of ingesting data, computing signals, and maintaining a portfolio based on user-entered trade data. Trade execution is fulfilled manually by the user. The user is responsible for recording their positions (e.g., instrument, entry price, size, date) within the system after executing a trade.

---

## 8. Edge Case Handling

- **No Qualifying Signals**: If no instruments meet the entry criteria within a given week, no new positions will be initiated. The system will hold cash or existing positions.
- **Conflicting Signals**: If indicators provide conflicting signals (e.g., MACD Buy, RSI Sell), no entry is triggered. All five composite signals must align.
- **Data Gaps**: The system should log an error and halt trading for an instrument if there are gaps in the historical data required for indicator calculation.

---

## 9. Risk Management

A disciplined approach to risk management is critical for long-term success. This section outlines key risks and mitigation strategies.

### 9.1. Market Risk

- **Description**: The risk of losses due to factors that affect the overall performance of financial markets, such as major economic events, changes in interest rates, or geopolitical turmoil. This includes the risk of significant drawdowns or "black swan" events.
- **Mitigation**:
  - The layered exit strategy (ATR trailing stops, relative-strength cast-off) is the primary defense against sustained drawdowns.
  - Position sizing rules limit the capital exposed in any single trade.
  - The strategy's inherent logic to hold cash during periods of conflicting signals or low conviction helps avoid volatile, non-trending markets.

### 9.2. Data Dependency Risk

- **Description**: The strategy's performance is highly dependent on the quality, timeliness, and availability of market data.
- **Mitigation**:
  - **Data Source Redundancy**: Implement connectors for at least two independent data providers to failover in case of an outage.
  - **Data Integrity Checks**: Before any signal calculation, the system must validate incoming data for gaps, outliers, or stale values. Log any anomalies and halt trading for the affected instrument until the issue is resolved.
  - **API Monitoring**: The system should monitor API responses for errors or changes in format that could break the data ingestion process.

### 9.3. Model & Manual Execution Risk

- **Description**: The risk that the model does not perform as expected in live market conditions (model risk) or that manually executed trades deviate from the generated signals (manual execution risk, e.g., slippage, delayed execution).
- **Mitigation**:
  - **Regular Backtesting**: The model's performance should be periodically re-evaluated against new market data to detect performance degradation.
  - **Execution Monitoring**: Log and review trade execution prices against the signal price to monitor for excessive slippage.
  - **Clear Signal Presentation**: The system must present trade signals and portfolio status clearly and unambiguously to minimize errors during manual trade execution and position entry.

---

## 10. Summary Table

| Component                | Specification Summary |
|--------------------------|------------------------|
| **Instruments**          | SPY, EUR/USD, bond ETF, gold ETF, utilities ETF, cyclical ETFs (XLK, XLI, XLY) |
| **Entry Signal**         | Composite indicators (MACD, RSI, Stochastic, candlestick/SMA, SMA trend) over 3-week window |
| **Relative Strength**    | ROC of normalized price ratios → ranking multiple qualifiers |
| **Position Sizing**      | Equal-weighted default; optional tiered by ROC differential |
| **Exit Strategy**        | ATR trailing stop (ATR21x3), relative-strength top-25% retention, 4-week maximum hold |
| **Edge Cases**           | Hold cash if no signals; require 100% signal alignment; log errors on data gaps. |
