<template>
  <v-form
    ref="form"
    v-model="valid"
  >
    <v-row justify="center" align="center">
      <v-col cols="12" sm="10" md="8" lg="6" align="center">
        <v-card elevation="2">
          <v-card-title>Run New Simulation</v-card-title>
            <v-card-text>
              <v-slider
                v-model="loops"
                class="my-7"
                label="Loops"
                color="secondary"
                hint="# of quarters to run"
                persistent-hint
                max="100"
                min="1"
                append-icon="mdi-sync"
                thumb-label="always"
              ></v-slider>
              <v-slider
                v-model="simTime"
                class="my-7"
                label="Simulation Time"
                color="secondary"
                hint="# of days in quarter"
                persistent-hint
                max="100"
                min="1"
                append-icon="mdi-clock"
                thumb-label="always"
              ></v-slider>
              <v-select
                v-model="policy"
                :items="items"
                item-text="type"
                item-value="id"
                label="Policy"
                append-icon="mdi-code-tags"
              ></v-select>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
             <v-btn
                :disabled="!valid"
                color="secondary"
                depressed
                @click="runSimulation"
              >
                <v-icon left>mdi-run</v-icon>
                Run Simulation
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                depressed
                @click="reset"
              >
                <v-icon>mdi-refresh</v-icon>
              </v-btn>
            </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-form>
</template>

<script>
import { loops, simTime, policy } from "../simulation/Globals.js";
  
export default {
  name: 'Run',
  data: () => ({
    valid: true,
    loops: loops,
    simTime: simTime,
    policy: policy,
    items: [
      { type: 'Basic', id: 0 },
      { type: 'Custom', id: 1 },
    ],
  }),
  methods: {
    runSimulation() {

    },
    reset () {
      this.simTime = 91;
      this.loops = 50;
      this.policy = 0;
    },
  },
}
</script>
