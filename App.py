import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA

# Load data
@st.cache_data
def load_data():
    orders_with_details = pd.read_csv('Data/prepared_restaurant_data.csv')
    orders_with_details['order_datetime'] = pd.to_datetime(orders_with_details['order_datetime'])
    return orders_with_details

data = load_data()

st.title('🍽️ Restaurant Operations Dashboard')

# Sidebar for filtering
st.sidebar.header('Filters')
date_range = st.sidebar.date_input('Select Date Range', [data['order_datetime'].min(), data['order_datetime'].max()])

# Filter data based on date range
filtered_data = data[(data['order_datetime'].dt.date >= date_range[0]) & (data['order_datetime'].dt.date <= date_range[1])]

# Overview metrics
st.header('Overview')
col1, col2, col3 = st.columns(3)
col1.metric('Total Orders', len(filtered_data))
col2.metric('Total Revenue', f"${filtered_data['price'].sum():.2f}")
col3.metric('Average Order Value', f"${filtered_data['price'].mean():.2f}")

# Hourly order trend
st.header('Hourly Order Trend')
hourly_orders = filtered_data.groupby(filtered_data['order_datetime'].dt.hour)['order_id'].count()
fig, ax = plt.subplots()
sns.lineplot(x=hourly_orders.index, y=hourly_orders.values, ax=ax)
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Number of Orders')
st.pyplot(fig)

# Top selling items
st.header('Top Selling Items')
top_items = filtered_data['item_name'].value_counts().head(10)
st.bar_chart(top_items)

# ARIMA Forecast
st.header('Order Forecast (Next 24 Hours)')
# Prepare data for ARIMA
ts_data = filtered_data.set_index('order_datetime')['order_id'].resample('H').count()
model = ARIMA(ts_data, order=(1,1,1))
results = model.fit()
forecast = results.forecast(steps=24)
st.line_chart(forecast)

# Recommendations based on analysis
st.header('Recommendations')
st.write("1. Optimize staffing during peak hours (see Hourly Order Trend)")
st.write("2. Consider promotions for top-selling items to boost sales")
st.write("3. Prepare for forecasted order volumes to ensure smooth operations")

# Add more visualizations and insights as needed

st.sidebar.info('This dashboard provides real-time insights into restaurant operations, helping optimize staffing, inventory, and marketing strategies.')