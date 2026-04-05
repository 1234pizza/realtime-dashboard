import streamlit as st  # Web app framework
import time  # For creating delays
from datetime import datetime  # For working with time
from data_source import DataSource  # Our data getting class
from charts import ChartCreator  # Our chart creating class

# Configure our web page
st.set_page_config(
    page_title="My First Real-time Dashboard",  # Browser tab title
    page_icon="📊",  # Browser tab icon
    layout="wide",  # Use full width of browser
    initial_sidebar_state="expanded"  # Show sidebar by default
    )

def main():
    """Main function that runs our dashboard"""

    # Create page title
    st.title("📊 My First Real-time Dashboard")
    st.markdown("Welcome to live data visualization!")
    st.markdown("---")  # Horizontal line separator

    # Create sidebar with controls
    st.sidebar.header("Dashboard Settings")
    st.sidebar.write("Use these controls to customize your dashboard")

    # Auto-refresh checkbox
    auto_refresh = st.sidebar.checkbox(
    "Enable Auto Refresh",
    value=True,
    help="Automatically update data every few seconds"
    )

# Refresh interval slider
refresh_interval = st.sidebar.slider(
    "Update Every (seconds)",
    min_value=5,   # Minimum 5 seconds
    max_value=30,  # Maximum 30 seconds
    value=10,      # Default 10 seconds
    help="How often to get new data"
)

# Information about what we're doing
st.sidebar.markdown("### What This Dashboard Shows:")
st.sidebar.write("• Live cryptocurrency prices")
st.sidebar.write("• Weather information")
st.sidebar.write("• Data updates automatically")

# Initialize our data source and chart creator
data_source = DataSource()
chart_creator = ChartCreator()

# Create containers for our content (these will update automatically)
status_container = st.empty()  # For status messages
metrics_container = st.empty() # For summary metrics
crypto_container = st.empty()  # For cryptocurrency chart
weather_container = st.empty() # For weather information

# Main loop for updating data
update_count = 0  # Count how many times we've updated

# --- INSIDE THE WHILE LOOP ---
while auto_refresh:
    update_count += 1
    
    # 1. Update Status Container
    status_container.info(f"Refreshed {update_count} times. Last update: {datetime.now().strftime('%H:%M:%S')}")

    # 2. Fetch Data
    crypto_data = data_source.get_crypto_data() # Assuming this method exists
    weather_data = data_source.get_sample_weather()

    # 3. Display Weather (Passing unique key to avoid conflicts)
    with weather_container.container():
        st.subheader("Current Weather")
        # We use the update_count in the key to force a fresh render
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="Temperature", 
                value=f"{weather_data['temperature']}°C",
                key=f"temp_{update_count}"
            )
        with col2:
            st.metric(
                label="Humidity", 
                value=f"{weather_data['humidity']}%",
                key=f"hum_{update_count}"
            )

    # 4. Display Crypto Chart
    with crypto_container.container():
        fig = chart_creator.create_crypto_chart(crypto_data)
        st.plotly_chart(fig, use_container_width=True, key=f"chart_{update_count}")

    # 5. Wait for the user-defined interval
    time.sleep(refresh_interval)