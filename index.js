import Vue from 'vue'
import Vuex from 'vuex'
import { loops, simTime, policy } from "../simulation/Globals.js";

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    simulationRunning: false,
    simulationDone: false,
    loops: loops,
    simTime: simTime,
    policy: policy,
    expectedPackageReturns: 0,
    expectedMalfunctionsRevisits: 0,
    datasetArrivalByArea: [],
    datasetPackagesBySize: [],

  },
  getters: {
  },
  mutations: {

  },
  actions: {
  },
  modules: {
  }
})
