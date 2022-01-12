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
    df.sale_date = pd.to_datetime(df.sale_date)
    df = df.set_index("sale_date").sort_index()
    df['month'] = df.index.month_name()
    df['day'] = df.index.day_name()
    df['sales_total'] = df.sale_amount * df.item_price


    sns.barplot(y='sale_amount', x='item_price', data=df)
    plt.xticks(rotation = 60)
    plt.tight_layout
    
    return df