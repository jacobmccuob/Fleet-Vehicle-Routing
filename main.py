import mapsetup
import driver
import cfg
import folium
import mapfunctions
from threading import *
import order

from flask import Flask, render_template, request
app = Flask(__name__)

#setup to be done initially
@app.before_first_request
def initialise():
    #setup the default map
    mapsetup.setupMap()
    #initialise drivers
    driver.initialiseDrivers()
    cfg.m.save('templates/map.html')

#once app is opened
@app.route("/")
def base():
    #order generation is started
    #t1=Thread(target = order.generateOrders)
    #t1.start()

    #return the placeholder map
    return render_template('index.html')

#when app refreshed    
@app.route("/refresh")
def get_refreshed_map():
    #create new map
    map = folium.Map(location= cfg.city_coords , zoom_start = 14, titles = "Hereford")
    #add all necessary map info to the map
    mapfunctions.renderMap(map)
    map.save('templates/map.html')
    #return the map
    return render_template('index.html')


@app.route('/generate')
def gen():
    order.generateOrder()
    map = folium.Map(location= cfg.city_coords , zoom_start = 14, titles = "Hereford")
    #add all necessary map info to the map
    mapfunctions.renderMap(map)
    map.save('templates/map.html')
    #return the map
    return render_template('index.html')



#run the app in debug to show errors, and do not use the reloader
if __name__ == "__main__":
    app.run(debug = True, use_reloader = False)




    
