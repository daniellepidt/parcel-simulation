# Imports

import numpy as np
import heapq
import random
import statistics
from pylab import plot, show, bar
import matplotlib.pyplot as plt

plt.style.use("ggplot")


# Classes

class Event:
    def __init__(self, time, event_type, package=-1):
        self.time = time  # event time
        self.event_type = event_type  # event type
        self.package = package  # a Package-type object
        heapq.heappush(P, self)  # add the event to the events list

    def __lt__(self, event2):
        return self.time < event2.time

    event_types = {
        0: 'pickup',
        1: 'arriving',
        2: 'placement',
        3: 'fixing',
        4: 'replacement'
    }

class Package:
    def __init__(self, id, dest, size, arrival_time, locker=None, lockersize=None, count_days_in_center=0,
                 trying_pickup=False, back=False, back_in_center=0):
        self.id = id  # The ID of the package
        self.dest = dest  # The destination of the package
        self.size = size  # There are 3 possible sizes of the packages: 0 - small, 1 - medium, 2 - large
        self.arrival_time = arrival_time  # The arrival time of the packages
        self.locker = locker  # Where did the package eventually placed. Can be only in the destination area in this code
        self.lockersize = lockersize  # What was the size of the locker it was placed. 0- small, 1- medium, 2- large.
        # Small can be placed in large, medium and small locker, medium can be placed in medium and small locker and
        # large can be placed only in large locker
        self.count_days_in_center = count_days_in_center  # How many days was the package in the center till it was placed
        self.trying_pickup = trying_pickup  # True when the customer tries to pickup the package, otherwise - false
        #self.back = back  # True when the package comes back to the center, false otherwise.
        # Can be only if the package was placed in a neighbour area and wasn't picked up for 4 days.
        self.back_in_center = back_in_center


class Locker():
    def __init__(self, id, neighbors, small_available=15, medium_available=6, large_available=4, fault=False):
        self.id = id  # The id of which locker means the area number.
        self.neighbors = neighbors  # The neighbor areas of the locker's area
        self.small_available = small_available  # Counts how many small lockers are available
        self.medium_available = medium_available  # Counts how many medium lockers are available
        self.large_available = large_available  # Counts how many large lockers are available
        self.fault = fault  # True if there was fault one of the pickups, otherwise - false.
        # There is 1% chance that there will be a fault


# Function that creates the event of pickup, for not duplicating the code in several places.
def creating_pickup(p):
    t = np.random.uniform(0, 0.75)  # Sampling time of arrival in the day and the day itself.
    # Setting back the counters
    p.count_days_in_center = 0
    p.back_in_center = 0
    if not p.trying_pickup:  # Means that the customer didn't tried to pickup the package
        p.trying_pickup = True
        x = np.random.random(1)  # Sampling the probability of being in each day
        # There are different probabilities if the package was placed in destination or not.
        if p.dest == p.locker.id:  # If the package was placed in destination area
            if x < 0.4:
                Event((curr_day+(6/24)) + t, 0, p)
            elif 0.4 <= x < 0.6:
                Event((curr_day+(6/24)) + (1 + t), 0, p)
            elif 0.6 <= x < 0.9:
                Event((curr_day+(6/24)) + (2 + t), 0, p)
            else:
                Event((curr_day+(6/24)) + (3 + t), 0, p)
        else:  # If the package was placed in neighbor area
            if x < 0.2:
                Event((curr_day+(6/24)) + t, 0, p)
            elif 0.2 <= x < 0.4:
                Event((curr_day+(6/24)) + (1 + t), 0, p)
            elif 0.4 <= x < 0.7:
                Event((curr_day+(6/24)) + (2 + t), 0, p)
            elif 0.7 <= x < 0.9:
                Event((curr_day+(6/24)) + (3 + t), 0, p)
            else:
                #print ("Package", p.id, "will come back")
                # The client didn't show up above 4 days, and the package was returned to the logistical center
                #p.back = True
                p.trying_pickup = False
                pack_return[l] += 1  # For measure no. 3
                # print (pack_return)
                back_queues[p.size].append(p)
                """if p.size == 0:
                    back_queue_small.append(p)
                elif p.size == 1:
                    back_queue_medium.append(p)
                else:
                    back_queue_large.append(p)"""
    else:  # Means that the customer did tried to pickup the package
        if curr_time - int(curr_time) < (6/24):
            Event((curr_day+(6/24)) + t, 0, p)
        else:
            Event((curr_day+(6/24)) + (1 + t), 0, p)


