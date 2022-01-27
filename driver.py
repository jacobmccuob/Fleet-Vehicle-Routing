import cfg
import csv
import mapfunctions
import time
import orderhandler
import threading
import order

#initialises data structure to hold driver objects
allDrivers = {}

#sets up driver objects
def initialiseDrivers():
    #open the external driver info file
    with open ('driverinfo.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter =',')
        line_count = 0
        #for each row
        for row in csv_reader:
            #skip the first line of the file
            if line_count == 0:
                line_count += 1
            #for every other line
            else:
                #using driver id as the key, store a driver
                #object constructed using parameters from the file
                allDrivers[row[1]] = (Driver(row[0],row[1],row[2],row[3]))
    #for each driver object
    for employee in allDrivers.values():
        #begin a thread to handle their AI
        employee.startThread()

#driver object class
class Driver:
    
    #constructor method, params are passed through the driver info file
    def __init__(self, name, id, home_address, desired_stops):
        #set params as attributes
        self.name = name
        self.id = id
        self.home_address = home_address
        self.desired_stops = desired_stops

        #initialise other attributes to default
        self.fatigue = 0
        self.fuel = 10000
        self.location = cfg.hub_location
        self.state = "idle"
        self.assignedOrder = 'none'

    #accept order and commence delivery
    def acceptOrder(self, currentOrder, duration):
        #set state to delivering
        self.state  = 'delivering'
        #set the order's assigned driver to the current driver
        currentOrder.setAssignedDriver(self.name)
        #drive to the order locatrion
        self.driveto(currentOrder.location, duration)
        print("order completed")
        #check that the order delivered is the same as the one assigned to the driver 
        #if(currentOrder != self.assignedOrder ):
            #orderhandler.assignDriverToOrder(self.assignedOrder)
        #remove order from outstanding orders. No other drivers will be assigned and marker will disappear
        order.outstandingOrders.remove(currentOrder)
        #remove driver's assignment
        self.assignedOrder = 'none'
        #return to idle state
        self.state = 'idle'

    #setter method for assigning an order to the driver
    def setAssignedOrder(self, order, duration):
        self.assignedOrder = (order, duration)

    #setter method for changing driver state
    def setState(self, state):
        self.state = state

    #todo when the driver is idle
    def idle(self):
        #ensure state is correct
        self.state = 'idle'
        #if driver is too tired
        if self.fatigue > 10800:
            #have a break
            self.rest()
        #if fuel is running a bit low
        if self.fuel < 1000:
            #go and get fuel
            self.refuel()
        #if an order has been assigned to the driver
        if self.assignedOrder != 'none':
            #accept the order
            self.acceptOrder(self.assignedOrder[0], self.assignedOrder[1])
        #for each outstanding order
        for queuedOrder in order.outstandingOrders:
            #if no other driver is currently seeing to it
            if queuedOrder.assignedDriver == 'none':
                #assign the order to the driver
                orderhandler.assignDriverToOrder(queuedOrder)
                #breaks to the other break statement to exit both loops
                break
            #if another driver is seeing to it, examine the next outstanding order
            else:
                continue
            #will be reached if the first break happens
            break

    #if driver requests a personal stop
    def makePersonalStop(self):
        #set state accordingly
        self.state = 'personal'
        #geocode the address
        personalstopcoords = mapfunctions.get_coords_of_address(self.desired_stops)
        #find how long it takes to drive there from driver's current location
        duration = mapfunctions.getDrivingDuration(personalstopcoords, self.location)
        self.driveto(personalstopcoords,duration)
        #give driver 5 mins for a personal stop
        time.sleep(cfg.timescale * 300)
        #return to idle
        self.state = 'idle'


    #sends driver to nearest petrol station
    def refuel(self):
        #update state
        self.state = 'refuelling'
        #placeholder 'closest' petrol station
        closest = ('loco', 99999999)
        #for each petrol station in the list of station locations
        for station in mapfunctions.petrolstations:
            #find driving distance and store as tuple with station location
            distance = (station, mapfunctions.getDrivingDuration(station, self.location))
            #if the time to drive to the station is less than the current closest 
            if distance[1] < closest[1] :
                #closest becomes the current station, stored alongside its driving duration
                closest = distance
        #driveto the station
        self.driveto(closest[0], closest[1])
        #give the driver 200 seconds to refuel
        time.sleep(200*cfg.timescale)
        #restore fuel
        self.fuel = 1000
        #return to idle
        self.idle

    #for when driver needs to take a break
    def rest(self):
        #set state accordingly
        self.state = 'on break'
        #variable for length of break in seconds
        length = 300
        #initialise timer
        timer = 0
        #while the timer is less than length of break
        while timer < length:
            #increment timer
            timer += 1
            #wait 1 second
            time.sleep(cfg.timescale)
        #remove fatigue
        self.fatigue = 0
        #return to idle
        self.idle

    def driveto(self, destination, duration):
        timer = 0
        #work out how much the driver moves in lat & lng each second to reach the order
        # in the time it would take to drive there
        latgain = (destination[0] - self.location[0])/duration
        lnggain = (destination[1] - self.location[1])/duration
        #while timer is less than time it takes to drive to order
        while timer < duration:
            #increment the driver's latitude and longitude by the necessary values
            self.location = [self.location[0] + latgain, self.location[1] + lnggain]
            #increase the driver's fatigue
            self.fatigue += 1
            #decrease the driver's fuel
            self.fuel -= 1
            #increment timer
            timer += 1
            #update driver list, needed for when the map is rendered to get correct driver location
            allDrivers[self.id] = self
            #wait one second
            time.sleep(cfg.timescale)

    #to be run for each driver by their own thread
    def stateCheck(self):
        #while loop for use while driver is working
        running = True
        while running == True:
            #if the driver is idle
            if (self.state == 'idle'):
                #run idle checklist, this will be done every second until they become not idle
                self.idle()
            #wait 1 second
            time.sleep(cfg.timescale)

    #start a thread
    def startThread(self):
        #create thread with target statecheck
        dthread = threading.Thread(target = self.stateCheck)
        #start the thread
        dthread.start()

    def requestBreak(self):
        self.fatigue = 20000