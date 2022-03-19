import heapq from 'heapq';

function convertNumToTime(number) {
  // Check sign of given number
  var sign = (number >= 0) ? 1 : -1;

  // Set positive value of number of sign negative
  number = number * sign;

  // Separate the int from the decimal part
  var hour = Math.floor(number);
  var decpart = number - hour;

  var min = 1 / 60;
  // Round to nearest minute
  decpart = min * Math.round(decpart / min);

  var minute = Math.floor(decpart * 60) + '';

  // Add padding if need
  if (minute.length < 2) {
  minute = '0' + minute; 
  }

  // Add Sign in final result
  sign = sign == 1 ? '' : '-';

  // Concate hours and minutes
  const time = sign + hour + ':' + minute;

  return time;
}

export class Package {
  id = 0;
  dest = 0
  size = 0
  arrivalTime = 0
  locker = new Locker();
  lockersize = null;
  countDaysInCenter = 0
  tryingPickup = false
  returnDay = null;

  constructor(id, dest, size, arrivalTime, locker, lockersize, countDaysInCenter, tryingPickup, returnDay) {
    this.id = id;
    this.dest = dest;
    this.size = size;
    this.arrivalTime = arrivalTime;
    this.locker = locker
    this.lockersize = lockersize
    this.countDaysInCenter = countDaysInCenter
    this.tryingPickup = tryingPickup
    this.returnDay = returnDay;
  }
}

export const compareEvents = (event1, event2) => {
  return event1.time < event2.time;
}

export class Event {
  quarter = 0;
  time = 0;
  eventType = 0;
  pckg = new Package();
  P = []
  
  constructor(quarter, time, eventType, pckg, P) {
    this.quarter = quarter
    this.time = time;
    this.eventType = eventType;
    this.pckg = pckg;
    this.P = P;
    heapq.push(P, this, compareEvents);
  }

  get timeOfDay() {
    return convertNumToTime(this.time % 1 * 24);
  }

  get datetime() {
    return `Q${this.quarter}, Day ${ Math.floor(this.time)} ${this.timeOfDay}`
  }

  get title() {
    switch (this.eventType) {
      case 0:
        return `Package #${this.pckg.id} picked up @ Locker #${this.locker.id}`
      case 1:
        return `Package #${this.pckg.id} arrived @ Log. Center`
      case 2:
        return `Package #${this.pckg.id} placed @ Locker #${this.locker.id}`
      case 3:
        return `Locker #${this.locker.id} faulted while picking up Package #${this.pckg.id}`
      case 4:
        return `Replacing packages returned to Log. Center`
    }
    return '';
  }

  get icon() {
    switch (this.eventType) {
      case 0:
        return 'mdi-emoticon'
      case 1:
        return 'mdi-package'
      case 2:
        return 'mdi-cube-send'
      case 3:
        return 'mdi-lock'
      case 4:
        return 'mdi-keyboard-return'
    }
    return '';
  }
  
  get color() {
    switch (this.eventType) {
      case 0:
        return 'success'
      case 1:
        return 'info'
      case 2:
        return 'primary'
      case 3:
        return 'error'
      case 4:
        return 'secondary'
    }
    return '';
  }
}

export class Locker {
  id = -1;
  neighbors = [];
  smallAvailable = 15;
  mediumAvailable = 6;
  largeAvailable = 4;
  fault = false;

  constructor(id, neighbors) {
    this.id = id;
    this.neighbors = neighbors;
  }

  get smallTaken() {
    return 15 - this.smallAvailable;
  }
  get mediumTaken() {
    return 6 - this.mediumAvailable;
  }
  get largeTaken() {
    return 4 - this.largeAvailable;
  }
}