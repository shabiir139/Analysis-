import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from scipy.optimize import linprog

st.title("Capital Planning Optimization & Financial Forecasting")

# Fetch Apple Inc. stock data
stock_data = yf.download("AAPL", start="2015-01-01", end="2025-01-01")
st.write(stock_data.tail())

# Capital Allocation Optimization
returns = [0.1, 0.12, 0.15]  # Example returns for different strategies
capital_budget = st.number_input("Enter Capital Budget ($)", min_value=10000, value=100000)

# Optimization logic for capital allocation
c = [-r for r in returns]  # We negate returns since linprog minimizes the objective function
bounds = [(10000, 50000)] * len(returns)  # Example bounds for each strategy
A = [[1, 1, 1]]  # Constraint to ensure total allocation is equal to capital budget
b = [capital_budget]

result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

# Show optimal allocation and return
optimal_allocation = result.x
st.write(f"Optimal Capital Allocation: {optimal_allocation}")
st.write(f"Total Expected Return: {-result.fun}")

# Plotting results
fig = go.Figure([go.Bar(x=['Strategy 1', 'Strategy 2', 'Strategy 3'], y=optimal_allocation)])
fig.update_layout(title="Optimal Capital Allocation", xaxis_title="Strategies", yaxis_title="Capital Allocation")
st.plotly_chart(fig)

# Additional section for financial forecasting based on stock data
st.subheader("Financial Forecasting")

# Display the stock closing prices
st.write(stock_data['Close'].tail())

# Example: Plot stock data for the past month
fig_stock = go.Figure()
fig_stock.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price'))
fig_stock.update_layout(title="Stock Closing Price (AAPL)", xaxis_title="Date", yaxis_title="Close Price")
st.plotly_chart(fig_stock)
