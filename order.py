import time
import datetime
import random
import orderhandler
import mapfunctions
import cfg

#holds outstanding orders
outstandingOrders = []

#simulates customer orders
def generateOrders():
    #takes addresses from an external file with sample addresses
    customerFile = open (cfg.customerFile)
    lines = customerFile.readlines()
    #randomises addresses
    random.shuffle(lines)

    #for each address
    for i in lines:
        #wait 30 seconds before putting order through
        time.sleep(5*cfg.timescale)
        print("Order recieved")
        #use geocoding to translate address to coords
        locale = mapfunctions.get_coords_of_address(i)
        #set location to the coordinates returned by mapfunctions
        location = (locale['lat'], locale['lng'])
        #create order object with current time
        newOrder = Order(location, datetime.datetime.now().strftime("%H:%M:%S"))
        newOrder.setAssignedDriver('pending')
        #call orderhandler to assign a driver to the order
        orderhandler.assignDriverToOrder(newOrder)
        #add order to list of outstanding orders
        outstandingOrders.append(newOrder)
        
#simulates customer orders
def generateOrder():
    #takes addresses from an external file with sample addresses
    customerFile = open (cfg.customerFile)
    lines = customerFile.readlines()
    #randomises addresses
    random.shuffle(lines)

    i = lines[0]
    print("Order recieved")
    #use geocoding to translate address to coords
    locale = mapfunctions.get_coords_of_address(i)
    #set location to the coordinates returned by mapfunctions
    location = (locale['lat'], locale['lng'])
    #create order object with current time
    newOrder = Order(location, datetime.datetime.now().strftime("%H:%M:%S"))
    newOrder.setAssignedDriver('pending')
    #call orderhandler to assign a driver to the order
    orderhandler.assignDriverToOrder(newOrder)
    #add order to list of outstanding orders
    outstandingOrders.append(newOrder)
        
     

     

class Order:

    #constructor method taking params as attributes
    def __init__(self, location, timeplaced):
        self.location = location
        self.timeplaced = timeplaced
        self.assignedDriver = 'pending'
    
    #setter method for assigning a driver to order
    def setAssignedDriver(self, employee):
        self.assignedDriver = employee
