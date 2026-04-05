import plotly.graph_objects as go  # Main plotting library
import plotly.express as px  # Simplified plotting functions
import streamlit as st  # Web interface library


class ChartCreator:

    def create_crypto_chart(self, crypto_data):
        """Create beautiful chart for cryptocurrency prices"""

        # Check if we have data to display
        if crypto_data.empty:
            return go.Figure()  # Return empty chart

        # Create new figure (empty chart container)
        fig = go.Figure()

        # Add bars to our chart
        fig.add_trace(go.Bar(
            x=crypto_data['name'],  # X-axis: cryptocurrency names
            y=crypto_data['price'],  # Y-axis: prices
            text=[f"${price:.2f}" for price in crypto_data['price']],  # Text on bars
            textposition='auto',  # Automatic text positioning
            marker_color=[
                'green' if change >= 0 else 'red'
                for change in crypto_data['change']
            ],  # Green for positive, red for negative changes
            name='Cryptocurrency Prices'  # Legend name
        ))

        # Customize chart appearance
        fig.update_layout(
            title="Live Cryptocurrency Prices",  # Chart title
            xaxis_title="Cryptocurrency",       # X-axis label
            yaxis_title="Price (USD)",          # Y-axis label
            height=400,                         # Chart height in pixels
            template="plotly_dark"              # Color theme
        )

        return fig

    def create_summary_metrics(self, crypto_data):
        """Create summary information about our data"""

        if not crypto_data.empty:
            # Calculate metrics
            avg_change = crypto_data['change'].mean()
            max_price = crypto_data['price'].max()
            min_price = crypto_data['price'].min()

            # Display summary metrics in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Avg 24h Change", f"{avg_change:.2f}%")
            with col2:
                st.metric("Highest Price", f"${max_price:,.2f}")
            with col3:
                st.metric("Lowest Price", f"${min_price:,.2f}")