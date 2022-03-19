import heapq from 'heapq';
import {Locker, Event, Package, compareEvents} from './Classes.js'
import {poisson, checkIfLockerFaults} from './Functions'
import {LOCKERS, averageNumberPackages} from './Globals'
import {ticAverage, tpaList} from './Measures'
import store from '../store/index';

function creatingPickup(p, P) {
  const t = (Math.random() * (0 - 0.75) + 0.75)
  if (!p.tryingPickup) {
    p.tryingPickup = true;
    x = Math.random()
    if (x < 0.4) {
      new Event((currDay+(6/24)) + t, 0, p, P)
    } else if (0.4 <= x <= 0.6) {
      new Event((currDay+(6/24)) + (1 + t), 0, p, P)
    } else if (0.6 <= x <= 0.9) {
      new Event((currDay+(6/24)) + (2 + t), 0, p, P)
    } else {
      new Event((currDay+(6/24)) + (3 + t), 0, p, P)
    }
  } else {
    if ((currTime - parseInt(currTime)) < (6/24)) {
      new Event((currDay+(6/24)) + t, 0, p, P)
    } else {
      new Event((currDay+(6/24)) + (1 + t), 0, p, P)
    }
  }
}

export function runBasic(
  loops,
  simTime,
  events,
  currentLoop,
  currDay,
  queueSmall,
  queueMedium,
  queueLarge,
  lockers
) {
  ticAvg = ticAverage
  tpaLst = tpaList
  for (let l = 0; l < loops; l++) {
    let queues = new Array(3).fill(new Array(6).fill([]))
    let packageIndex = 0;
    P = []

    new Event(1 + (5/24), 1, P=P)
    new Event(1 + (5.5), 2, P=P)

    let event = heapq.pop(P, compareEvents);
    let currTime = event.time
    currDay = parseInt(currTime)
    let p = event.pckg

    while ((currTime < simTime + 1) && P.length) {
      if (event.eventType == 1) {
        for (let i = 1; i < 7; i++) {
          for (let j = 0; j < 3; j++) {
            const X = poisson(averageNumberPackages[i][j])
            for (z = 0; z < X; z++) {
              newPackage = new Package(packageIndex, i, j, currTime)
              packageIndex += 1
              queues[j][i-1].push(newPackage)
            }
          }
        }
        if (currDay % 7 == 0) {
          for (let i = 0; i < 6; i++) {
            for (let j = 0; j < 3; j++) {
              if ( Object.keys(ticAvg[j]).includes(l) ) {
                if (Object.keys(ticAvg[j][i]).includes(l)) {
                  ticAvg[j][l][currDay] += queues[j][i].length
                } else {
                  ticAvg[j][l][currDay] = queues[j][i].length
                }
              } else {
                ticAvg[j][l][currDay] = queues[j][i].length
              }
            }
          }
        } 
        new Event(currTime + 1, 1, P=P)
      } else if (event.eventType == 2) {
        for (let i = 0; i < 6; i++) {
          for (let p1 of queues[2][i][]) {}
        }
      }
    }

  }
}