<template>
  <div>
    <v-row justify="center" class="mb-3">
      <v-col cols="11" sm="6" md="3">
        <v-card elevation="3">
          <v-card-title class="font-weight-bold">Simulation Settings</v-card-title>
          <v-simple-table>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">
                    Loops
                  </th>
                  <th class="text-left">
                    Simulation Time
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{{ currentLoop }} / {{ loops }}</td>
                  <td>{{ parseInt(currDay) }} / {{ simTime }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
          <v-divider></v-divider>
          <v-card-subtitle>Progress</v-card-subtitle>
          <v-progress-linear
            :value="simulationProgress"
            height="25"
            color="secondary"
            class="mb-4"
            striped
            readonly
          >
            <strong>{{ Math.floor(simulationProgress) }}%</strong>
          </v-progress-linear>
          <v-divider></v-divider>
          <v-card-subtitle>Logs</v-card-subtitle>
          <v-virtual-scroll
            :bench="benched"
            :items="simEvents"
            height="350"
            item-height="64"
          >
            <template v-slot:default="{ item }">
              <v-list-item :key="item">
                <v-list-item-action>
                  <v-btn
                    fab
                    small
                    depressed
                    :color="item.color"
                  >
                    <v-icon>{{ item.icon }}</v-icon>
                  </v-btn>
                </v-list-item-action>

                <v-list-item-content>
                  <v-list-item-subtitle>
                    {{ item.datetime }}
                  </v-list-item-subtitle>
                  <v-list-item-title>
                    {{ item.title }}
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>

              <v-divider></v-divider>
            </template>
          </v-virtual-scroll>
        </v-card>
      </v-col>
      <v-col cols="11" sm="6" md="8">
        <v-row justify="center">
          <v-col cols="12">
            <v-card elevation="3">
              <v-simple-table>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="text-left font-weight-black">
                        Current Status
                      </th>
                      <th class="text-left">
                        Small
                      </th>
                      <th class="text-left">
                        Medium
                      </th>
                      <th class="text-left">
                        Large
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td class="font-weight-bold">Packages Waiting Placement</td>
                      <td>
                        <v-icon v-for="s in queueSmall" :key="s" small>
                          mdi-package
                        </v-icon>
                      </td>
                      <td>
                        <v-icon v-for="s in queueMedium" :key="s">
                          mdi-package
                        </v-icon>
                      </td>
                      <td>
                        <v-icon v-for="s in queueLarge" :key="s" large>
                          mdi-package
                        </v-icon>
                      </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-card>
          </v-col>
          <v-col v-for="l of lockersData" :key="l.id" cols="12" md="6" lg="4">
            <v-card elevation="3">
              <v-card-title>
                Locker #{{l.id}}
                <v-chip
                  v-if="l.fault"
                  class="ma-2"
                  color="error"
                  dark
                  label
                  small
                >
                  <v-icon left small>
                    mdi-lock-outline
                  </v-icon>
                  Fault
                </v-chip>
              </v-card-title>
              <v-card-subtitle>
                Neighbors:
                <v-chip v-for="n of l.neighbors" :key="n" color="secondary" label x-small>{{n}}</v-chip>
              </v-card-subtitle>
              <v-simple-table>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="text-left">
                        Size
                      </th>
                      <th class="text-left">
                        Packages Present
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Small</td>
                      <td>
                        <v-icon v-for="s in l.smallTaken" :key="s" small>
                          mdi-package
                        </v-icon>
                      </td>
                    </tr>
                    <tr>
                      <td>Medium</td>
                      <td>
                        <v-icon v-for="s in l.mediumTaken" :key="s">
                          mdi-package
                        </v-icon>
                      </td>
                    </tr>
                    <tr>
                      <td>Large</td>
                      <td>
                        <v-icon v-for="s in l.largeTaken" :key="s" large>
                          mdi-package
                        </v-icon>
                      </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-dialog
      v-model="dialog"
      persistent
      max-width="290"
    >
      <v-card>
        <v-card-title class="text-h5">
          Simulation Done!
        </v-card-title>
        <v-card-text>
          The simulation is done and the results are in!
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
          <v-btn
            color="secondary"
            depressed
            @click="dialog = false"
            :to="{ name: 'Results' }"
          >
            View Results
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex';
// import { mapGetters } from 'vuex';
// import heapq from 'heapq';
// import {Locker, Event, Package} from '../simulation/Classes.js';
// import {checkIfLockerFaults} from '../simulation/Functions.js'
// import {averageNumberPackages, LOCKERS} from '../simulation/Globals.js'
import {LOCKERS} from '../simulation/Globals.js'
// import {} from '../simulation/Measures'


export default {
  name: 'Simulation',
  data: () => ({
    lockersData: [],
    simEvents: [],
    benched: 0,
    dialog: false,
    events: [],
    currentLoop: 0,
    currDay: 0,
    queueSmall: 0,
    queueMedium: 0,
    queueLarge: 0,
    lockers: LOCKERS,
  }),
  computed: {
    ...mapState([
      'simulationDone',
      'loops',
      'simTime',
    ]),
    simulationProgress() {
      return this.currentLoop / this.loops * 100;
    }
  },
  methods: {

  },
  created() {
    this.lockersData = this.lockers;
  },
  watch: {
    lockers: function(val) {
      this.lockersData = val;
    },
    events: function(val) {
      this.simEvents = val;
    },
    simulationDone: function(val) {
      if (val) {
        this.dialog = val;
      }
    }
  }
}
</script>