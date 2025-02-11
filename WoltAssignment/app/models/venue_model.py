class Venue:
    def __init__(self, name, coordinates, order_minimum, base_price, distance_ranges):
        self._name = name
        self._coordinates = coordinates  # Tuple (lon, lat)
        self._order_minimum = order_minimum
        self._base_price = base_price
        self._distance_ranges = distance_ranges

    # Encapsulated Getters
    def get_name(self):
        return self._name

    def get_coordinates(self):
        return self._coordinates

    def get_order_minimum(self):
        return self._order_minimum

    def get_base_price(self):
        return self._base_price

    def get_distance_ranges(self):
        return self._distance_ranges

    def to_dict(self):
        return {
            "name": self._name,
            "coordinates": self._coordinates,
            "order_minimum": self._order_minimum,
            "base_price": self._base_price,
            "distance_ranges": self._distance_ranges
        }
