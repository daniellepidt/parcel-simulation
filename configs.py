from classes import LockerVariation

config1 = [
  LockerVariation(1, [2, 3, 4]),
  LockerVariation(2, [1, 4]),
  LockerVariation(3, [1, 4, 5]),
  LockerVariation(4, [1, 2, 3, 5, 6]),
  LockerVariation(5, [3, 4, 6], 1),
  LockerVariation(6, [4, 5], 2),
]

config2 = [
  LockerVariation(1, [2, 3, 4]),
  LockerVariation(2, [1, 4]),
  LockerVariation(3, [1, 4, 5]),
  LockerVariation(4, [1, 2, 3, 5, 6], 1),
  LockerVariation(5, [3, 4, 6]),
  LockerVariation(6, [4, 5]),
]

config3 = [
  LockerVariation(1, [2, 3, 4]),
  LockerVariation(2, [1, 4], 1),
  LockerVariation(3, [1, 4, 5], 2),
  LockerVariation(4, [1, 2, 3, 5, 6]),
  LockerVariation(5, [3, 4, 6], 1),
  LockerVariation(6, [4, 5]),
]