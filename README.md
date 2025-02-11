## Delivery Order Price Calculator service (DOPC)

This project calculates the delivery order price based on user location, venue details, and cart value. It fetches venue information from external APIs and uses the Haversine formula to calculate the delivery distance.

## Features

- Fetches venue data from static and dynamic APIs.
- Calculates delivery order price, including delivery fee, small order surcharge, and distance.
- Provides a RESTful API endpoint for calculating delivery order price.

## Setup

***Ensure that you have Python 3.7 or later installed.

# Install dependencies:
  pip install -r requirements.txt

# Running the Project 
  CMD/Powershel: python run.py

# Example Request:
```bash
  curl "http://127.0.0.1:5003/api/v1/delivery-order-price?venue_slug=some-venue&cart_value=50&user_lat=60.1699&user_lon=24.9384"

```
*** remember to add "" in the url

# Example Response:
```json
    {
        "delivery_price": {
            "cart_value": 1000,
            "delivery": {
                "distance": 177,
                "fee": 190
            },
            "small_order_surcharge": 0,
        "total_price": 1190
        }
    }

