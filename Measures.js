import { loops, simTime } from './Globals.js';

const zeroes = new Array(loops).fill(0);
const zeroesArray = new Array(simTime + 1).fill(zeroes);

const tpaZeroesObject = {}
for (let i = 0; i < simTime + 1; i++) {
  tpaZeroesObject[i] = zeroesArray[i]
}

export const tpaList = new Array(6).fill(tpaZeroesObject);

const ticZeroesObject = {}
for (let i = 0; i < simTime + 1; i++) {
  ticZeroesObject[i] = 0
}
const ticObjectsObject = {}
for (let i = 0; i < simTime + 1; i++) {
  ticObjectsObject[i] = ticZeroesObject;
}

export const ticAverage = new Array(3).fill(ticObjectsObject)


export const packReturn = new Array(loops).fill(0)
export const costReturn = new Array(loops).fill(0)