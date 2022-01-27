import requests
import json
import urllib
import cfg
import folium
import order
import driver

#holds location of surrounding petrol stations
petrolstations = []

#removes illegal characters from coordinates for use in API request URL
def sanitise_coords_for_url(coords):
    #holds unwanted characters
    characters_to_remove = " ()'latn}g{:[]"
    #string for sanitised coords
    sanitised_coords = str(coords)
    #for each illegal charactrer
    for character in characters_to_remove:
        #'replace' it with nothing
        sanitised_coords=sanitised_coords.replace(character,"")
    #return the new string without unwanted characters
    return sanitised_coords

#geocoding, takes address and returns coords
def get_coords_of_address(address):
    #parameters to be used in API request
    parameters = {"address": address ,"key": cfg.AUTH_KEY}
    #holds result of geocoding API query using address and key
    r= requests.get(f"{cfg.geocode_url}{urllib.parse.urlencode(parameters)}")
    #load result from json
    data = json.loads(r.content)
    #returnss element of reult indicating location in coordinate form
    return data.get("results")[0].get("geometry").get("location")

#finds nearby petrol stations using nearby search
def display_nearby_petrol_stations(parameters):
    #makes a nearby search query with the given parameters
    petrolreq = requests.get(f"{cfg.nearby_search_url}""&location="+
    (sanitise_coords_for_url(cfg.city_coords))+"&"f"{urllib.parse.urlencode(parameters)}")
    #load result from json
    petroldata = json.loads(petrolreq.content)
    #for each petrol station
    for petrolStation in petroldata.get("results"):
        #store location
        locale = petrolStation.get("geometry").get("location")
        #set the latitude and longitude to a coordinate variable
        coords = (locale['lat'], locale["lng"])
        #add this to list of petrol stations
        petrolstations.append(coords)
        
#check whether a petrol station exists in radius of a location
def exists_petrol_station_within(origin, radius):
    #setup parameters to be passed to API
    parameters = {"radius": radius, "type": "gas_station", "key": cfg.AUTH_KEY}
    #makes a nearby search query with given params
    petrolreq = requests.get(f"{cfg.nearby_search_url}""&location="+
    (sanitise_coords_for_url(origin))+"&"f"{urllib.parse.urlencode(parameters)}")
    #load results from json
    petroldata = json.loads(petrolreq.content)
    #if there are no petrol stations within the radius
    if (petroldata.get("status") == "ZERO_RESULTS"):
        return False
    #if petrol stations are present within the radius
    else :
        return True

#returns the duration in seconds of a drive between a source and destination 
def getDrivingDuration(source, destination):
    #makes a distance matrix request from the source to the destination
    r= requests.get(f"{cfg.distance_matrix_url}""&origins="+(sanitise_coords_for_url
    (source)+"&destinations="+(sanitise_coords_for_url(destination)+"&key="+cfg.AUTH_KEY)))
    #load data from json
    data = json.loads(r.content)
    #return the element of the data containing driving time in seconds
    return data['rows'][0]['elements'][0]['duration']['value']



#render map for when manager refreshes page
def renderMap(map):
    #add marker for the hub
    folium.Marker(location =  cfg.hub_location, popup = "Business",
     tooltip = 'Restaurant', icon=folium.Icon(color='red', icon='cutlery')).add_to(map)
    #for each petrol station
    for station in petrolstations:
        #add a marker to the map
        (folium.Marker(location = station, popup = "petrol",
         tooltip = 'Petrol Station', icon=folium.Icon(color='green', icon= 'wrench'))).add_to(map)
    #for each outstanding order
    for orders in order.outstandingOrders:
        #add a marker to the map
        folium.Marker(location = orders.location, popup = ("Time placed: " +  orders.timeplaced+
         ' Assigned Driver: ' + orders.assignedDriver), tooltip = 'customer').add_to(map)
    #for each driver
    for employee in driver.allDrivers.values():
        #add a marker to the map
        folium.Marker(location=employee.location, popup=('Name: ' + employee.name, ' Fatigue: ' 
        +str(employee.fatigue), ' Fuel  ' + str(employee.fuel), ' State: ' + employee.state), 
        tooltip=employee.name , icon=folium.Icon(color = 'yellow', icon = 'car')).add_to(map)
