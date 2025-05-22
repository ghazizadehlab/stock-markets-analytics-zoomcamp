import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# Download S&P 500 historical data
sp500 = yf.download('^GSPC', start='1950-01-01', end=datetime.now().strftime('%Y-%m-%d'))

# Calculate all-time highs
sp500['AllTimeHigh'] = sp500['Close'].cummax()
sp500['IsAllTimeHigh'] = sp500['Close'] >= sp500['AllTimeHigh']

# Get all-time high dates
all_time_highs = sp500[sp500['IsAllTimeHigh']].copy()

# Initialize lists to store results
high_dates = []
high_prices = []
min_prices = []
min_dates = []

# Find minimum prices between consecutive all-time highs
for i in range(len(all_time_highs) - 1):
    current_high_date = all_time_highs.index[i]
    next_high_date = all_time_highs.index[i + 1]
    
    # Get the period between these two highs
    period_data = sp500.loc[current_high_date:next_high_date]
    
    # Find the minimum price in this period
    min_price = period_data['Close'].min()
    min_date = period_data['Close'].idxmin()
    
    # Store results
    high_dates.append(current_high_date)
    high_prices.append(all_time_highs['Close'].iloc[i])
    min_prices.append(min_price)
    min_dates.append(min_date)

# Create a DataFrame with the results
results = pd.DataFrame({
    'High Date': high_dates,
    'High Price': high_prices,
    'Min Price': min_prices,
    'Min Date': min_dates,
    'Drawdown %': ((high_prices - min_prices) / high_prices * 100).round(2)
})

# Print summary statistics
print("\nSummary of S&P 500 All-Time Highs and Subsequent Minimums:")
print(f"Total number of all-time highs: {len(results)}")
print(f"\nAverage drawdown between highs: {results['Drawdown %'].mean():.2f}%")
print(f"Maximum drawdown: {results['Drawdown %'].max():.2f}%")
print(f"Minimum drawdown: {results['Drawdown %'].min():.2f}%")

# Save results to CSV
results.to_csv('sp500_highs_and_mins.csv')
print("\nResults have been saved to 'sp500_highs_and_mins.csv'") 