# Parameters
SIM_TIME = 91  # 13 weeks * 7 days in week
PACKAGE_INDEX = 1  # Setting counter for package id
# Given data
LOOPS = 50
AVERAGE_NO_PACKAGES = {1: [7, 3, 1], 2: [8, 2, 1.5], 3: [12, 4, 2], 4: [5, 1, 3], 5: [8, 3, 1], 6: [3, 1, 1.5]}

# Measures
# Time (days) until placement - measure no.1
tpa_lst = [{j: [0 for z in range(0, LOOPS)] for j in range(0, SIM_TIME + 1)} for i in range(6)]

# Time in center - measure no.2
tic_avg = [{j: {j: 0 for j in range(1, SIM_TIME+1)} for j in range(0, LOOPS)},
           {j: {j: 0 for j in range(1, SIM_TIME+1)} for j in range(0, LOOPS)},
           {j: {j: 0 for j in range(1, SIM_TIME+1)} for j in range(0, LOOPS)}]

# Expectation of number of packages which returned to the logistics center - measure no. 3: not relevant here
pack_return = [0 for j in range(0, LOOPS)]

# Expectation of number of customers that needed to return the day after - measure no. 4
customer_return = [0 for j in range(0, LOOPS)]

# The Simulation
for l in range(LOOPS):
    # Initialization of the simulation
    # Setting all the lockers with their neighbors
    LOCKER1 = Locker(1, [2, 3, 4])
    LOCKER2 = Locker(2, [1, 4])
    LOCKER3 = Locker(3, [1, 4, 5])
    LOCKER4 = Locker(4, [1, 2, 3, 5, 6])
    LOCKER5 = Locker(5, [3, 4, 6])
    LOCKER6 = Locker(6, [4, 5])
    LOCKERS = [LOCKER1, LOCKER2, LOCKER3, LOCKER4, LOCKER5, LOCKER6]  # Setting the list of them
    queues = [[] for i in range(3)]  # Queue of placing packages in lockers
    #queue_small = []  # Queue of placing small packages in lockers
    #queue_medium = []  # Queue of placing medium packages in lockers
    #queue_large = []  # Queue of placing large packages in lockers
    back_queues = [[] for i in range(3)] # Queue of placing packages in lockers which came back to the logistics center
    #back_queue_small = []  # Queue of placing small packages which came back to the logistics center
    #back_queue_medium = []  # Queue of placing medium packages which came back to the logistics center
    #back_queue_large = []  # Queue of placing large packages which came back to the logistics center
    P = []  # Events heap

    # Creating the first arrival of packages
    Event(1 +(5 / 24), 1)
    # Creating the first replacement of packages
    Event(1 + ((5.25) / 24), 4)
    # Creating the first placement of packages
    Event(1 + (5.5) / 24, 2)

    # Update simulation clock, and 'pop' the next event
    event = heapq.heappop(P)
    curr_time = event.time
    curr_day = int(curr_time)
    p = event.package

    # Entering the simulation
    while (curr_time < SIM_TIME + 1) and P:  # while we have events and we didn't exceeded the SIM_TIME

        # Event of arriving
        if event.event_type == 1:
            #print("day: %d, time: %s" % (curr_day, curr_time), event.event_type)
            # for each area
            for i in range(1, 7):
                # for each size
                for j in range(0, 3):
                    # Sampling how many packages came in this size on this day
                    X = np.random.poisson(AVERAGE_NO_PACKAGES[i][j])
                    for z in range(0, X):
                        new_package = Package(PACKAGE_INDEX, i, j, curr_time)
                        # print("%s %s is arrving in area no. %s" % (new_package.size, new_package.id, new_package.dest))
                        PACKAGE_INDEX += 1
                        # Now we will categorise the packages to the relevant queue
                        queues[j].append(new_package)
                        """if j == 0:
                            queue_small.append(new_package)
                        elif j == 1:
                            queue_medium.append(new_package)
                        else:
                            queue_large.append(new_package)"""
            # print ("After Arrival")
            # print ("SMALL", len(queues[0]), "MEDIUM", len(queues[1]), "LARGE", len(queues[2]))
            
            # For measure no.2
            #curr_day = int(curr_time)
            if (curr_day) % 7 == 0:
                for i in range(3):
                    if l in tic_avg[i].keys():
                        if curr_day in tic_avg[i][l].keys():
                            tic_avg[i][l][curr_day] += len(queues[i])
                        else:
                            tic_avg[i][l][curr_day] = len(queues[i])
                    else:
                        tic_avg[i][l][curr_day] = len(queues[i])

            # Each arriving event creates another arriving event
            Event(curr_time + 1, 1)

        # Event of replacing the package in locker
        elif event.event_type == 4:
            #print("day: %d, time: %s" % (curr_day, curr_time), event.event_type)

            # for each large package in the queue
            for p1 in back_queues[2][:]:
                #print("Replacing large package no. ", p1.id, "the dest is", p1.dest, "Days in center", p1.count_days_in_center, "Back in center", p1.back_in_center)
                if p1.back_in_center == 4:
                    X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                    if LOCKERS[X].large_available > 0:
                        # print("Package no. %s was placed succesfully" % (p1.id), "after %s days" % (p1.count_days_in_center))
                        LOCKERS[X].large_available -= 1
                        p1.lockersize = 2
                        p1.locker = LOCKERS[X]
                        back_queues[2].remove(p1)  # The package was placed successfully
                        #back_queue_large.remove(p1)
                        # Update numbers days until placement - for measure no.1
                        tpa_lst[X][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1)
                    else:  # Can't place the package, will remain in the logistics center
                        #print("Failed placing package no. ", p1.id, "waits for %s days" % (p1.count_days_in_center))
                        p1.count_days_in_center += 1
                        # print ("Days in center", p1.count_days_in_center)
                        #p1.back_in_center += 1
                        # print ("Back in center", p1.back_in_center)
                        continue  # Continue to the next package
                else:  # Its not the time for replacement
                    # Updating the counters
                    p1.back_in_center += 1
                    #p1.count_days_in_center += 1
                    # print ("Its not the time for replacement")
                    # print ("Back in center", p1.back_in_center)
                    # print ("Days in center", p1.count_days_in_center)

            # for each medium package in the queue
            for p1 in back_queues[1][:]:
                # print("Replacing medium package no. ", p1.id, "the dest is", p1.dest, "Days in center", p1.count_days_in_center, "Back in center", p1.back_in_center)
                if p1.back_in_center == 4:  # Does the collection area have any available medium lockers?
                    X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                    if LOCKERS[X].medium_available > 0:
                        # print("Package no. %s was placed succesfully in medium locker" % (p1.id), "after %s days" % (p1.count_days_in_center))
                        # Placing the package in the locker
                        LOCKERS[X].medium_available -= 1
                        p1.lockersize = 1
                    elif LOCKERS[X].large_available > 0:  # Does the collection area have any available large lockers?
                        # print("Package no. %s was placed succesfully in large locker" % (p1.id), "after %s days" % (p1.count_days_in_center))
                        # Placing the package in the locker
                        LOCKERS[X].large_available -= 1
                        p1.lockersize = 2
                    else:  # Can't place the package, will remain in the logistics center
                        # print("Failed placing package no. ", p1.id, "waits for %s days" % (p1.count_days_in_center))
                        # Updating the counters
                        p1.count_days_in_center += 1  # Placing the package in the locker
                        #p1.back_in_center += 1
                        # print ("Back in center", p1.back_in_center)
                        # print ("Days in center", p1.count_days_in_center)
                        continue  # Continue to the next package
                    p1.locker = LOCKERS[X]  # Placing the package in the locker
                    back_queues[1].remove(p1)  # The package was placed successfully
                    # back_queue_medium.remove(p1)  # The package was placed successfully
                    # Update numbers days until placement - for measure no.1
                    tpa_lst[X][p1.count_days_in_center][l] += 1
                    # Creating event of pick up
                    creating_pickup(p1)
                else:  # Its not the time for replacement
                    # Updating the counters
                    p1.back_in_center += 1
                    # p1.count_days_in_center += 1
                    # print ("Its not the time for replacement")
                    # print ("Back in center", p1.back_in_center)
                    # print ("Days in center", p1.count_days_in_center)

            # for each small package in the queue
            for p1 in back_queues[0][:]:
                # print("Replacing small package no. ", p1.id, "the dest is", p1.dest, "Days in center", p1.count_days_in_center, "Back in center", p1.back_in_center)
                if p1.back_in_center == 4:
                    X = p1.dest - 1  # Popping the destination area for placing the package there, - 1 for right index
                    if LOCKERS[X].small_available > 0:  # Does the collection area have any available small lockers?
                        # print("Package no. %s was placed succesfully in small locker" % (p1.id), "after %s days" % (p1.count_days_in_center))
                        # Placing the package in the locker
                        LOCKERS[X].small_available -= 1
                        p1.lockersize = 0
                    elif LOCKERS[X].medium_available > 0:  # Does the collection area have any available medium lockers?
                        # print("Package no. %s was placed succesfully in medium locker" % (p1.id), "after %s days" % (p1.count_days_in_center))
                        # Placing the package in the locker
                        LOCKERS[X].medium_available -= 1
                        p1.lockersize = 1
                    elif LOCKERS[X].large_available > 0:  # Does the collection area have any available large lockers?
                        # print("Package no. %s was placed succesfully in large locker" % (p1.id), "after %s days" % (p1.count_days_in_center))
                        # Placing the package in the locker
                        LOCKERS[X].large_available -= 1
                        p1.lockersize = 2
                    else:  # Can't place the package, will remain in the logistics center
                        # print("Failed placing package no. ", p1.id, "waits for %s days" % (p1.count_days_in_center))
                        # Updating the counters
                        p1.count_days_in_center += 1  # Placing the package in the locker
                        #p1.back_in_center += 1
                        # print ("Back in center", p1.back_in_center)
                        # print ("Days in center", p1.count_days_in_center)
                        continue  # Continue to the next package
                    p1.locker = LOCKERS[X]  # Placing the package in the locker
                    back_queues[0].remove(p1)  # The package was placed successfully
                    # back_queue_small.remove(p1)  # The package was placed successfully
                    # Update numbers days until placement - for measure no.1
                    tpa_lst[X][p1.count_days_in_center][l] += 1
                    # Creating event of pick up
                    creating_pickup(p1)
                else:  # Its not the time for replacement
                    # Updating the counters
                    p1.back_in_center += 1
                    #p1.count_days_in_center += 1
                    # print ("Its not the time for replacement")
                    # print ("Back in center", p1.back_in_center)
                    # print ("Days in center", p1.count_days_in_center)

            # For measure no.2
            #curr_day = int(curr_time)
            for i in range(3):
                if l in tic_avg[i].keys():
                    if curr_day in tic_avg[i][l].keys():
                        tic_avg[i][l][curr_day] += len(back_queues[i])
                    else:
                        tic_avg[i][l][curr_day] = len(back_queues[i])
                else:
                    tic_avg[i][l][curr_day] = len(back_queues[i])

            # print ("After Replacement")
            # print ("SMALL_BACK", len(back_queues[0]), "MEDIUM_BACK", len(back_queues[1]), "LARGE_BACK", len(back_queues[2]))

            # Creating event of replacement again
            if (curr_day + 1) % 7 == 0:  # if we are on Friday, the next replacement will be in two days, on Sunday.
                Event(curr_time + 2, 4)
            else:  # else, the next replacement will be tomorrow.
                Event(curr_time + 1, 4)

        # Event of placing the package in locker
        elif event.event_type == 2:
            #print("day: %d, time: %s" % (curr_day, curr_time), event.event_type)

            # for each large package in the queue
            for p1 in queues[2][:]:
                # print("Placing large package no. ", p1.id, "the dest is", p1.dest, "Days in center", p1.count_days_in_center)
                X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                if LOCKERS[X].large_available > 0:  # Does the collection area have any available large lockers?
                    # print("Package no. %s was placed succesfully" % (p1.id), "after %s days" % (p1.count_days_in_center), "in area", LOCKERS[X - 1].id)
                    # Placing the package in the locker
                    LOCKERS[X].large_available -= 1
                    p1.lockersize = 2
                    p1.locker = LOCKERS[X]
                    queues[2].remove(p1)  # The package was placed successfully
                    # Update numbers days until placement - for measure no.1
                    tpa_lst[X][p1.count_days_in_center][l] += 1
                    # Creating event of pick up
                    creating_pickup(p1)

            # for each medium package in the queue
            for p1 in queues[1][:]:
                # print("Placing medium package no. ", p1.id, "the dest is", p1.dest, "Days in center", p1.count_days_in_center)
                X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                if LOCKERS[X].medium_available > 0: # Does the collection area have any available medium lockers?
                    # print("Package no. %s was placed succesfully in medium locker" % (p1.id), "after %s days" % (p1.count_days_in_center),  "in area", LOCKERS[X - 1].id)
                    # Placing the package in the locker
                    LOCKERS[X].medium_available -= 1
                    p1.lockersize = 1
                elif LOCKERS[X].large_available > 0:  # Does the collection area have any available large lockers?
                    # print("Package no. %s was placed succesfully in large locker" % (p1.id), "after %s days" % (p1.count_days_in_center),  "in area", LOCKERS[X - 1].id)
                    # Placing the package in the locker
                    LOCKERS[X].large_available -= 1
                    p1.lockersize = 2
                else:  # Can't place, so continue to the next package without the next commends
                    continue
                p1.locker = LOCKERS[X]  # Placing the package in the locker
                queues[1].remove(p1)  # The package was placed successfully
                # queue_medium.remove(p1)  # The package was placed successfully
                # Update numbers days until placement - for measure no.1
                tpa_lst[X][p1.count_days_in_center][l] += 1
                # Creating event of pick up
                creating_pickup(p1)

            # for each small package in the queue
            for p1 in queues[0][:]:
                # print("Placing small package no. ", p1.id, "the dest is", p1.dest, "Days in center", p1.count_days_in_center)
                X = p1.dest - 1  # Popping the destination area for placing the package there, - 1 for right index
                if LOCKERS[X].small_available > 0:  # Does the collection area have any available small lockers?
                    # print("Package no. %s was placed succesfully in small locker" % (p1.id), "after %s days" % (p1.count_days_in_center), "in area", LOCKERS[X - 1].id)
                    # Placing the package in the locker
                    LOCKERS[X].small_available -= 1
                    p1.lockersize = 0
                elif LOCKERS[X].medium_available > 0:  # Does the collection area have any available medium lockers?
                    # print("Package no. %s was placed succesfully in medium locker" % (p1.id), "after %s days" % (p1.count_days_in_center), "in area", LOCKERS[X - 1].id)
                    # Placing the package in the locker
                    LOCKERS[X].medium_available -= 1
                    p1.lockersize = 1
                elif LOCKERS[X].large_available > 0:  # Does the collection area have any available large lockers?
                    # print("Package no. %s was placed succesfully in large locker" % (p1.id), "after %s days" % (p1.count_days_in_center), "in area", LOCKERS[X - 1].id)
                    # Placing the package in the locker
                    LOCKERS[X].large_available -= 1
                    p1.lockersize = 2
                else:  # Can't place the package, will remain in the logistics center
                    # print("Failed placing package no. ", p1.id, "wait for %s days" % (p1.count_days_in_center))
                    continue  # Continue to the next package
                p1.locker = LOCKERS[X]  # Placing the package in the locker
                queues[0].remove(p1)  # The package was placed successfully
                # queue_small.remove(p1)  # The package was placed successfully
                # Update numbers days until placement - for measure no.1
                tpa_lst[X][p1.count_days_in_center][l] += 1
                # Creating event of pick up
                creating_pickup(p1)

            # Now we will try to place the remain packages in the neighbor areas

            # for each large package in the queue
            for p1 in queues[2][:]:
                # print("Placing again large package no. ", p1.id, "the dest is", p1.dest, "Days in center", p1.count_days_in_center)
                X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                for n in LOCKERS[X].neighbors:  # For each neighbor area
                    # print ("looking for in neighbor", n)
                    if LOCKERS[n-1].large_available > 0:  # Does the collection area have any available large lockers?
                        # print("Package no. %s was placed succesfully" % (p1.id), "after %s days" % (p1.count_days_in_center), "in area", LOCKERS[n - 1].id)
                        # Placing the package in the locker
                        LOCKERS[n-1].large_available -= 1
                        p1.lockersize = 2
                        p1.locker = LOCKERS[n-1]
                        queues[2].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure no.1
                        tpa_lst[n-1][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1)
                        break  # Don't check other neighbors if it was placed
                    else:  # Can't place the package, will remain in the logistics center
                        # print("Failed placing package no. ", p1.id, "waits for %s days" % (p1.count_days_in_center))
                        continue  # Continue to the next neighbor
                if not p1.locker:  # Can't place the package, will remain in the logistics center
                    # print("Failed placing package no. ", p1.id, "waits for %s days" % (p1.count_days_in_center))
                    p1.count_days_in_center += 1
                    # print ("Days in center", p1.count_days_in_center)

            # for each medium package in the queue
            for p1 in queues[1][:]:
                # print("Placing again medium package no. ", p1.id, "the dest is", p1.dest, "Days in center", p1.count_days_in_center)
                X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                # print ("Neighbors",LOCKERS[X - 1].neighbors)
                for n in LOCKERS[X].neighbors:  # For each neighbor area
                    # print ("looking for in neighbor", n)
                    if LOCKERS[n-1].medium_available > 0:  # Does the collection area have any available medium lockers?
                        # print("Package no. %s was placed succesfully in medium locker" % (p1.id), "after %s days" % (p1.count_days_in_center), "in area", LOCKERS[n - 1].id)
                        # Placing the package in the locker
                        LOCKERS[n-1].medium_available -= 1
                        p1.lockersize = 1
                        p1.locker = LOCKERS[n-1]
                        queues[1].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure no.1
                        tpa_lst[n-1][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1)
                        break  # Don't check other neighbors if it was placed
                    elif LOCKERS[n-1].large_available > 0:
                        # print("Package no. %s was placed succesfully in large locker" % (p1.id), "after %s days" % (p1.count_days_in_center), "in area", LOCKERS[n - 1].id)
                        # Placing the package in the locker
                        LOCKERS[n-1].large_available -= 1
                        p1.lockersize = 2
                        p1.locker = LOCKERS[n-1]
                        queues[1].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure no.1
                        tpa_lst[n-1][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1)
                        break  # Don't check other neighbors if it was placed
                    else:  # Can't place the package, will remain in the logistics center
                        # print("Failed placing package no. ", p1.id, "waits for %s days" % (p1.count_days_in_center))
                        continue  # Continue to the next neighbor
                if not p1.locker:  # Can't place the package, will remain in the logistics center
                    # print("Failed placing package no. ", p1.id, "waits for %s days" % (p1.count_days_in_center))
                    p1.count_days_in_center += 1
                    # print ("Days in center", p1.count_days_in_center)

            # for each small package in the queue
            for p1 in queues[0][:]:
                # print("Placing again small package no. ", p1.id, "the dest is", p1.dest, "Days in center", p1.count_days_in_center)
                X = p1.dest - 1  # Popping the destination area for placing the package there, - 1 for right index
                # print ("Neighbors",LOCKERS[X - 1].neighbors)
                for n in LOCKERS[X].neighbors:# For each neighbor area
                    # print ("looking for in neighbor", n)
                    if LOCKERS[n-1].small_available > 0:  # Does the collection area have any available small lockers?
                        # print("Package no. %s was placed succesfully in small locker" % (p1.id), "after %s days" % (p1.count_days_in_center), "in area", LOCKERS[n - 1].id)
                        # Placing the package in the locker
                        LOCKERS[n-1].small_available -= 1
                        p1.lockersize = 0
                        p1.locker = LOCKERS[n-1]
                        queues[0].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure no.1
                        tpa_lst[n-1][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1)
                        break  # Don't check other neighbors if it was placed
                    elif LOCKERS[n-1].medium_available > 0:
                        # print("Package no. %s was placed succesfully in medium locker" % (p1.id), "after %s days" % (p1.count_days_in_center), "in area", LOCKERS[n - 1].id)
                        # Placing the package in the locker
                        LOCKERS[n-1].medium_available -= 1
                        p1.lockersize = 1
                        p1.locker = LOCKERS[n - 1]
                        queues[0].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure no.1
                        tpa_lst[n-1][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1)
                        break  # Don't check other neighbors if it was placed
                    elif LOCKERS[n-1].large_available > 0:
                        # print("Package no. %s was placed succesfully in large locker" % (p1.id), "after %s days" % (p1.count_days_in_center), "in area", LOCKERS[n - 1].id)
                        # Placing the package in the locker
                        LOCKERS[n-1].large_available -= 1
                        p1.lockersize = 2
                        p1.locker = LOCKERS[n-1]
                        queues[0].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure no.1
                        tpa_lst[n-1][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1)
                        break  # Don't check other neighbors if it was placed
                    else:  # Can't place the package, will remain in the logistics center
                        # print("Failed placing package no. ", p1.id, "wait for %s days" % (p1.count_days_in_center))
                        continue  # Continue to the next neighbor
                if not p1.locker:  # Can't place the package, will remain in the logistics center
                    # print("Failed placing package no. ", p1.id, "waits for %s days" % (p1.count_days_in_center))
                    p1.count_days_in_center += 1
                    # print ("Days in center", p1.count_days_in_center)

            # For measure no.2
            #curr_day = int(curr_time)
            for i in range(3):
                if l in tic_avg[i].keys():
                    if curr_day in tic_avg[i][l].keys():
                        tic_avg[i][l][curr_day] += len(queues[i])
                    else:
                        tic_avg[i][l][curr_day] = len(queues[i])
                else:
                    tic_avg[i][l][curr_day] = len(queues[i])


            # print ("After Placement")
            # print ("SMALL", len(queues[0]), "MEDIUM", len(queues[1]), "LARGE", len(queues[2]))

            # Creating event of placement again
            if (curr_day + 1) % 7 == 0:  # If we are on Friday, the next placement will be in two days, on Sunday.
                Event(curr_time + 2, 2)
            else:  # else, the next placement will be tomorrow.
                Event(curr_time + 1, 2)

        # Event of pick-up the package:
        elif event.event_type == 0 :
            #print("day: %d, time: %s" % (curr_day, curr_time), event.event_type)
            if p.locker.fault:  # If there is a fault in the locker already
                # print("There is a fault, the client will pick up the package tomorrow")
                # For measure no. 4
                customer_return[l] += 1
                creating_pickup(p)
            else:  # If everything is normal
                x = np.random.random(1)  # Sampling the probability of creating a fault
                if x < 0.01:  # If there is a fault
                    p.locker.fault = True
                    # For measure no. 4
                    customer_return[l] += 1
                    # Creating event of fixing
                    Event(curr_time + np.random.uniform((1 / 24), (5 / 24)), 3, p)
                else:  # If everything is normal
                    # print("Client is picking up %s successfully in %f" % (p.id, curr_time))
                    # Picked up the package successfully
                    if p.lockersize == 0:
                        p.locker.small_available += 1
                    elif p.lockersize == 1:
                        p.locker.medium_available += 1
                    else:
                        p.locker.large_available += 1

        # Event of fixing the fault
        elif event.event_type == 3:
            #print("day: %d, time: %s" % (curr_day, curr_time), event.event_type)
            p.locker.fault = False  # Fixed the locker successfully
            creating_pickup(p)  # Creating the pickup of the package again

        # Update simulation clock, and 'pop' the next event
        prev_time = curr_time
        event = heapq.heappop(P)
        curr_time = event.time
        curr_day = int(curr_time)
        p = event.package

