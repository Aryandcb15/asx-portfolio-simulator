import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ── PORTFOLIO CONFIGURATION ──────────────────────────────────────
portfolio = {
    'CBA.AX':  0.30,   # Commonwealth Bank      30%
    'BHP.AX':  0.20,   # BHP Group              20%
    'WBC.AX':  0.20,   # Westpac                20%
    'ANZ.AX':  0.15,   # ANZ Banking Group      15%
    'WES.AX':  0.15,   # Wesfarmers             15%
}

# Stress test scenarios (start date, end date, label)
scenarios = {
    'COVID Crash (2020)':      ('2020-01-01', '2020-12-31'),
    'Rate Hike Cycle (2022)':  ('2022-01-01', '2022-12-31'),
    'GFC (2008)':              ('2007-01-01', '2009-12-31'),
    'Full History (2015-2025)':('2015-01-01', '2025-01-01'),
}

benchmark = '^AXJO'  # ASX 200

def get_portfolio_returns(tickers, weights, start, end):
    data = yf.download(list(tickers) + [benchmark], start=start, end=end,
                      auto_adjust=True, progress=False)['Close']
    data = data.dropna()
    if data.empty:
        return None, None

    # Normalise to 100 at start
    normalised = data / data.iloc[0] * 100

    # Weighted portfolio
    port_cols = [t for t in tickers if t in normalised.columns]
    port_weights = [weights[t] for t in port_cols]
    normalised['Portfolio'] = sum(normalised[t] * w
                                  for t, w in zip(port_cols, port_weights))
    return normalised, data

def max_drawdown(series):
    roll_max = series.cummax()
    drawdown = (series - roll_max) / roll_max * 100
    return drawdown.min()

# ── RUN ANALYSIS ─────────────────────────────────────────────────
print("Fetching ASX data...")
results = {}

for scenario, (start, end) in scenarios.items():
    norm, raw = get_portfolio_returns(portfolio, portfolio, start, end)
    if norm is not None:
        port_return = norm['Portfolio'].iloc[-1] - 100
        bench_col = '^AXJO' if '^AXJO' in norm.columns else None
        bench_return = (norm[bench_col].iloc[-1] - 100) if bench_col else None
        mdd = max_drawdown(norm['Portfolio'])
        results[scenario] = {
            'data': norm,
            'portfolio_return': port_return,
            'benchmark_return': bench_return,
            'max_drawdown': mdd
        }
        print(f"\n{scenario}")
        print(f"  Portfolio Return:  {port_return:+.1f}%")
        if bench_return:
            print(f"  ASX 200 Return:   {bench_return:+.1f}%")
        print(f"  Max Drawdown:     {mdd:.1f}%")

# ── PLOT ─────────────────────────────────────────────────────────
print("\nGenerating charts...")
fig = make_subplots(rows=2, cols=2,
    subplot_titles=list(results.keys()),
    vertical_spacing=0.12)

positions = [(1,1),(1,2),(2,1),(2,2)]

for (scenario, res), (row, col) in zip(results.items(), positions):
    norm = res['data']

    fig.add_trace(go.Scatter(
        x=norm.index, y=norm['Portfolio'],
        name='Portfolio', line=dict(color='steelblue', width=2),
        showlegend=(row==1 and col==1)), row=row, col=col)

    if '^AXJO' in norm.columns:
        fig.add_trace(go.Scatter(
            x=norm.index, y=norm['^AXJO'],
            name='ASX 200', line=dict(color='tomato', width=2, dash='dash'),
            showlegend=(row==1 and col==1)), row=row, col=col)

fig.update_layout(
    title='ASX Portfolio Stress Test Simulator',
    height=700,
    template='plotly_white',
    legend=dict(orientation='h', y=1.05))

fig.write_html('portfolio_stress_test.html')
print("\nSaved portfolio_stress_test.html — open it in your browser!")