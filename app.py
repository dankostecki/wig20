import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide", page_title="WIG20 Terminal")
st.markdown("<style>body {background-color: #0e1117; color: white;}</style>", unsafe_allow_html=True)
st.title("📊 WIG20 TOP 15 NAJGORSZYCH SESJI")

@st.cache_data(ttl=3600)
def get_wig_data():
    df = yf.download("WIG20.WA", period="10y", progress=False)
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.droplevel(1)
    df['D1'] = df['Close'].pct_change()
    for days, label in zip([21, 63, 252], ['+1M', '+3M', '+12M']):
        df[label] = (df['Close'].shift(-days) / df['Close']) - 1
    return df

df = get_wig_data()
top15 = df.nsmallest(15, 'D1').copy().reset_index()
top15['Date'] = top15['Date'].dt.strftime('%Y-%m-%d')

# Formatowanie tabeli
def color_val(v):
    if pd.isna(v) or isinstance(v, str): return ""
    return f"color: {'#00ff00' if v > 0 else '#ff4d4d'}"

st.table(top15[['Date', 'D1', '+1M', '+3M', '+12M', 'Close']].style.format({
    'D1': "{:.2%}", '+1M': "{:.2%}", '+3M': "{:.2%}", '+12M': "{:.2%}", 'Close': "{:.2f}"
}).map(color_val, subset=['D1', '+1M', '+3M', '+12M']))
