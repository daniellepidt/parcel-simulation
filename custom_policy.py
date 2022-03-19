# Imports
import numpy as np
import heapq
from classes import *
from functions import * # Import all common functions
from globals import * # Import all global parameters
from measures import * # Import all measures
from plots import output_results_plots

def coming_back(p):
    if (curr_day + 4) % 7 == 0:
        p.return_day = curr_day + 5
    else:
        p.return_day = curr_day + 4

# Function that creates the event of pickup, for not duplicating the code in several places.
def creating_pickup(p, P):
    t = np.random.uniform(0, 0.75)  # Sampling time of arrival in the day and the day itself.
    # Setting back the counters
    p.count_days_in_center = 0
    if not p.trying_pickup:  # Means that the customer didn't tried to pickup the package
        p.trying_pickup = True
        x = np.random.random(1)  # Sampling the probability of being in each day
        # There are different probabilities if the package was placed in destination or not.
        if p.dest == p.locker.id:  # If the package was placed in destination area
            if x < 0.4:
                Event((curr_day+(6/24)) + t, 0, p, P)
            elif 0.4 <= x < 0.6:
                Event((curr_day+(6/24)) + (1 + t), 0, p, P)
            elif 0.6 <= x < 0.9:
                Event((curr_day+(6/24)) + (2 + t), 0, p, P)
            else:
                Event((curr_day+(6/24)) + (3 + t), 0, p, P)
        else:  # If the package was placed in neighbor area
            if x < 0.2:
                Event((curr_day+(6/24)) + t, 0, p, P)
            elif 0.2 <= x < 0.4:
                Event((curr_day+(6/24)) + (1 + t), 0, p, P)
            elif 0.4 <= x < 0.7:
                Event((curr_day+(6/24)) + (2 + t), 0, p, P)
            elif 0.7 <= x < 0.9:
                Event((curr_day+(6/24)) + (3 + t), 0, p, P)
            else:
                # The client didn't show up above 4 days, and the package was returned to the logistical center
                p.trying_pickup = False
                pack_return[l] += 1  # For measure #3
                back_queues[p.size].append(p)
                coming_back(p)
    else:  # Means that the customer did tried to pickup the package
        if curr_time - int(curr_time) < (6/24):
            Event((curr_day+(6/24)) + t, 0, p, P)
        else:
            Event((curr_day+(6/24)) + (1 + t), 0, p, P)


