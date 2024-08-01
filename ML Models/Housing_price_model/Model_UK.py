import time
import os

import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
#from statsmodels.tsa.arima_model import ARIMA
import time
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns

import dask.dataframe as dd
start_time = time.time()

# Read CSV with Dask
df = dd.read_csv("price_paid_records.csv")

# Convert the 'Date of Transfer' column to datetime
df['Date of Transfer'] = dd.to_datetime(df['Date of Transfer'])

# Extract year, month, and date (formatted as '%Y%m') using map_partitions
df['year'] = df['Date of Transfer'].dt.year
df['month'] = df['Date of Transfer'].dt.month
df['date'] = df['Date of Transfer'].dt.strftime('%Y%m')

# Compute the result to see the changes
df = df.compute()

end_time = time.time()

print(f"Dask code time taken: {end_time - start_time:.2f} seconds")
print(df.head())