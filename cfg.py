import folium

#url parameters hold first part of API request URLS
geocode_url= "https://maps.googleapis.com/maps/api/geocode/json?"
nearby_search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
distance_matrix_url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
#google API key
AUTH_KEY = "AIzaSyDOvtOv1J4nqblmRc-Ww123_JPQpgAtsJM"

#variables for location of business and surrounding town/city
customerFile = 'herefordcustomers.txt'
city_coords =  52.0564,-2.7160 #52.486217, -1.890399

hub_location =  52.0591716,-2.7090934 #52.484412, -1.890602

delivery_radius = 6000
#modifier for simulation timescale, 1 is normal time, 0.1 is 10x speed, 2 is 1/2 speed
timescale = 0.1

#holds base map for use before simulation begins
m = folium.Map(location= city_coords , zoom_start = 14, titles = "Hereford")