import mapfunctions
import folium
import cfg

#setup the placeholder map
def setupMap():
    #marker for the hub
    folium.Marker(location =  cfg.hub_location, popup = "Restaurant",
     tooltip = 'Restaurant', icon=folium.Icon(color='red', icon='cutlery')).add_to(cfg.m)
    #parameters for use in nearby search to find petrol stations
    petrolparams = {"radius": cfg.delivery_radius, "type": "gas_station", "key": cfg.AUTH_KEY}
    #calls function to store nearby petrol station locations in array
    mapfunctions.display_nearby_petrol_stations(petrolparams)
    #for each nearby petrol station
    for station in mapfunctions.petrolstations:
        #add a marker to the map
        (folium.Marker(location = station, popup = "petrol", tooltip = 'Petrol Station',
         icon=folium.Icon(color='green', icon= 'wrench'))).add_to(cfg.m)


    

    

    

