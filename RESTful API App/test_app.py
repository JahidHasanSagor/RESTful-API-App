import unittest
from unittest.mock import patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.controllers.delivery_controller import app  # Import your Flask app

class TestDeliveryOrderPriceAPI(unittest.TestCase):
    def setUp(self):
        # Set up the test client for the Flask app
        self.client = app.test_client()
        self.base_url = "/api/v1/delivery-order-price"
    
    # Test case for a valid request
    def test_valid_request(self):
        response = self.client.get(
            f"{self.base_url}?venue_slug=home-assignment-venue-helsinki&cart_value=1500&user_lat=60.1699&user_lon=24.9384"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("total_price", data)
        self.assertIn("delivery", data)

    # Test case for missing query parameter
    def test_dynamic_missing_parameters(self):
        required_params = {
            "venue_slug": "home-assignment-venue-helsinki",
            "cart_value": "1500",
            "user_lat": "60.1699",
            "user_lon": "24.9384"
        }
        for missing_param in required_params:
            test_params = required_params.copy()
            del test_params[missing_param]  # Remove one parameter
            query_string = "&".join([f"{key}={value}" for key, value in test_params.items()])
            response = self.client.get(f"{self.base_url}?{query_string}")
            self.assertEqual(response.status_code, 400)
            data = response.json
            self.assertIn("error", data)
            self.assertEqual(data["error"], f"Missing required query parameter: {missing_param}")

    # Test case for invalid venue slug
    def test_invalid_venue_slug(self):
        response = self.client.get(
            f"{self.base_url}?venue_slug=invalid-venue&cart_value=1500&user_lat=60.1699&user_lon=24.9384"
        )
        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Failed to fetch venue data.")

    # Test case for invalid data types
    def test_invalid_data_types(self):
        response = self.client.get(
            f"{self.base_url}?venue_slug=home-assignment-venue-helsinki&cart_value=abc&user_lat=abc&user_lon=24.9384"
        )
        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid data type for one or more parameters.")

    # Test case for delivery not possible
    def test_delivery_not_possible(self):
        response = self.client.get(
            f"{self.base_url}?venue_slug=home-assignment-venue-helsinki&cart_value=1500&user_lat=0.0&user_lon=0.0"
        )
        self.assertEqual(response.status_code, 400)
        data = response.json
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Delivery not possible for the given distance.")

    # Test case for small order surcharge
    def test_small_order_surcharge(self):
        response = self.client.get(
            f"{self.base_url}?venue_slug=home-assignment-venue-helsinki&cart_value=500&user_lat=60.1699&user_lon=24.9384"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn("small_order_surcharge", data)
        self.assertGreater(data["small_order_surcharge"], 0)

    # Mock the external API call to simulate failure
    def test_api_failure_handling(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 500
            response = self.client.get(
                f"{self.base_url}?venue_slug=home-assignment-venue-helsinki&cart_value=1500&user_lat=60.1699&user_lon=24.9384"
            )
            self.assertEqual(response.status_code, 400)
            data = response.json
            self.assertIn("error", data)
            self.assertEqual(data["error"], "Failed to fetch venue data.")


if __name__ == "__main__":
    unittest.main()
