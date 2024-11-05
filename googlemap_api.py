import googlemaps
import re

# in order to initialize the googleMapAPI, you need to allow billing on google 
# cloud for googlemapAPI and update the 'GOOG_API_KEY.txt' with your key if the 
# original key text is not working

class googleMapApi:

    def __init__(self):
        # Initializer of googleMapApi class which read the Google API key from file, and create GoogleMap Client
        self.api_key = open('GOOG_API_KEY.txt', 'r').read()
        self.gmaps = googlemaps.Client(self.api_key)
        self.gmPlotter = None

    def get_coordinator_by_address(self, addr_string):
        response = self.gmaps.places(addr_string)
        location = response.get('results')[0].get('geometry').get('location')
        return location.get('lat'), location.get('lng')

    def search_nearby(self, location, search_string, distance=2000):
        # Make the GoogleMap places API call and reformat the response
        # This method extract the 'name' and 'rating' field from API response

        # :param location: The latitude and longitude tuple
        # :param search_string: for GoogleMap places API keyword 
        # :param distance: distance used for GoogleMap places API radius search, default=2000 meters
        # :return:  result dictionary of GoogleMap places API call

        response = self.gmaps.places_nearby(
            location=location,
            keyword=search_string,
            radius=distance,
        )
        result_dict = {}
        for result in response.get('results'):
            result_dict[result["name"]] = float(result['rating'])

        return result_dict

    def get_distance(self, src_loc, dst_loc, mode="transit", avoid="tolls", ):
        # Make the GoogleMap Distance Matrix API call and reformat the response
        # This method extract the 'distance' and 'duration' field from API response

        # :param src_loc: The latitude and longitude tuple of the origin
        # :param dst_loc: The latitude and longitude tuple of the destination
        # :param mode: The mode of transit that from user inputs, default="transit"(can be 'driving'/'walking'/'cycling')
        # :param avoid: avoid used for GoogleMap Distance API avoid arg
        # :return: result dictionary of GoogleMap places API call
        
        response = self.gmaps.directions(src_loc, dst_loc,
                                         mode=mode, avoid=avoid,
                                         departure_time="now")
        distance = response[0]['legs'][0]['distance']['text']
        duration = response[0]['legs'][0]['duration']['text']
        return {"distance": distance, "duration": duration}

    def calculate_transportation_score(self, src_loc, dst_loc, transit_mode):
        # Calculate the score of the transportation by considering number of nearby bus stops,distance and duration 

        # :param src_loc: The latitude and longitude tuple of the starting location
        # :param dst_loc: The latitude and longitude tuple of the tourist attraction
        # :param transit_mode: The transit method that from user input
        # :return: The transit score, total score of tourist attraction normalized to out of 100
        
        dist_matrix = self.get_distance(src_loc, dst_loc, transit_mode)
        bus_stops = self.search_nearby(src_loc, 'bus stop', distance=500)
        duration = [int(s) for s in dist_matrix.get('duration').split() if s.isdigit()][0]
        distance = float(re.findall("\d+\.\d+", dist_matrix.get('distance'))[0])
        return (100 - duration) * 0.8 + (100 - distance) * 0.1 + len(bus_stops.keys())


if __name__ == '__main__':
    print("Testing Google Map API")

    my_geolocation = (40.455795218277885, -79.93804539306154)
    phipps_geolocation = (40.44019469951259, -79.9484382696617)

    gma = googleMapApi()

    # Test 
    print(gma.search_nearby(my_geolocation, 'restaurant', distance=2000))
    print(gma.get_distance(my_geolocation, phipps_geolocation, mode="driving", avoid="tolls", ))
    print(gma.get_distance(my_geolocation, phipps_geolocation, mode="transit", avoid="tolls", ))
    print(gma.calculate_transportation_score(my_geolocation, phipps_geolocation, "transit"))

# reference:
# https://developers.google.com/maps/documentation/javascript/examples/directions-travel-modes 
