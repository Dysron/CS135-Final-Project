import collections
import os
import csv
import math
import sys
import matplotlib.pyplot as plt
import requests
from PIL import Image
from plot import Plot
from region import Region
import configparser

def mercator(lat):
    """project latitude 'lat' according to Mercator"""
    lat_rad = (lat * math.pi) / 180
    projection = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))
    return (180 * projection) / math.pi

def to_point(list_coords):
    new_list = []
    for coords in list_coords:
        new_list.append((coords[0],mercator(float(coords[1]))))
    return new_list

def getSaipeData(year):
    config = configparser.ConfigParser()
    config.read("config.ini")
    """ 
    return a list of all the poverty data less the header for the given year
    """
    params = {"time":str(year), "for":"county:*",
              "in":"state:*" , "key":config["DEFAULT"]["key"]}
    r = requests.get("https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,STABREV,COUNTY,SAEPOVRTALL_PT",params)

    # list in the format [countyName,stateAbbreviation,countyNumber, poverty %,year,stateNumber,countyNumber]
    return r.json()[1:]

def convert_to_dict(saipe_data):
    """
    takes saipe data and creates a dictionary mapping the state to a county to a poverty percentage
    :return: dictionary
    """
    d = dict()
    for line in saipe_data:
        state=line[1]
        full_county_name = line[0]
        split_county_name = full_county_name.split()
        county = " ".join(split_county_name[:len(split_county_name)-1])
        poverty_percentage = float(line[3])
        if state in d:
            d[state][county] = poverty_percentage
        else:
            d[state] = dict()
    return d

def stitchImages(image1, image2,name):
    img1 = Image.open(image1)
    img2 = Image.open(image2)
    combinedWidth = img1.size[0] + img2.size[0]
    maxHeight = max(img1.size[1],img2.size[1])
    img3 = Image.new("RGB",(combinedWidth,maxHeight))
    img3.paste(img1, (0,0))
    img3.paste(img2, (img1.size[0],0))
    img3.save(name,"PNG")

def US_map(boundaries, width, year):
    """
    Draws an image.
    This function creates an image object, constructs Region objects by reading
    in data from csv files, and draws polygons on the image based on those Regions

    Args:
        boundaries (str): .csv file with boundaries
        width (int): width of the image
        year (str): year of data
    """
    # Alaska and Hawaii aren't in the boundary data
    saipe = convert_to_dict([x for x in getSaipeData(year) if x[1]!="AK" and x[1]!="HI"])
    region_list = []

    with open(boundaries) as file1:
        f1 = csv.reader(file1)
        for line in f1:
            state = line[1]
            county  = line[0]
            pov = saipe[state].get(county,0)
            xValues = line[2::2]
            yValues = line[3::2]
            coords = [(float(x),float(y)) for x,y in zip(xValues,yValues)]
            coords2 = to_point(coords)
            region_list.append(Region(coords2,float(pov)))
     
    region_min_long = min(r.min_long() for r in region_list)
    region_max_long = max(r.max_long() for r in region_list)
    region_min_lat = min(r.min_lat() for r in region_list)
    region_max_lat = max(r.max_lat() for r in region_list)
    min_p_rate = (min(r.p_rate() for r in region_list))/100
    max_p_rate = (max(r.p_rate() for r in region_list))/100
    p = Plot(width, region_min_long, region_min_lat, region_max_long, region_max_lat)
    for r in region_list:
        p.draw(r,min_p_rate,max_p_rate)
    p.save(str(year)+"map_output.png")

def create_subplots(rows,columns,x_data,y_data, annotations=False, index=0):
    """
    creates a matplotlib figure with uniform # of rows, column, and data with annotations
    :param rows: the amount of rows each subplot should use
    :param columns: the amount of columns each subplot should use
    :param x_data: list of x coordinates for each subplot
    :param y_data: list of y coordinates for each subplot
    :param annotations: whether annotations hsould be on the subplots or not
    :param annotation_index: where in the data the annotations should come from
    :return: figure with data given
    """
    count = 0
    fig = plt.figure()
    for key in iter(y_data):
        ax = fig.add_subplot(rows,columns,count+1)
        ax.plot(x_data,y_data[key])
        ax.set_xlabel("Year")
        ax.set_ylabel("rate per 100,000 people")
        ax.set_title(key + " in " + str(x_data[index]))
        x_y = (x_data[index],y_data[key][index])
        ax.axvline(x=year, color = 'red')
        ax.annotate(str(x_y[1]), xy=x_y)
        count+=1
    plt.tight_layout()
    return plt

def crime_graph(crime_data, year, year_range):
    """
    Create line graph of out of crime rate data and the years
    :param crime_data: name of .csv file containing crime statistics
    :param year: year of data
    :param year_range: list containing years to plot on graph
    :return:
    """

    ## dictionary doesn't maintain order, so an ordereddcit would make creating subplots in the same position easier
    c = collections.OrderedDict()
    index = year_range.index(year)
    with open(crime_data) as file2:
        f2 = csv.reader(file2)
        for line in f2:
            try:
                if int(line[0]) in year_range:
                    # crime rates per 100,000 people
                    c['Violent Crime rate'] = c.setdefault('Violent Crime rate',list()) + [float(line[2])]
                    c['Property crime rate'] = c.setdefault('Property crime rate',list()) + [float(line[8])]
            except: continue
    x_values = year_range
    y_values = c
    graph = create_subplots(len(c),1,x_values,y_values,annotations=True,index=x_values.index(year))
    graph.savefig(str(year)+"graph_output.png")

if __name__ == '__main__':
    crime_data = sys.argv[1]
    boundaries = sys.argv[2]
    yearStart = int(sys.argv[3])
    yearEnd = int(sys.argv[4])+1
    width = int(sys.argv[5])
    year_range = list(range(yearStart,yearEnd))
    for year in year_range:
        US_map(boundaries, width, year)
        crime_graph(crime_data, year, year_range)
        mapName = str(year)+"map_output.png"
        graphName = str(year)+"graph_output.png"
        stitchImages(mapName,graphName, str(year)+"stitched.png")
        os.remove(mapName)
        os.remove(graphName)

# $ python3 crime_poverty.py statistic-data/crimes/USCrimeRates.csv statistic-data/boundaries/US.csv 1999 2015 1024
# https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,STABREV,COUNTY&for=county:*&in=state:53&time=2015&key=
