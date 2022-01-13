import pandas as pd
from datetime import timedelta, datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

import warnings
warnings.filterwarnings("ignore")

from acquire import get_store_data

# plotting defaults
plt.rc('figure', figsize=(13, 7))
plt.style.use('seaborn-whitegrid')
plt.rc('font', size=16)

def prep_store_data(df):
    # Convert date column to datetime format
    df.sale_date = pd.to_datetime(df.sale_date)# consider placing some datetime format= code here to speed the processing
    # Set the index to be the datetime variable.
    df = df.set_index("sale_date").sort_index()
    # Add a 'month' and 'day of week' column to your dataframe.
    df['month'] = df.index.month_name()
    df['day'] = df.index.day_name()
    # Add a 'sales_total' column, which is a derived from sale_amount (total items) and item_price
    df['sales_total'] = df.sale_amount * df.item_price
    # Plot the distribution of sale_amount and item_price and sales_total
    df[['sale_amount','item_price','sales_total']].hist()
    return df




def prep_ops_data():
    # Acquire the raw ops data
    df = pd.read_csv("https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv")
    # Convert date column to datetime format.
    df.Date = pd.to_datetime(df.Date)
    # Set the index to be the datetime variable.
    df = df.set_index("Date").sort_index()
    # Plot the distribution of each of your variables.
    df.hist()
    # Add a month and a year column to your dataframe
    df['year'] = df.index.year
    df['month'] = df.index.month_name()
    # Fill any missing values
    df = df.fillna(0)
    return df


