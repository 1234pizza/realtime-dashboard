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

    # 1. Create page title and header
    st.title("📊 My First Real-time Dashboard")
    st.markdown("Welcome to live data visualization!")
    st.markdown("---")  # Horizontal line separator

    # 2. Create sidebar with controls
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

    # 3. Initialize our data source and chart creator
    data_source = DataSource()
    chart_creator = ChartCreator()

    # 4. Create containers for our content (these stay fixed, but their contents change)
    status_container = st.empty()   # For status messages
    metrics_container = st.empty()  # For summary metrics
    crypto_container = st.empty()   # For cryptocurrency chart
    weather_container = st.empty()  # For weather information

    update_count = 0  # Count how many times we've updated

    # 5. Main loop for updating data (MUST be inside main to see auto_refresh)
    while auto_refresh:
        update_count += 1
        
        # Get the current time for the status message
        current_time = datetime.now().strftime("%H:%M:%S")
        status_container.info(f"Last updated: {current_time} (Update #{update_count})")

        # Fetch data from our sources
        # (Assuming these methods exist in your DataSource class)
        weather_data = data_source.get_sample_weather()
        crypto_data = data_source.get_crypto_data() 

        # Display Weather Metrics
        with weather_container.container():
            st.subheader("Local Weather")
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
            with col3:
                st.write(f"**City:** {weather_data['city']}")
                st.write(f"**Condition:** {weather_data['description']}")

        # Display Crypto Chart
        with crypto_container.container():
            st.subheader("Market Trends")
            # Create the figure using your ChartCreator class
            fig = chart_creator.create_crypto_chart(crypto_data)
            st.plotly_chart(fig, use_container_width=True, key=f"chart_{update_count}")

        # Wait for the specified interval before the next update
        time.sleep(refresh_interval)

# This line tells Python to actually run the main function when the file loads
if __name__ == "__main__":
    main()