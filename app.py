import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -------------------------
# Page config (Netflix vibe)
# -------------------------
st.set_page_config(
    page_title="Netflix Stock Dashboard",
    layout="wide"
)

NETFLIX_RED = "#E50914"
NETFLIX_GRAY = "#6e6e6e"

st.markdown(
    f"""
    <style>
    h1 {{
        color: {NETFLIX_RED};
        font-family: Montserrat, Arial, sans-serif;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Load data
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("NFLX_stocks.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    return df

df = load_data()
years = sorted(df["year"].unique().astype(int))

for col in ['open', 'high', 'low', 'close', 'adj_close', 'volume']:
    df[col] = pd.to_numeric(df[col], errors='coerce')


# -------------------------
# Sidebar filter
# -------------------------
st.sidebar.title("Filters")
selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)

df_year = df[df["year"] == selected_year]

# -------------------------
# Create Plotly figure
# -------------------------
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    row_heights=[0.7, 0.3],
    vertical_spacing=0.03
)

# Candlestick
fig.add_trace(
    go.Candlestick(
        x=df_year["date"],
        open=df_year["open"],
        high=df_year["high"],
        low=df_year["low"],
        close=df_year["close"],
        increasing_line_color="green",
        decreasing_line_color="red",
        name="Price"
    ),
    row=1, col=1
)

# Volume
volume_colors = np.where(
    df_year["close"] >= df_year["open"],
    "green",
    "red"
)

fig.add_trace(
    go.Bar(
        x=df_year["date"],
        y=df_year["volume"],
        marker_color=volume_colors,
        name="Volume"
    ),
    row=2, col=1
)

# -------------------------
# Layout styling
# -------------------------
fig.update_layout(
    title=dict(
        text=(
            "<b>NETFLIX STOCK PRICE & VOLUME</b><br>"
            f"<span style='font-size:16px; color:{NETFLIX_GRAY};'>"
            f"{int(selected_year)} — Candlestick with Trading Volume</span>"
        ),
        x=0.5,
        xanchor="center",
        font=dict(
            family="Montserrat, Arial Black, Helvetica Neue, Arial",
            size=28,
            color=NETFLIX_RED
        )
    ),
    template="plotly_white",
    height=750,
    margin=dict(t=120),
    xaxis_rangeslider_visible=False
)

fig.update_yaxes(title_text="Price ($)", row=1, col=1)
fig.update_yaxes(title_text="Volume", row=2, col=1)

# -------------------------
# Render
# -------------------------
st.plotly_chart(fig, use_container_width=True)
