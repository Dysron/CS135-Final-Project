from PIL import Image, ImageDraw
from PIL.ImageColor import getrgb


class Plot:

    """
    Provides the ability to map, draw and color regions in a long/lat
    bounding box onto a proportionally scaled image.
    """

    @staticmethod
    def interpolate(x_1, x_2, x_3, newlength):
        """
        linearly interpolates x_2 <= x_1 <= x_3 into newlength
        x_2 and x_3 define a line segment, and x2 falls somewhere between them
        scale the width of the line segment to newlength, and return where
        x_1 falls on the scaled line.
        """
        return newlength*((x_1-x_2)/(x_3-x_2))

    @staticmethod
    def proportional_height(new_width, width, height):
        """
        return a height for new_width that is
        proportional to height with respect to width
        Yields:
            int: a new height
        """
        return (new_width*height)/width

    #code from http://stackoverflow.com/questions/20792445/calculate-rgb-value-for-a-range-of-values-to-create-heat-map
    @staticmethod
    def fill(region,min_rate,max_rate):
        """return the fill color for region according to the given 'style'"""
        minimum, maximum = min_rate, max_rate
        value = region.p_rate()/100
        halfmax = (minimum + maximum) / 2
        if minimum <= value <= halfmax:
            r = 0
            g = int( 255./(halfmax - minimum) * (value - minimum))
            b = int( 255. + -255./(halfmax - minimum)  * (value - minimum))
            return (r,g,b)
        elif halfmax < value <= maximum:
            r = int( 255./(maximum - halfmax) * (value - halfmax))
            g = int( 255. + -255./(maximum - halfmax)  * (value - halfmax))
            b = 0
            return (r,g,b)

    def __init__(self, width, min_long, min_lat, max_long, max_lat):
        """
        Create a width x height image where height is proportional to width
        with respect to the long/lat coordinates.
        """
        self.width = width
        self.min_long = min_long
        self.min_lat = min_lat
        self.max_long = max_long
        self.max_lat = max_lat
        self.height = int(Plot.proportional_height(self.width, (self.max_long-self.min_long), (self.max_lat-self.min_lat)))
        self.im = Image.new("RGB", (self.width, self.height), (255, 255, 255))

    def save(self, filename):
        """save the current image to 'filename'"""
        self.im.save(filename, "PNG")

    def trans_lat(x_1, x_2, x_3, newlength):
        interpolated = Plot.interpolate(x_1, x_2, x_3, newlength)
        return newlength-interpolated

    def draw(self, region, min_rate, max_rate):
        """
        Draws 'region' in the given 'style' at the correct position on the
        current image
        Args:
            region (Region): a Region object with a set of coordinates
            style (str): 'GRAD' or 'SOLID' to determine the polygon's fill
        """
        longs = [Plot.interpolate(_coord[0],self.min_long,self.max_long,self.width) for _coord in region.coords]
        lats = [Plot.trans_lat(_coord[1],self.min_lat,self.max_lat,self.height) for _coord in region.coords]
        interpolated_coords = zip(longs,lats)
        ImageDraw.Draw(self.im).polygon(list(interpolated_coords), fill=Plot.fill(region,min_rate,max_rate), outline=(0,0,0))
