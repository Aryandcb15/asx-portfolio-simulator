# ASX Portfolio Stress Test Simulator

## Overview
An interactive simulator that stress tests a portfolio of Australian blue-chip 
ASX stocks against major historical market events. Built as a personal project 
to research and understand portfolio risk before beginning to invest in the 
Australian market.

The ASX was chosen deliberately over US markets — as someone based in Melbourne 
targeting roles in Australian finance, understanding local market dynamics and 
how Australian blue-chips behave under stress is directly relevant to both my 
career and personal investment goals.

## Portfolio
| Stock | Company | Weight |
|-------|---------|--------|
| CBA.AX | Commonwealth Bank | 30% |
| BHP.AX | BHP Group | 20% |
| WBC.AX | Westpac Banking Corporation | 20% |
| ANZ.AX | ANZ Banking Group | 15% |
| WES.AX | Wesfarmers | 15% |

## Stress Test Scenarios
| Scenario | Period | Portfolio Return | ASX 200 Return |
|----------|--------|-----------------|----------------|
| COVID Crash | 2020 | +6.3% | -0.1% |
| Rate Hike Cycle | 2022 | +6.5% | -7.3% |
| GFC | 2007-2009 | +31.2% | -14.8% |
| Full History | 2015-2025 | +169.8% | +50.1% |

## Key Findings
- The portfolio outperformed the ASX 200 benchmark across all 4 scenarios
- During the GFC the portfolio achieved +31.2% while the broader market fell 14.8%
- Over the full 10-year history the portfolio returned 169.8% vs the ASX 200's 50.1%
- Maximum drawdown during COVID was -38.3% — highlighting the importance of 
  understanding downside risk before investing

## Tools Used
- Python (yfinance, pandas, plotly)
- yfinance — real-time ASX stock data via Yahoo Finance
- Plotly — interactive HTML dashboard

## Files
- `simulator.py` — full simulation and charting code
- `portfolio_stress_test.html` — interactive dashboard (download to view)

## How to Run
```bash
pip install yfinance plotly pandas
python simulator.py
```
Open `portfolio_stress_test.html` in your browser to view the interactive charts.