# The Simulation
for l in range(LOOPS):
    # Initialization of the simulation
    LOCKERS = init_lockers()
    queues = [[] for i in range(3)]  # Queue of placing packages in lockers
    back_queues = [[] for i in range(3)] # Queue of placing packages in lockers which came back to the logistics center
    P = []  # Events heap

    # Creating the first arrival of packages
    Event(1 + (5 / 24), 1, P=P)
    # Creating the first replacement of packages
    Event(1 + ((5.25) / 24), 4, P=P)
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
                        queues[j].append(new_package)
            
            # For measure #2
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
            Event(curr_time + 1, 1, P=P)

        # Event of replacing the package in locker
        elif event.event_type == 4:
            # for each large package in the queue
            for p1 in back_queues[2][:]:
                if p1.return_day == curr_day:
                    if p1.lockersize == 0:
                        p1.locker.small_available += 1
                    elif p1.lockersize == 1:
                        p1.locker.medium_available += 1
                    else:
                        p1.locker.large_available += 1
                elif p1.return_day < curr_day:
                    X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                    if LOCKERS[X].large_available > 0:
                        LOCKERS[X].large_available -= 1
                        p1.lockersize = 2
                        p1.locker = LOCKERS[X]
                        back_queues[2].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure #1
                        tpa_lst[X][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1, P)
                    else:  # Can't place the package, will remain in the logistics center
                        p1.count_days_in_center += 1
                        continue  # Continue to the next package

            # for each medium package in the queue
            for p1 in back_queues[1][:]:
                if p1.return_day == curr_day:
                    if p1.lockersize == 0:
                        p1.locker.small_available += 1
                    elif p1.lockersize == 1:
                        p1.locker.medium_available += 1
                    else:
                        p1.locker.large_available += 1
                elif p1.return_day < curr_day:
                    X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                    if LOCKERS[X].medium_available > 0:
                        # Placing the package in the locker
                        LOCKERS[X].medium_available -= 1
                        p1.lockersize = 1
                    elif LOCKERS[X].large_available > 0:  # Does the collection area have any available large lockers?
                        # Placing the package in the locker
                        LOCKERS[X].large_available -= 1
                        p1.lockersize = 2
                    else:  # Can't place the package, will remain in the logistics center
                        # Updating the counters
                        p1.count_days_in_center += 1  # Placing the package in the locker
                        continue  # Continue to the next package
                    p1.locker = LOCKERS[X]  # Placing the package in the locker
                    back_queues[1].remove(p1)  # The package was placed successfully
                    # Update numbers days until placement - for measure #1
                    tpa_lst[X][p1.count_days_in_center][l] += 1
                    # Creating event of pick up
                    creating_pickup(p1, P)

            # for each small package in the queue
            for p1 in back_queues[0][:]:
                if p1.return_day == curr_day:
                    if p1.lockersize == 0:
                        p1.locker.small_available += 1
                    elif p1.lockersize == 1:
                        p1.locker.medium_available += 1
                    else:
                        p1.locker.large_available += 1
                elif p1.return_day < curr_day:
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
                        # Updating the counters
                        p1.count_days_in_center += 1  # Placing the package in the locker
                        continue  # Continue to the next package
                    p1.locker = LOCKERS[X]  # Placing the package in the locker
                    back_queues[0].remove(p1)  # The package was placed successfully
                    # Update numbers days until placement - for measure #1
                    tpa_lst[X][p1.count_days_in_center][l] += 1
                    # Creating event of pick up
                    creating_pickup(p1, P)

            # For measure #2
            for i in range(3):
                if l in tic_avg[i].keys():
                    if curr_day in tic_avg[i][l].keys():
                        tic_avg[i][l][curr_day] += len(back_queues[i])
                    else:
                        tic_avg[i][l][curr_day] = len(back_queues[i])
                else:
                    tic_avg[i][l][curr_day] = len(back_queues[i])


            # Creating event of replacement again
            if (curr_day + 1) % 7 == 0:  # if we are on Friday, the next replacement will be in two days, on Sunday.
                Event(curr_time + 2, 4, P=P)
            else:  # else, the next replacement will be tomorrow.
                Event(curr_time + 1, 4, P=P)

        # Event of placing the package in locker
        elif event.event_type == 2:
            # for each large package in the queue
            for p1 in queues[2][:]:
                X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                if LOCKERS[X].large_available > 0:  # Does the collection area have any available large lockers?
                    # Placing the package in the locker
                    LOCKERS[X].large_available -= 1
                    p1.lockersize = 2
                    p1.locker = LOCKERS[X]
                    queues[2].remove(p1)  # The package was placed successfully
                    # Update numbers days until placement - for measure #1
                    tpa_lst[X][p1.count_days_in_center][l] += 1
                    # Creating event of pick up
                    creating_pickup(p1, P)

            # for each medium package in the queue
            for p1 in queues[1][:]:
                X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                if LOCKERS[X].medium_available > 0: # Does the collection area have any available medium lockers?
                    # Placing the package in the locker
                    LOCKERS[X].medium_available -= 1
                    p1.lockersize = 1
                elif LOCKERS[X].large_available > 0:  # Does the collection area have any available large lockers?
                    # Placing the package in the locker
                    LOCKERS[X].large_available -= 1
                    p1.lockersize = 2
                else:  # Can't place, so continue to the next package without the next commends
                    continue
                p1.locker = LOCKERS[X]  # Placing the package in the locker
                queues[1].remove(p1)  # The package was placed successfully
                # Update numbers days until placement - for measure #1
                tpa_lst[X][p1.count_days_in_center][l] += 1
                # Creating event of pick up
                creating_pickup(p1, P)

            # for each small package in the queue
            for p1 in queues[0][:]:
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
                    continue  # Continue to the next package
                p1.locker = LOCKERS[X]  # Placing the package in the locker
                queues[0].remove(p1)  # The package was placed successfully
                # Update numbers days until placement - for measure #1
                tpa_lst[X][p1.count_days_in_center][l] += 1
                # Creating event of pick up
                creating_pickup(p1, P)

            # Now we will try to place the remain packages in the neighbor areas

            # for each large package in the queue
            for p1 in queues[2][:]:
                X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                for n in LOCKERS[X].neighbors:  # For each neighbor area
                    if LOCKERS[n-1].large_available > 0:  # Does the collection area have any available large lockers?
                        # Placing the package in the locker
                        LOCKERS[n-1].large_available -= 1
                        p1.lockersize = 2
                        p1.locker = LOCKERS[n-1]
                        queues[2].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure #1
                        tpa_lst[n-1][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1, P)
                        break  # Don't check other neighbors if it was placed
                    else:  # Can't place the package, will remain in the logistics center
                        continue  # Continue to the next neighbor
                if not p1.locker:  # Can't place the package, will remain in the logistics center
                    p1.count_days_in_center += 1

            # for each medium package in the queue
            for p1 in queues[1][:]:
                X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                for n in LOCKERS[X].neighbors:  # For each neighbor area
                    if LOCKERS[n-1].medium_available > 0:  # Does the collection area have any available medium lockers?
                        # Placing the package in the locker
                        LOCKERS[n-1].medium_available -= 1
                        p1.lockersize = 1
                        p1.locker = LOCKERS[n-1]
                        queues[1].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure #1
                        tpa_lst[n-1][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1, P)
                        break  # Don't check other neighbors if it was placed
                    elif LOCKERS[n-1].large_available > 0:
                        # Placing the package in the locker
                        LOCKERS[n-1].large_available -= 1
                        p1.lockersize = 2
                        p1.locker = LOCKERS[n-1]
                        queues[1].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure #1
                        tpa_lst[n-1][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1, P)
                        break  # Don't check other neighbors if it was placed
                    else:  # Can't place the package, will remain in the logistics center
                        continue  # Continue to the next neighbor
                if not p1.locker:  # Can't place the package, will remain in the logistics center
                    p1.count_days_in_center += 1

            # for each small package in the queue
            for p1 in queues[0][:]:
                X = p1.dest - 1  # Popping the destination area for placing the package there, - 1 for right index
                for n in LOCKERS[X].neighbors:# For each neighbor area
                    if LOCKERS[n-1].small_available > 0:  # Does the collection area have any available small lockers?
                        # Placing the package in the locker
                        LOCKERS[n-1].small_available -= 1
                        p1.lockersize = 0
                        p1.locker = LOCKERS[n-1]
                        queues[0].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure #1
                        tpa_lst[n-1][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1, P)
                        break  # Don't check other neighbors if it was placed
                    elif LOCKERS[n-1].medium_available > 0:
                        # Placing the package in the locker
                        LOCKERS[n-1].medium_available -= 1
                        p1.lockersize = 1
                        p1.locker = LOCKERS[n - 1]
                        queues[0].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure #1
                        tpa_lst[n-1][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1, P)
                        break  # Don't check other neighbors if it was placed
                    elif LOCKERS[n-1].large_available > 0:
                        # Placing the package in the locker
                        LOCKERS[n-1].large_available -= 1
                        p1.lockersize = 2
                        p1.locker = LOCKERS[n-1]
                        queues[0].remove(p1)  # The package was placed successfully
                        # Update numbers days until placement - for measure #1
                        tpa_lst[n-1][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1, P)
                        break  # Don't check other neighbors if it was placed
                    else:  # Can't place the package, will remain in the logistics center
                        continue  # Continue to the next neighbor
                if not p1.locker:  # Can't place the package, will remain in the logistics center
                    p1.count_days_in_center += 1

            # For measure #2
            for i in range(3):
                if l in tic_avg[i].keys():
                    if curr_day in tic_avg[i][l].keys():
                        tic_avg[i][l][curr_day] += len(queues[i])
                    else:
                        tic_avg[i][l][curr_day] = len(queues[i])
                else:
                    tic_avg[i][l][curr_day] = len(queues[i])


            # Creating event of placement again
            if (curr_day + 1) % 7 == 0:  # If we are on Friday, the next placement will be in two days, on Sunday.
                Event(curr_time + 2, 2, P=P)
            else:  # else, the next placement will be tomorrow.
                Event(curr_time + 1, 2, P=P)

        # Event of pick-up the package:
        elif event.event_type == 0 :
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

output_results_plots(tpa_lst, tic_avg, customer_return, pack_return)