# For analysis
# Measure no.1
# Calculate the average
for i in range(6):
    for j in range(0, SIM_TIME + 1):
        tpa_lst[i][j] = statistics.mean(tpa_lst[i][j])
# print (tpa_lst)

# Visualization of the average
for i in range(6):
    plt.bar(range(len(tpa_lst[i])), tpa_lst[i].values(), align='center')
    plt.xticks(range(len(tpa_lst[i])), tpa_lst[i].keys())
    plt.xlabel('Number of days')
    plt.ylabel('Number of packages')
    plt.title('Distribution of the time (days) from the arrival until the placement - area %s' % (i + 1))
    plt.show()

# Measure no. 2
tic_temp = [{} for i in range(3)]  # Calculating the no. of packages and which day there was this amount
for z in range(3): # For each size
    for l in tic_avg[z]:  # For each loop
        for key in tic_avg[z][l]:  #
            if tic_avg[z][l][key] in tic_temp[z].keys():
                if l in tic_temp[z][tic_avg[z][l][key]].keys():
                    tic_temp[z][tic_avg[z][l][key]][l] += 1
                else:
                    tic_temp[z][tic_avg[z][l][key]][l] = 1
            else:
                tic_temp[z][tic_avg[z][l][key]] = {}
                tic_temp[z][tic_avg[z][l][key]][l] = 1
