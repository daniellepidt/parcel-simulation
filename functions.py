import numpy as np
from classes import *

# Global Functions
def init_lockers():
  # Setting all the lockers with their neighbors
  LOCKER1 = Locker(1, [2, 3, 4])
  LOCKER2 = Locker(2, [1, 4])
  LOCKER3 = Locker(3, [1, 4, 5])
  LOCKER4 = Locker(4, [1, 2, 3, 5, 6])
  LOCKER5 = Locker(5, [3, 4, 6])
  LOCKER6 = Locker(6, [4, 5])
  return [LOCKER1, LOCKER2, LOCKER3, LOCKER4, LOCKER5, LOCKER6]  # Setting the list of them

def check_if_locker_faults(p, customer_return, l, curr_time, P, creating_pickup):
  if p.locker.fault:  # If there is a fault in the locker already
      # For measure #4
      customer_return[l] += 1
      # Creating pickup in the next day
      creating_pickup(p, P)
  else:  # If everything is normal
    x = np.random.random(1)  # Sampling the probability of creating a fault
    if x < 0.01:  # If there is a fault
      p.locker.fault = True
      # For measure #4
      customer_return[l] += 1
      # Creating event of fixing
      Event(curr_time + np.random.uniform((1 / 24), (5 / 24)), 3, p, P)
    else:  # If everything is normal
      # Picked up the package successfully
      if p.lockersize == 0:
          p.locker.small_available += 1
      elif p.lockersize == 1:
          p.locker.medium_available += 1
      else:
          p.locker.large_available += 1