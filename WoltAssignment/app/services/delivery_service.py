import requests
from app.models.venue_model import Venue

def fetch_venue_data(venue_slug):
    static_url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/static"
    dynamic_url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/dynamic"

    try:
        # Make requests to both the static and dynamic URLs
        static_response = requests.get(static_url)
        dynamic_response = requests.get(dynamic_url)

        # Check if the responses are successful
        static_response.raise_for_status()  # This will raise an exception for 4xx/5xx status codes
        dynamic_response.raise_for_status()  # This will raise an exception for 4xx/5xx status codes

        # If successful, parse the JSON responses
        static_data = static_response.json()
        dynamic_data = dynamic_response.json()

        # Return the Venue object
        return Venue(
            name=venue_slug,
            coordinates=tuple(static_data['venue_raw']['location']['coordinates']),
            order_minimum=dynamic_data['venue_raw']['delivery_specs']['order_minimum_no_surcharge'],
            base_price=dynamic_data['venue_raw']['delivery_specs']['delivery_pricing']['base_price'],
            distance_ranges=dynamic_data['venue_raw']['delivery_specs']['delivery_pricing']['distance_ranges']
        )
    
    except requests.exceptions.RequestException as e:
        # Handle any exception that occurs during the API request
        print(f"Error during API request: {e}")
        return None  # You can return None or any error message you'd like
