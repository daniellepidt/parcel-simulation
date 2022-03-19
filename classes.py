import heapq

# Classes
class Event:
  def __init__(self, time, event_type, package=-1, P=[]):
    self.time = time  # event time
    self.event_type = event_type  # event type
    self.package = package  # a Package-type object
    self.P = P # Heap used for events
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
                trying_pickup=False, return_day=None):
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
    # Can be only if the package was placed in a neighbour area and wasn't picked up for 4 days.
    self.return_day = return_day

class LockerVariation():
  def __init__(self, id, neighbors, type=0, fault=False):
    self.id = id  # The id of which locker means the area number.
    self.neighbors = neighbors  # The neighbor areas of the locker's area
    types = [
      {'small': 15, 'medium': 6, 'large': 4}, # 1st Locker Variation
      {'small': 30, 'medium': 4, 'large': 2}, # 2nd Locker Variation
      {'small': 24, 'medium': 4, 'large': 3}, # 3rd Locker Variation
    ]
    self.small_available = types[type]['small'] # Counts how many small lockers are available
    self.medium_available = types[type]['medium']  # Counts how many medium lockers are available
    self.large_available = types[type]['large']  # Counts how many large lockers are available
    self.fault = fault  # True if there was fault one of the pickups, otherwise - false.
    # There is 1% chance that there will be a fault

  def __repr__(self):
    return f'Locker {self.id}, Availables: Sm-{self.small_available} Md-{self.medium_available} Lg-{self.large_available}'