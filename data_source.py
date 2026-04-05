import requests  # Library for getting data from internet
import pandas as pd  # Library for working with data tables
from datetime import datetime  # Library for working with time

class DataSource:

    def __init__(self):
        # URLs - addresses where we get our data
        self.crypto_url = "https://api.coingecko.com/api/v3/simple/price"

    def get_crypto_prices(self):
        """Get cryptocurrency prices from internet"""
        try:
            # Parameters - what exactly we want to get
            params = {
                'ids': 'bitcoin,ethereum,cardano',  # Which cryptocurrencies
                'vs_currencies': 'usd',  # In which currency (US dollars)
                'include_24hr_change': 'true'  # Include daily changes
            }

            # Send request to get data
            response = requests.get(self.crypto_url, params=params, timeout=10)

            # Check if request was successful
            if response.status_code == 200:
                data = response.json()  # Convert response to Python dictionary

                # Create list to store our cryptocurrency data
                crypto_list = []

                # Process each cryptocurrency
                for coin_name, coin_info in data.items():
                    crypto_list.append({
                        'name': coin_name.title(),  # Cryptocurrency name
                        'price': coin_info['usd'],  # Current price
                        'change': coin_info.get('usd_24h_change', 0),  # 24h change
                        'time': datetime.now()  # When we got this data
                    })

                # Convert list to DataFrame (like Excel table)
                return pd.DataFrame(crypto_list)

        except Exception as error:
                print(f"Error getting crypto data: {error}")
                return pd.DataFrame()  # Return empty table if error
        
    def get_sample_weather(self):
        """Get sample weather data (for demonstration)"""
        # For beginners, we'll use sample data instead of real API
        return {
            'temperature': 22,
            'humidity': 65,
            'city': 'London',
            'description': 'Sunny',
            'time': datetime.now()
        }   