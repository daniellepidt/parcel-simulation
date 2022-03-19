from globals import SIM_TIME, LOOPS

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
