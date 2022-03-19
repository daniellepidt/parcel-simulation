# Imports
import numpy as np
import pandas as pd
import heapq
from classes import Event, Package
from globals import SIM_TIME, PACKAGE_INDEX, AVERAGE_NO_PACKAGES
from plots import output_results
import copy


def coming_back(p, curr_day):
    if (curr_day + 4) % 7 == 0:
        p.return_day = curr_day + 5
    else:
        p.return_day = curr_day + 4

# Function that creates the event of pickup, for not duplicating the code in several places.


def creating_pickup(p, P, curr_day, curr_time, pack_return, l, back_queues):
    # Sampling time of arrival in the day and the day itself.
    t = np.random.uniform(0, 0.75)
    # Setting back the counters
    p.count_days_in_center = 0
    if not p.trying_pickup:  # Means that the customer didn't tried to pickup the package
        p.trying_pickup = True
        # Sampling the probability of being in each day
        x = np.random.random(1)
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
                coming_back(p, curr_day)
    else:  # Means that the customer did tried to pickup the package
        if curr_time - int(curr_time) < (6/24):
            Event((curr_day+(6/24)) + t, 0, p, P)
        else:
            Event((curr_day+(6/24)) + (1 + t), 0, p, P)

def update_tic_avg(l, tic_avg, curr_day, queues):
    for i in range(3):
        if l in tic_avg[i].keys():
            if curr_day in tic_avg[i][l].keys():
                tic_avg[i][l][curr_day] += len(queues[i])
            else:
                tic_avg[i][l][curr_day] = len(queues[i])
        else:
            tic_avg[i][l][curr_day] = len(queues[i])


