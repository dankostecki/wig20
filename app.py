import yfinance as yf
import pandas as pd

# Pobieranie i obliczenia (WIG20)
df = yf.download("WIG20.WA", period="10y", progress=False)
if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.droplevel(1)

df['D1'] = df['Close'].pct_change()
for d, label in zip([21, 63, 252], ['+1M', '+3M', '+12M']):
    df[label] = (df['Close'].shift(-d) / df['Close']) - 1

top15 = df.nsmallest(15, 'D1').copy().reset_index()
top15['Date'] = top15['Date'].dt.strftime('%Y-%m-%d')

# Generowanie prostego HTML z kolorami
html_table = top15[['Date', 'D1', '+1M', '+3M', '+12M', 'Close']].to_html(classes='table', index=False)
html_content = f"""
<html>
<head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body {{ background-color: #111; color: #eee; padding: 20px; font-family: monospace; }}
        table {{ border-color: #444; }}
        .pos {{ color: #00ff00; }} .neg {{ color: #ff4d4d; }}
    </style>
</head>
<body>
    <h3>WIG20 TOP 15 NAJGORSZYCH SESJI (Ostatnie 10 lat)</h3>
    {html_table.replace('<td>-', '<td class="neg">-').replace('<td>0.', '<td class="pos">0.')}
</body>
</html>
"""
with open("index.html", "w") as f:
    f.write(html_content)
