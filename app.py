import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime


# Function to plot stock performance using Plotly
def plot_stock_performance(
    stock1_name, stock2_name, stock1_ticker, stock2_ticker, start_date, end_date=None
):
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    stock1_data = yf.download(stock1_ticker, start=start_date, end=end_date)
    stock2_data = yf.download(stock2_ticker, start=start_date, end=end_date)

    stock1_normalized = (stock1_data["Close"] / stock1_data["Close"].iloc[0]) * 100
    stock2_normalized = (stock2_data["Close"] / stock2_data["Close"].iloc[0]) * 100

    stock1_ytd_performance = stock1_normalized.iloc[-1] - 100
    stock2_ytd_performance = stock2_normalized.iloc[-1] - 100

    # Plot normalized stock performance
    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(
            x=stock1_normalized.index,
            y=stock1_normalized,
            mode="lines",
            name=stock1_name,
            line=dict(color="blue"),
        )
    )
    fig1.add_trace(
        go.Scatter(
            x=stock2_normalized.index,
            y=stock2_normalized,
            mode="lines",
            name=stock2_name,
            line=dict(color="red"),
        )
    )
    fig1.update_layout(
        title=f"{stock1_name} vs {stock2_name} YTD Performance",
        xaxis_title="Date",
        yaxis_title="Normalized Price (Start of Year = 100)",
        legend=dict(x=0.01, y=0.99),
    )
    st.plotly_chart(fig1)

    # Calculate percentage difference
    percentage_difference = (
        (stock1_normalized - stock2_normalized) / stock2_normalized
    ) * 100

    # Plot percentage difference
    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=percentage_difference.index,
            y=percentage_difference,
            mode="lines",
            name="Percentage Difference",
            line=dict(color="purple"),
        )
    )
    fig2.update_layout(
        title=f"Percentage Difference in Performance between {stock1_name} and {stock2_name}",
        xaxis_title="Date",
        yaxis_title="Percentage Difference (%)",
        legend=dict(x=0.01, y=0.99),
    )
    st.plotly_chart(fig2)

    # Determine which stock performed better
    if stock1_ytd_performance > stock2_ytd_performance:
        better_stock = stock1_name
        worse_stock = stock2_name
        performance_difference = stock1_ytd_performance - stock2_ytd_performance
        comparison_message = f"{better_stock} performed {performance_difference:.2f}% better than {worse_stock}"
    else:
        better_stock = stock2_name
        worse_stock = stock1_name
        performance_difference = stock2_ytd_performance - stock1_ytd_performance
        comparison_message = f"{better_stock} performed {performance_difference:.2f}% better than {worse_stock}"

    # Display key KPIs
    st.subheader("Performance Summary")
    st.markdown(
        f"**Performance of {stock1_name} from {start_date} until {end_date}:** {stock1_ytd_performance:.2f}%"
    )
    st.markdown(
        f"**Performance of {stock2_name} from {start_date} until {end_date}:** {stock2_ytd_performance:.2f}%"
    )
    st.markdown(f"**Performance Difference:** {comparison_message}")


# Streamlit app
st.markdown(
    "<h1 style='text-align: center;'><span style='font-size: 50px;'>📈 StockSnap 📉</span></h1>",
    unsafe_allow_html=True,
)

# Stock options
stock_options = {
    "Apple Inc.": "AAPL",
    "Microsoft Corp": "MSFT",
    "NVIDIA Corp": "NVDA",
    "Amazon.com, Inc.": "AMZN",
    "Meta Platforms Inc.": "META",
    "Alphabet Inc. Class A": "GOOGL",
    "Berkshire Hathaway Inc. Class B": "BRK.B",
    "Eli Lilly and Company": "LLY",
    "Broadcom Inc.": "AVGO",
    "JPMorgan Chase & Co.": "JPM",
    "Exxon Mobil Corp.": "XOM",
    "Tesla Inc.": "TSLA",
    "The Procter & Gamble Company": "PG",
    "Mastercard Inc.": "MA",
    "S&P 500": "^GSPC",
    "Dow Jones Industrial Average": "^DJI",
    "Nasdaq Composite": "^IXIC",
    "Russell 2000": "^RUT",
    "FTSE 100": "^FTSE",
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "ARK Innovation ETF": "ARKK",
}

# Convert stock options to a DataFrame for search functionality
stock_options_df = pd.DataFrame(list(stock_options.items()), columns=["Name", "Ticker"])

# Stock search bar
stock1_name = st.selectbox("Select first stock:", stock_options_df["Name"], index=2)
stock2_name = st.selectbox("Select second stock:", stock_options_df["Name"], index=14)

# Get tickers from selected stock names
stock1_ticker = stock_options_df[stock_options_df["Name"] == stock1_name][
    "Ticker"
].values[0]
stock2_ticker = stock_options_df[stock_options_df["Name"] == stock2_name][
    "Ticker"
].values[0]

# Date range slider
start_date, end_date = st.date_input(
    "Select date range:", [datetime(datetime.now().year, 1, 1), datetime.now()]
)

# Plot button
if st.button("Plot Performance Comparison"):
    plot_stock_performance(
        stock1_name,
        stock2_name,
        stock1_ticker,
        stock2_ticker,
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"),
    )
