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

    # 1. Page Setup
    st.title("📊 My First Real-time Dashboard")
    st.markdown("Welcome to live data visualization!")
    st.markdown("---")

    # 2. Sidebar Controls
    st.sidebar.header("Dashboard Settings")
    auto_refresh = st.sidebar.checkbox(
        "Enable Auto Refresh",
        value=True,
        help="Automatically update data every few seconds"
    )

    refresh_interval = st.sidebar.slider(
        "Update Every (seconds)",
        min_value=5,
        max_value=30,
        value=10
    )

    # 3. Initialize Classes
    data_source = DataSource()
    chart_creator = ChartCreator()

    # 4. Content Containers (Only status and crypto now)
    status_container = st.empty()
    crypto_container = st.empty()

    update_count = 0

    # 5. The Live Update Loop
    while auto_refresh:
        update_count += 1
        
        # Update Status
        current_time = datetime.now().strftime("%H:%M:%S")
        status_container.info(f"Last updated: {current_time} (Update #{update_count})")

        # Fetch Crypto Data
        crypto_data = data_source.get_crypto_data()

        # --- CRYPTO SECTION ---
        if crypto_data is not None and not crypto_data.empty:
            with crypto_container.container():
                st.subheader("Market Trends")
                # Create the figure using your ChartCreator class
                fig = chart_creator.create_crypto_chart(crypto_data)
                # Display the chart with a unique key
                st.plotly_chart(fig, use_container_width=True, key=f"chart_{update_count}")
        else:
            crypto_container.warning("No crypto data available...")

        # 6. The Wait (Crucial for loop stability)
        time.sleep(refresh_interval)

# The Ignition Switch
if __name__ == "__main__":
    main()