# The Simulation
def run_custom_policy_simulation(loops, lockers):
    # new_lockers = lockers
    # Measures
    # Time (days) until placement - measure no.1
    tpa_lst = [{j: [0 for z in range(0, loops)] for j in range(
        0, SIM_TIME + 1)} for i in range(6)]

    # Time in center - measure no.2
    tic_avg = [{j: {j: 0 for j in range(1, SIM_TIME+1)} for j in range(0, loops)},
               {j: {j: 0 for j in range(1, SIM_TIME+1)}
                for j in range(0, loops)},
               {j: {j: 0 for j in range(1, SIM_TIME+1)} for j in range(0, loops)}]

    # Expectation of number of packages which returned to the logistics center - measure no. 3: not relevant here
    pack_return = [0 for j in range(0, loops)]

    # Expectation of number of customers that needed to return the day after - measure no. 4
    customer_return = [0 for j in range(0, loops)]

    # List of sums of number of days each package was left at the logistics center throughout each quarter.
    sum_of_package_days_every_quarter = []

    for l in range(loops):
        if l % 5 == 0 and loops >= 5:
            # Indication for current status
            print(f'Starting quarter {l}/{loops}...')
        # Initialization of the simulation
        # Set the Random-Seed according to the iteration's number
        np.random.seed(l)
        package_index = PACKAGE_INDEX
        LOCKERS = copy.deepcopy(lockers) # Create a deepcopy of the lockers to prevent a reference.
        queues = [[] for i in range(3)]  # Queue of placing packages in lockers
        # Queue of placing packages in lockers which came back to the logistics center
        back_queues = [[] for i in range(3)]
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
        # while we have events and we didn't exceeded the SIM_TIME
        while (curr_time < SIM_TIME + 1) and P:
            # Event of arriving
            if event.event_type == 1:
                # for each area
                for i in range(1, 7):
                    # for each size
                    for j in range(0, 3):
                        # Sampling how many packages came in this size on this day
                        X = np.random.poisson(AVERAGE_NO_PACKAGES[i][j])
                        for z in range(0, X):
                            new_package = Package(
                                package_index, i, j, curr_time)
                            package_index += 1
                            # Now we will categorise the packages to the relevant queue
                            queues[j].append(new_package)

                # For measure #2
                if (curr_day) % 7 == 0:
                    update_tic_avg(l, tic_avg, curr_day, queues)

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
                            # The package was placed successfully
                            back_queues[2].remove(p1)
                            # Update numbers days until placement - for measure #1
                            tpa_lst[X][p1.count_days_in_center][l] += 1
                            # Creating event of pick up
                            creating_pickup(
                                p1, P, curr_day, curr_time, pack_return, l, back_queues)
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
                        # Does the collection area have any available large lockers?
                        elif LOCKERS[X].large_available > 0:
                            # Placing the package in the locker
                            LOCKERS[X].large_available -= 1
                            p1.lockersize = 2
                        else:  # Can't place the package, will remain in the logistics center
                            # Updating the counters
                            p1.count_days_in_center += 1  # Placing the package in the locker
                            continue  # Continue to the next package
                        # Placing the package in the locker
                        p1.locker = LOCKERS[X]
                        # The package was placed successfully
                        back_queues[1].remove(p1)
                        # Update numbers days until placement - for measure #1
                        tpa_lst[X][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1, P, curr_day, curr_time,
                                        pack_return, l, back_queues)

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
                        # Popping the destination area for placing the package there, - 1 for right index
                        X = p1.dest - 1
                        # Does the collection area have any available small lockers?
                        if LOCKERS[X].small_available > 0:
                            # Placing the package in the locker
                            LOCKERS[X].small_available -= 1
                            p1.lockersize = 0
                        # Does the collection area have any available medium lockers?
                        elif LOCKERS[X].medium_available > 0:
                            # Placing the package in the locker
                            LOCKERS[X].medium_available -= 1
                            p1.lockersize = 1
                        # Does the collection area have any available large lockers?
                        elif LOCKERS[X].large_available > 0:
                            # Placing the package in the locker
                            LOCKERS[X].large_available -= 1
                            p1.lockersize = 2
                        else:  # Can't place the package, will remain in the logistics center
                            # Updating the counters
                            p1.count_days_in_center += 1  # Placing the package in the locker
                            continue  # Continue to the next package
                        # Placing the package in the locker
                        p1.locker = LOCKERS[X]
                        # The package was placed successfully
                        back_queues[0].remove(p1)
                        # Update numbers days until placement - for measure #1
                        tpa_lst[X][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1, P, curr_day, curr_time,
                                        pack_return, l, back_queues)

                # For measure #2
                update_tic_avg(l, tic_avg, curr_day, back_queues)

                # Creating event of replacement again
                # if we are on Friday, the next replacement will be in two days, on Sunday.
                if (curr_day + 1) % 7 == 0:
                    Event(curr_time + 2, 4, P=P)
                else:  # else, the next replacement will be tomorrow.
                    Event(curr_time + 1, 4, P=P)

            # Event of placing the package in locker
            elif event.event_type == 2:
                # for each large package in the queue
                for p1 in queues[2][:]:
                    X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                    # Does the collection area have any available large lockers?
                    if LOCKERS[X].large_available > 0:
                        # Placing the package in the locker
                        LOCKERS[X].large_available -= 1
                        p1.lockersize = 2
                        p1.locker = LOCKERS[X]
                        # The package was placed successfully
                        queues[2].remove(p1)
                        # Update numbers days until placement - for measure #1
                        tpa_lst[X][p1.count_days_in_center][l] += 1
                        # Creating event of pick up
                        creating_pickup(p1, P, curr_day, curr_time,
                                        pack_return, l, back_queues)

                # for each medium package in the queue
                for p1 in queues[1][:]:
                    X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                    # Does the collection area have any available medium lockers?
                    if LOCKERS[X].medium_available > 0:
                        # Placing the package in the locker
                        LOCKERS[X].medium_available -= 1
                        p1.lockersize = 1
                    # Does the collection area have any available large lockers?
                    elif LOCKERS[X].large_available > 0:
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
                    creating_pickup(p1, P, curr_day, curr_time,
                                    pack_return, l, back_queues)

                # for each small package in the queue
                for p1 in queues[0][:]:
                    # Popping the destination area for placing the package there, - 1 for right index
                    X = p1.dest - 1
                    # Does the collection area have any available small lockers?
                    if LOCKERS[X].small_available > 0:
                        # Placing the package in the locker
                        LOCKERS[X].small_available -= 1
                        p1.lockersize = 0
                    # Does the collection area have any available medium lockers?
                    elif LOCKERS[X].medium_available > 0:
                        # Placing the package in the locker
                        LOCKERS[X].medium_available -= 1
                        p1.lockersize = 1
                    # Does the collection area have any available large lockers?
                    elif LOCKERS[X].large_available > 0:
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
                    creating_pickup(p1, P, curr_day, curr_time,
                                    pack_return, l, back_queues)

                # Now we will try to place the remain packages in the neighbor areas

                # for each large package in the queue
                for p1 in queues[2][:]:
                    X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                    for n in LOCKERS[X].neighbors:  # For each neighbor area
                        # Does the collection area have any available large lockers?
                        if LOCKERS[n-1].large_available > 0:
                            # Placing the package in the locker
                            LOCKERS[n-1].large_available -= 1
                            p1.lockersize = 2
                            p1.locker = LOCKERS[n-1]
                            # The package was placed successfully
                            queues[2].remove(p1)
                            # Update numbers days until placement - for measure #1
                            tpa_lst[n-1][p1.count_days_in_center][l] += 1
                            # Creating event of pick up
                            creating_pickup(
                                p1, P, curr_day, curr_time, pack_return, l, back_queues)
                            break  # Don't check other neighbors if it was placed
                        else:  # Can't place the package, will remain in the logistics center
                            continue  # Continue to the next neighbor
                    if not p1.locker:  # Can't place the package, will remain in the logistics center
                        p1.count_days_in_center += 1

                # for each medium package in the queue
                for p1 in queues[1][:]:
                    X = p1.dest - 1  # Popping the destination area for placing the package there, minus 1 for right index
                    for n in LOCKERS[X].neighbors:  # For each neighbor area
                        # Does the collection area have any available medium lockers?
                        if LOCKERS[n-1].medium_available > 0:
                            # Placing the package in the locker
                            LOCKERS[n-1].medium_available -= 1
                            p1.lockersize = 1
                            p1.locker = LOCKERS[n-1]
                            # The package was placed successfully
                            queues[1].remove(p1)
                            # Update numbers days until placement - for measure #1
                            tpa_lst[n-1][p1.count_days_in_center][l] += 1
                            # Creating event of pick up
                            creating_pickup(
                                p1, P, curr_day, curr_time, pack_return, l, back_queues)
                            break  # Don't check other neighbors if it was placed
                        elif LOCKERS[n-1].large_available > 0:
                            # Placing the package in the locker
                            LOCKERS[n-1].large_available -= 1
                            p1.lockersize = 2
                            p1.locker = LOCKERS[n-1]
                            # The package was placed successfully
                            queues[1].remove(p1)
                            # Update numbers days until placement - for measure #1
                            tpa_lst[n-1][p1.count_days_in_center][l] += 1
                            # Creating event of pick up
                            creating_pickup(
                                p1, P, curr_day, curr_time, pack_return, l, back_queues)
                            break  # Don't check other neighbors if it was placed
                        else:  # Can't place the package, will remain in the logistics center
                            continue  # Continue to the next neighbor
                    if not p1.locker:  # Can't place the package, will remain in the logistics center
                        p1.count_days_in_center += 1

                # for each small package in the queue
                for p1 in queues[0][:]:
                    # Popping the destination area for placing the package there, - 1 for right index
                    X = p1.dest - 1
                    for n in LOCKERS[X].neighbors:  # For each neighbor area
                        # Does the collection area have any available small lockers?
                        if LOCKERS[n-1].small_available > 0:
                            # Placing the package in the locker
                            LOCKERS[n-1].small_available -= 1
                            p1.lockersize = 0
                            p1.locker = LOCKERS[n-1]
                            # The package was placed successfully
                            queues[0].remove(p1)
                            # Update numbers days until placement - for measure #1
                            tpa_lst[n-1][p1.count_days_in_center][l] += 1
                            # Creating event of pick up
                            creating_pickup(
                                p1, P, curr_day, curr_time, pack_return, l, back_queues)
                            break  # Don't check other neighbors if it was placed
                        elif LOCKERS[n-1].medium_available > 0:
                            # Placing the package in the locker
                            LOCKERS[n-1].medium_available -= 1
                            p1.lockersize = 1
                            p1.locker = LOCKERS[n - 1]
                            # The package was placed successfully
                            queues[0].remove(p1)
                            # Update numbers days until placement - for measure #1
                            tpa_lst[n-1][p1.count_days_in_center][l] += 1
                            # Creating event of pick up
                            creating_pickup(
                                p1, P, curr_day, curr_time, pack_return, l, back_queues)
                            break  # Don't check other neighbors if it was placed
                        elif LOCKERS[n-1].large_available > 0:
                            # Placing the package in the locker
                            LOCKERS[n-1].large_available -= 1
                            p1.lockersize = 2
                            p1.locker = LOCKERS[n-1]
                            # The package was placed successfully
                            queues[0].remove(p1)
                            # Update numbers days until placement - for measure #1
                            tpa_lst[n-1][p1.count_days_in_center][l] += 1
                            # Creating event of pick up
                            creating_pickup(
                                p1, P, curr_day, curr_time, pack_return, l, back_queues)
                            break  # Don't check other neighbors if it was placed
                        else:  # Can't place the package, will remain in the logistics center
                            continue  # Continue to the next neighbor
                    if not p1.locker:  # Can't place the package, will remain in the logistics center
                        p1.count_days_in_center += 1

                # For measure #2
                update_tic_avg(l, tic_avg, curr_day, queues)

                # Creating event of placement again
                # If we are on Friday, the next placement will be in two days, on Sunday.
                if (curr_day + 1) % 7 == 0:
                    Event(curr_time + 2, 2, P=P)
                else:  # else, the next placement will be tomorrow.
                    Event(curr_time + 1, 2, P=P)

            # Event of pick-up the package:
            elif event.event_type == 0:
                if p.locker.fault:  # If there is a fault in the locker already
                    # For measure #4
                    customer_return[l] += 1
                    # Creating pickup in the next day
                    creating_pickup(p, P, curr_day, curr_time,
                                    pack_return, l, back_queues)
                else:  # If everything is normal
                    # Sampling the probability of creating a fault
                    x = np.random.random(1)
                    if x < 0.01:  # If there is a fault
                        p.locker.fault = True
                        # For measure #4
                        customer_return[l] += 1
                        # Creating event of fixing
                        Event(curr_time +
                              np.random.uniform((1 / 24), (5 / 24)), 3, p, P)
                    else:  # If everything is normal
                        # Picked up the package successfully
                        if p.lockersize == 0:
                            p.locker.small_available += 1
                        elif p.lockersize == 1:
                            p.locker.medium_available += 1
                        else:
                            p.locker.large_available += 1

            # Event of fixing the fault
            elif event.event_type == 3:
                p.locker.fault = False  # Fixed the locker successfully
                # Creating the pickup of the package again
                creating_pickup(p, P, curr_day, curr_time,
                                pack_return, l, back_queues)

            # Update simulation clock, and 'pop' the next event
            prev_time = curr_time
            event = heapq.heappop(P)
            curr_time = event.time
            curr_day = int(curr_time)
            p = event.package
        # Output information from each quarter of the simulation
        # in order to use it to calculate which is the best configuration.
        tic_for_loop = [tic_avg[0][l], tic_avg[1][l], tic_avg[2][l]]
        tic_for_loop_df = pd.DataFrame(tic_for_loop)
        tic_df_sum = tic_for_loop_df.to_numpy().sum()
        # Add quarterly sum to the list.
        sum_of_package_days_every_quarter.append(tic_df_sum)
    results = output_results(tpa_lst, tic_avg, customer_return, pack_return)
    results['sum_of_package_days'] = sum_of_package_days_every_quarter
    return results
