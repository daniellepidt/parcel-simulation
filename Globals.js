import { Locker } from './Classes.js'

export const averageNumberPackages = {
  1: [7, 3, 1],
  2: [8, 2, 1.5],
  3: [12, 4, 2],
  4: [5, 1, 3],
  5: [8, 3, 1],
  6: [3, 1, 1.5]
}

export const loops = 50;
export const simTime = 91
export const policy = 0

const LOCKER1 = new Locker(1, [2,3,4])
const LOCKER2 = new Locker(2, [1,4])
const LOCKER3 = new Locker(3, [1,4,5])
const LOCKER4 = new Locker(4, [1,2,3,5,6])
const LOCKER5 = new Locker(5, [3,4,6])
const LOCKER6 = new Locker(6, [4,5])
export const LOCKERS = [LOCKER1, LOCKER2, LOCKER3, LOCKER4, LOCKER5, LOCKER6]