for z in range(3): # Calculating the mean for all the loops
    for p in tic_temp[z]:
        tic_temp[z][p] = statistics.mean(tic_temp[z][p].values())

tic_unite = [{} for z in range(3)]  # Uniting in groups of 10
for z in range(3):  # For each size
    for p in tic_temp[z]:  # For each no. of packages
        if p % 10 > 0 and int(p/10) in tic_unite[z].keys():
            tic_unite[z][int(p/10)] += tic_temp[z][p]
        else:
            tic_unite[z][int(p/10)] = tic_temp[z][p]

# Visualization of the average
for z in range(3):
    plt.bar(range(len(tic_unite[z])), tic_unite[z].values(), align='center')
    plt.xticks(range(len(tic_unite[z])), tic_unite[z].keys())
    plt.xlabel('Number of packages')
    plt.ylabel('Number of days')
    if z == 0:
        plt.title("Distribution of a number of small packages stored in the logistics center")
    elif z == 1:
        plt.title("Distribution of a number of medium packages stored in the logistics center")
    else:
        plt.title("Distribution of a number of large packages stored in the logistics center")
    plt.show()

# Measure no.3
pack_return_av = statistics.mean(pack_return)
print("measure no.3 - pack_return_av", pack_return_av)

# Measure no.4
customer_return_av_new = statistics.mean(customer_return)
print("measure no.4 -customer_return_av_new", customer_return_av_new)
