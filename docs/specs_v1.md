# Specification: Weekly Trend-Based Rotational Strategy

## 1. Overview

This strategy systematically rotates among highly liquid ETFs and spot FX using weekly composite trend signals, enhanced by a macro relative-strength overlay. It enables low-frequency (weekly) trading, prioritizing disciplined entries, measured allocations, and robust exit mechanisms to withstand whipsaw.

---

## 2. Asset Universe

- **Core Instruments**:
  - S&P 500 ETF (e.g., SPY)
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
  - Non‑doji close above SMA of **HIGH** → trend shifts up (Buy)
  - Non‑doji close below SMA of **LOW** → trend shifts down (Sell)
- **Trend Force (SMA Close)**:
  - SMA(Close, 20) > SMA(Close, 50) → **Uptrend**
  - SMA(Close, 20) < SMA(Close, 50) → **Downtrend**

---

## 4. Macro Overlay: Relative Strength Gauge

- For each instrument pair, compute the **Price Series Ratio** (e.g. XLK/XLU).
- **Normalize** this ratio series (e.g., via rolling z‑score).
- Calculate its **Rate of Change (ROC)**—this is the **ROC Differential**.
- When multiple instruments qualify for entry, **rank by ROC Differential** to prioritize allocation.

---

## 5. Position Sizing & Allocation (USD 5,000 Portfolio)

- **Equal-Weighted Allocation**: Allocate capital equally across qualifiers—for simplicity and diversification.
- **Optional Tiered Allocation**: Assign higher weight to instruments with stronger ROC differential (e.g., 60% to top, rest equally split among others).

---

## 6. Exit Strategy: Layered Approach to Combat Whipsaw

### A. ATR-Based Trailing Stop

- **ATR Period**: 21 days (weekly equivalent)
- **Multiplier**: 3× ATR (default for trend systems)
- **Logic**:
  - **Long position**: Stop = Highest Price − (3 × ATR)
  - **Short position**: Stop = Lowest Price + (3 × ATR)
  - Stop only tightens in favor of the trend, never loosens

### B. Relative-Strength “Cast‑Off” Retention

- Maintain positions **while instrument remains in the top 25%** of relative strength (ROC Differential).
- Exit when it drops below the 75th percentile—lets winners run; removes laggards early

### C. Time-Based Safety Exit

- **Maximum Holding Period**: 4 weeks.
- Exit positions that haven’t triggered counter-signals or exit criteria within this timeframe—limits stale trades

---

## 7. Summary Table

| Component                | Specification Summary |
|--------------------------|------------------------|
| **Instruments**          | SPY, EUR/USD, bond ETF, gold ETF, utilities ETF, cyclical ETFs (XLK, XLI, XLY) |
| **Entry Signal**         | Composite indicators (MACD, RSI, Stochastic, candlestick/SMA, SMA trend) over 3-week window |
| **Relative Strength**    | ROC of normalized price ratios → ranking multiple qualifiers |
| **Position Sizing**      | Equal-weighted default; optional tiered by ROC differential |
| **Exit Strategy**        | ATR trailing stop (ATR21×3), relative-strength top-25% retention, 4-week maximum hold |

