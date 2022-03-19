import { Event } from './Classes.js';

export function checkIfLockerFaults(
  quarter,
  p,
  costReturn,
  l,
  currTime,
  P,
  creatingPickup
) {
  if (p.locker.fault) {
    costReturn[l] += 1
    creatingPickup(p, P)
  } else {
    const x = Math.random()
    if (x < 0.01) {
      p.locker.fault = true
      costReturn[l] += 1
      new Event(
        quarter,
        currTime + (Math.random() * (1/24 - 5/24) + 5/24),
        3,
        p,
        P
      )
    } else {
      if (p.lockersize == 0) {
        p.locker.smallAvailable += 1
      } else if (p.lockersize == 1) {
        p.locker.mediumAvailable += 1
      } else {
        p.locker.largeAvailable += 1
      }
    }
  }
}

export function poisson(mean) {
  var L = Math.exp(-mean);
  var p = 1.0;
  var k = 0;

  do {
      k++;
      p *= Math.random();
  } while (p > L);

  return k - 1;
}