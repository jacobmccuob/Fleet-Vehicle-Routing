import driver
import mapfunctions

#assigns driver to order based off human-centered parameters
def assignDriverToOrder(currentOrder):
    #initialises dictionary to hold driver objects as keys and their fitness for the current order as items
    driversAndFitnesses = {}
    #variable to hold the number of drivers which are not available to take the order
    unavailableDrivers = 0
    #for each driver
    for currentDriver in driver.allDrivers.values():
        #if they are in an idle state
        if currentDriver.state == 'idle':
            #initialise their fitness to 0
            fitness = 0
            #Fitness based on driver's distance from order
            orderduration = mapfunctions.getDrivingDuration(currentDriver.location,currentOrder.location)
            fitness -= orderduration/10

            #fitness based on destination's distance from driver request stops
            requestduration = mapfunctions.getDrivingDuration(mapfunctions.get_coords_of_address
            (currentDriver.desired_stops), currentOrder.location)
            fitness -= requestduration/50

            #fitness based on if driver needs to refuel
            #if the fuel is getting low
            if (currentDriver.fuel < 1500):
                #if there is a petrol station within 300 metres of the destination add 10 to fitness
                if (mapfunctions.exists_petrol_station_within(currentDriver.location, 300)):
                    fitness += 10

                #otherwise, if there is a petrol station within 500 metres of the destination add 5 to fitness
                elif (mapfunctions.exists_petrol_station_within(currentDriver.location, 500)):
                    fitness += 5

                #if there are no petrol stations within 500m of destination, no fitness is gained
                else:
                    fitness +=0

            #accounts for driver fatigue
            fitness -= currentDriver.fatigue/ 10
            driversAndFitnesses[currentDriver] = fitness
        else:
            #if driver isn't available, add to list of unavailable drivers
            unavailableDrivers += 1
    #if there is at least one available driver
    if unavailableDrivers < len(driver.allDrivers):
        #sort the dictionary by fitness
        driversAndFitnesses = sorted(driversAndFitnesses.items(), key = lambda x:x[1])
        #select the driver corresponding to the highest fitness value
        chosenDriver = (driversAndFitnesses[-1][0])
        currentOrder.setAssignedDriver(chosenDriver.name)
        #set chosen driver's assigned order to the current order
        chosenDriver.setAssignedOrder(currentOrder, orderduration)
    else:
        #state that there are no available drivers to take the order
        print('no available drivers')
        currentOrder.setAssignedDriver('none')