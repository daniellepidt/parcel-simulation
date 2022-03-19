# Imports
import numpy as np
import heapq
from classes import *
from functions import * # Import all common functions
from globals import * # Import all global parameters
from measures import * # Import all measures
from plots import output_results_plots

# Function that creates the event of pickup, for not duplicating the code in several places.
def creating_pickup(p, P):
    t = np.random.uniform(0, 0.75)  # Sampling time of arrival in the day and the day itself.
    if not p.trying_pickup:  # Means that the customer didn't try to pickup the package
        p.trying_pickup = True
        x = np.random.random(1)  # Sampling the probability of being in each day
        if x < 0.4:
                Event((curr_day+(6/24)) + t, 0, p, P)
        elif 0.4 <= x < 0.6:
                Event((curr_day+(6/24)) + (1 + t), 0, p, P)
        elif 0.6 <= x < 0.9:
                Event((curr_day+(6/24)) + (2 + t), 0, p, P)
        else:
                Event((curr_day+(6/24)) + (3 + t), 0, p, P)
    else:  # Means that the customer tried to pickup the package
        if curr_time - int(curr_time) < (6/24):
            Event((curr_day+(6/24)) + t, 0, p, P)
        else:
            Event((curr_day+(6/24)) + (1 + t), 0, p, P)


# The Simulation
for l in range(LOOPS):
    # Initialization of the simulation
    LOCKERS = init_lockers()
    queues = [[[] for i in range (6)] for j in range(3)]  # Queue of placing packages in lockers
    P = []  # Events heap

    # Creating the first arrival of packages
    Event(1 + (5 / 24), 1, P=P)
    # Creating the first placement of packages
    Event(1 + (5.5) / 24, 2, P=P)

    # Update simulation clock, and 'pop' the next event
    event = heapq.heappop(P)
    curr_time = event.time
    curr_day = int(curr_time)
    p = event.package

    # Entering the simulation
    while (curr_time < SIM_TIME + 1) and P:  # while we have events and we didn't exceeded the SIM_TIME
        # Event of arriving
        if event.event_type == 1:
            # for each area
            for i in range(1, 7):
                # for each size
                for j in range(0, 3):
                    # Sampling how many packages came in this size on this day
                    X = np.random.poisson(AVERAGE_NO_PACKAGES[i][j])
                    for z in range(0, X):
                        new_package = Package(PACKAGE_INDEX, i, j, curr_time)
                        PACKAGE_INDEX += 1
                        # Now we will categorise the packages to the relevant queue
                        queues[j][i-1].append(new_package)
            
            # For measure #2
            if (curr_day) % 7 == 0:    
                for i in range(6):
                    for j in range(3):
                        if l in tic_avg[j].keys():
                            if curr_day in tic_avg[j][l].keys():
                                tic_avg[j][l][curr_day] += len(queues[j][i])
                            else:
                                tic_avg[j][l][curr_day] = len(queues[j][i])
                        else:
                            tic_avg[j][l][curr_day] = len(queues[j][i])

            # Each arriving event creates another arriving event
            Event(curr_time + 1, 1, P=P)

        # Event of placing the package in locker
        elif event.event_type == 2:
            # for each large package in the queue
            for i in range(6):
                for p1 in queues[2][i][:]:
                    X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                    if LOCKERS[X].large_available > 0:  # Does the collection area have any available large lockers?
                        # Placing the package in the locker
                        LOCKERS[X].large_available -= 1
                        p1.lockersize = 2
                        p1.locker = LOCKERS[X]
                        queues[2][i].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure #1
                        tpa_lst[X][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1, P)
                    else:  # Can't place the package, will remain in the logistics center
                        p1.count_days_in_center += 1
                        continue  # Continue to the next package

            # for each medium package in the queue
            for i in range(6):
                for p1 in queues[1][i][:]:
                    X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                    if LOCKERS[X].medium_available > 0:  # Does the collection area have any available medium lockers?
                        # Placing the package in the locker
                        LOCKERS[X].medium_available -= 1
                        p1.lockersize = 1
                    elif LOCKERS[X].large_available > 0:  # Does the collection area have any available large lockers?
                        # Placing the package in the locker
                        LOCKERS[X].large_available -= 1
                        p1.lockersize = 2
                    else:  # Can't place the package, will remain in the logistics center
                        p1.count_days_in_center += 1
                        continue  # Continue to the next package without the next commends
                    p1.locker = LOCKERS[X]  # Placing the package in the locker
                    queues[1][i].remove(p1)  # The package was placed successfully
                    # Update numbers days until placement - for measure #1
                    tpa_lst[X][p1.count_days_in_center][l] += 1
                    # Creating event of pick up
                    creating_pickup(p1, P)
                
            # for each small package in the queue
            for i in range(6):
                for p1 in queues[0][i][:]:
                    X = p1.dest - 1  # Popping the destination area for placing the package there, - 1 for right index
                    if LOCKERS[X].small_available > 0:  # Does the collection area have any available small lockers?
                        # Placing the package in the locker
                        LOCKERS[X].small_available -= 1
                        p1.lockersize = 0
                    elif LOCKERS[X].medium_available > 0:  # Does the collection area have any available medium lockers?
                        # Placing the package in the locker
                        LOCKERS[X].medium_available -= 1
                        p1.lockersize = 1
                    elif LOCKERS[X].large_available > 0:  # Does the collection area have any available large lockers?
                        # Placing the package in the locker
                        LOCKERS[X].large_available -= 1
                        p1.lockersize = 2
                    else:  # Can't place the package, will remain in the logistics center
                        p1.count_days_in_center += 1
                        continue  # Continue to the next package without the next commends
                    p1.locker = LOCKERS[X]  # Placing the package in the locker
                    queues[0][i].remove(p1)  # The package was placed successfully
                    # Update numbers days until placement - for measure #1
                    tpa_lst[X][p1.count_days_in_center][l] += 1
                    # Creating event of pick up
                    creating_pickup(p1, P)

            # For measure #2
            curr_day = int(curr_time)
            for i in range(6):
                for j in range(3):
                    if l in tic_avg[j].keys():
                        if curr_day in tic_avg[j][l].keys():
                            tic_avg[j][l][curr_day] += len(queues[j][i])
                        else:
                            tic_avg[j][l][curr_day] = len(queues[j][i])
                    else:
                        tic_avg[j][l][curr_day] = len(queues[j][i])

            # Creating event of placement again
            if (curr_day + 1) % 7 == 0:  # If we are on Friday, the next placement will be in two days, on Sunday.
                Event(curr_time + 2, 2, P=P)
            else:  # else, the next placement will be tomorrow.
                Event(curr_time + 1, 2, P=P)

        # Event of pick-up the package:
        elif event.event_type == 0:
            check_if_locker_faults(p, customer_return, l, curr_time, P, creating_pickup)

        # Event of fixing the fault
        elif event.event_type == 3:
            p.locker.fault = False  # Fixed the locker successfully
            creating_pickup(p, P)  # Creating the pickup of the package again

        # Update simulation clock, and 'pop' the next event
        prev_time = curr_time
        event = heapq.heappop(P)
        curr_time = event.time
        curr_day = int(curr_time)
        p = event.package

output_results_plots(tpa_lst, tic_avg, customer_return)