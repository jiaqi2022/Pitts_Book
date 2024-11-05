import googlemaps
import gmplot
import pprint
import webbrowser
import os
import pandas as pd   

class googleMapApi:

    def __init__(self):
        """Initializer of googleMapApi class
        This method read the Google API key from file, and create GoogleMap Client
        """
        self.api_key = open('GOOG_API_KEY.txt', 'r').read()
        self.gmaps = googlemaps.Client(self.api_key)
        self.gmPlotter = None
        self.pp = pprint.PrettyPrinter()

    def gmPlotter_init(self, location):
        """Initialize GoogleMap Plotter object
        This method setup api key and centre coordinate of the house location
        Add red marker on the house coordinate
        :param location: The latitude and longitude tuple of the house
        """
        latitude = float(location[0])
        longitude = float(location[1])     
        self.gmPlotter = gmplot.GoogleMapPlotter(latitude, longitude, 13)
        self.gmPlotter.apikey = self.api_key
        self.gmPlotter.marker(latitude, longitude, 'blue')
        
    def gmPlotter_heatmap(self, latitude_list, longitude_list): 
        self.gmPlotter.heatmap(latitude_list, longitude_list)

        
    def add_plotter_marker(self, coordinate, color='blue'):
        """Add markers to the Google Map plot you are going to draw
        This method ddd marker on the coordinate
        :param coordinate: The latitude and longitude tuple of the marker
        """
        latitude = float(coordinate[0])
        longitude = float(coordinate[1])
        self.gmPlotter.marker(latitude, longitude, color)

    def draw_and_display_gm_plot(self, filename='my_map.html'):
        """Draw Google Map plot, save to filename and display on browser tab
        This method generate html file of the Google Map drawn, and open on the browser
        :param filename: The file name of output html file
        """
        self.gmPlotter.draw(filename)
        url = 'file:///' + os.getcwd() + '/' + filename
        webbrowser.open_new_tab(url)  # open in new tab
