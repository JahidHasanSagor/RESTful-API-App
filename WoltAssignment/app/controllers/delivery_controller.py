# app/controllers/delivery_controller.py
from flask import Flask, request, jsonify
from app.services.delivery_service import fetch_venue_data
from app.utils.helper_distance_calculation import calculate_distance

app = Flask(__name__)  # Initialize Flask app instance

# Register the route directly without Blueprint
@app.route('/api/v1/delivery-order-price', methods=['GET'])
def calculate_delivery_order_price():
    # Extract query parameters
    venue_slug = request.args.get('venue_slug')
    cart_value = request.args.get('cart_value', type=int)
    user_lat = request.args.get('user_lat', type=float)
    user_lon = request.args.get('user_lon', type=float)

    # Call the service to get venue data
    venue = fetch_venue_data(venue_slug)
    if venue is None:
        return jsonify({"error": "Failed to fetch venue data."}), 400

    # Calculate distance using helper function
    distance = calculate_distance(user_lat, user_lon, venue.get_coordinates()[1], venue.get_coordinates()[0])

    # Determine delivery fee
    delivery_fee = None
    for range_ in venue.get_distance_ranges():
        if range_['min'] <= distance < range_['max'] or range_['max'] == 0:
            delivery_fee = venue.get_base_price() + range_['a'] + round(range_['b'] * distance / 10)
            break

    if delivery_fee is None:
        return jsonify({"error": "Delivery not possible for the given distance."}), 400

    # Calculate small order surcharge
    small_order_surcharge = max(0, venue.get_order_minimum() - cart_value)

    # Calculate total price
    total_price = cart_value + small_order_surcharge + delivery_fee

    # Construct the response
    response = {
        "delivery_price": {
            "cart_value": cart_value,
            "delivery": {
                "distance": round(distance),
                "fee": delivery_fee
            },
            "small_order_surcharge": small_order_surcharge,
            "total_price": total_price
        }
    }

    return jsonify(response)
