
class Region:
    """
    A region represented by its coordinates poverty_rate).
    """

    def __init__(self, coords,poverty_rate):
        self.coords = coords
        self.poverty_rate = poverty_rate

    def lats(self):
        "Return a list of the latitudes of all the coordinates in the region"
        return [long_lat[1] for long_lat in self.coords]

    def longs(self):
        "Return a list of the longitudes of all the coordinates in the region"
        return [long_lat[0] for long_lat in self.coords]

    def min_lat(self):
        "Return the minimum latitude of the region"
        return min([long_lat[1] for long_lat in self.coords])

    def min_long(self):
        "Return the minimum longitude of the region"
        return min([long_lat[0] for long_lat in self.coords])

    def max_lat(self):
        "Return the maximum latitude of the region"
        return max([long_lat[1] for long_lat in self.coords])

    def max_long(self):
        "Return the maximum longitude of the region"
        return max([long_lat[0] for long_lat in self.coords])

    def p_rate(self):
        "Return the poverty rate of the region"
        return self.poverty_rate
