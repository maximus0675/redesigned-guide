import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import time

# 1. Page Config
st.set_page_config(page_title="Live PLC Dashboard", layout="wide")
st.title("⚡ Live Factory Dashboard")

# 2. Connect to Database (Supabase)
# We use st.secrets for security (explained in Step 3)
# For local testing, replace st.secrets[...] with your actual string 'postgresql://...'
db_url = st.secrets["DB_URL"] 
engine = create_engine(db_url)

# 3. Define the Data Fetching Function
def get_data():
    query = "SELECT created_at, machine_id, temperature, status FROM plc_data ORDER BY created_at DESC LIMIT 50"
    return pd.read_sql(query, engine)

# 4. Create the Dashboard Layout
placeholder = st.empty() # Creates a container that we can overwrite

# 5. The "Live" Loop
while True:
    df = get_data()
    
    # Calculate Metrics
    latest_temp = df.iloc[0]['temperature']
    latest_status = df.iloc[0]['status']
    
    with placeholder.container():
        # KPIs at the top
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label="Latest Temperature", value=f"{latest_temp} °C", delta=f"{latest_temp - 40} vs Target")
        kpi2.metric(label="Machine Status", value=latest_status)
        kpi3.metric(label="Last Update", value=str(df.iloc[0]['created_at'].time())[:8])

        # Charts
        st.subheader("Temperature Trend (Last 50 Readings)")
        st.line_chart(df, x='created_at', y='temperature')

        # Data Table
        st.dataframe(df)
        
    # Wait 2 seconds before refreshing (Simulates "Live" view)
    time.sleep(2)