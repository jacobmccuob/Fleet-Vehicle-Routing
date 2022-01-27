import main
import driver
import time
import order
import orderhandler
import cfg
import datetime

def test1():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        assert employee.state == 'idle'

def test2():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.fuel = 100
        assert employee.state == 'refuelling'

def test3():
    driver.initialiseDrivers
    testOrder = order.Order([52.059171, -2.726275], datetime.datetime.now().strftime("%H:%M:%S"))
    for employee in driver.allDrivers.values():
        employee.setAssignedOrder(testOrder)
        assert employee.state == 'delivering'

def test4():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.fatigue = 11000
        assert employee.state == 'on break'

def test5():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.state = 'idle'
        employee.requestBreak()
        assert employee.state == 'on break'

def test6():
    driver.initialiseDrivers
    testOrder = order.Order([52.059171, -2.726275], datetime.datetime.now().strftime("%H:%M:%S"))
    for employee in driver.allDrivers.values():
        employee.setAssignedOrder(testOrder)
        employee.setAssignedOrder('Another order')
        assert employee.state == 'delivering'

def test7():
    driver.initialiseDrivers
    testOrder = order.Order([52.059171, -2.726275], datetime.datetime.now().strftime("%H:%M:%S"))
    for employee in driver.allDrivers.values():
        employee.setAssignedOrder(testOrder)
        employee.fuel = 100
        assert employee.state == 'delivering'

def test8():
    driver.initialiseDrivers
    testOrder = order.Order([52.059171, -2.726275], datetime.datetime.now().strftime("%H:%M:%S"))
    for employee in driver.allDrivers.values():
        employee.setAssignedOrder(testOrder)
        employee.fatigue = 11000
        assert employee.state == 'delivering'

def test9():
    driver.initialiseDrivers
    testOrder = order.Order([52.059171, -2.726275], datetime.datetime.now().strftime("%H:%M:%S"))
    for employee in driver.allDrivers.values():
        employee.setAssignedOrder(testOrder)
        employee.requestBreak()
        assert employee.state == 'delivering'

def test10():
    driver.initialiseDrivers
    testOrder = order.Order(cfg.hub_location, datetime.datetime.now().strftime("%H:%M:%S"))
    for employee in driver.allDrivers.values():
        employee.setAssignedOrder(testOrder)
        time.sleep(5)
        assert employee.state == 'idle'

def test11():
    driver.initialiseDrivers
    testOrder = order.Order(cfg.hub_location, datetime.datetime.now().strftime("%H:%M:%S"))
    for employee in driver.allDrivers.values():
        employee.state = 'refuelling'
        employee.fuel = 100
        employee.setAssignedOrder(testOrder)
        assert employee.state == 'refuelling'

def test12():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.state = 'refuelling'
        employee.fuel = 100
        assert employee.state == 'refuelling'

def test13():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.state = 'refuelling'
        employee.fatigue = 11000
        assert employee.state == 'on break'

def test14():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.state = 'refuelling'
        employee.requestBreak()
        assert employee.state == 'on break'

def test15():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.state = 'refuelling'
        employee.fuel = 100
        time.sleep(3000)
        assert employee.state == 'idle'

def test16():
    testOrder = order.Order(cfg.hub_location, datetime.datetime.now().strftime("%H:%M:%S"))
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.fatigue = 11000
        employee.state = 'on break'
        employee.setAssignedOrder(testOrder)
        assert employee.state == 'on break'

def test17():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.fatigue = 11000
        employee.state = 'on break'
        employee.fuel = 100
        assert employee.state == 'on break'

def test18():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.state = 'on break'
        employee.fatigue = 11000
        assert employee.state == 'on break'

def test19():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.state = 'on break'
        employee.fatigue = 11000
        employee.requestBreak()
        assert employee.state == 'on break'

def testcov1():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.stateCheck.running = False
        assert employee.stateCheck.running == False

def testcov2():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.state = 'idle'
        assert employee.stateCheck.running == True

def testcov3():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.state = 'idle'
        employee.fatigue = 11000
        assert employee.state == 'on break'

def testcov4():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.state = 'idle'
        employee.fatigue = 500
        employee.fuel = 100
        assert employee.state == 'refuelling'

def testcov5():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.state = 'idle'
        employee.fatigue = 500
        employee.fuel = 10000
        employee.assignedOrder = 'not none'
        assert employee.state == 'delivering'

def testcov6():
    driver.initialiseDrivers
    for employee in driver.allDrivers.values():
        employee.state = 'idle'
        employee.fatigue = 500
        employee.fuel = 100
        employee.assignedOrder = 'none'
        assert employee.stateCheck.running == True

def testscenario():
    driver.initialiseDrivers
    testOrder = order.Order([52.058267, -2.715694], datetime.datetime.now().strftime("%H:%M:%S"))
    secondTestOrder = order.Order([52.057047, -2.711596], datetime.datetime.now().strftime("%H:%M:%S"))
    order.outstandingOrders.append(testOrder)
    order.outstandingOrders.append(secondTestOrder)
    for employee in driver.allDrivers.values():
        employee.setAssignedOrder(testOrder)
        time.sleep(2)
        employee.setAssignedOrder(secondTestOrder)
        time.sleep(600)
        assert(testOrder not in order.outstandingOrders)
        assert(secondTestOrder.assignedDriver == employee.name)
