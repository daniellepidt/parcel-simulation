<template>
  <v-row justify="center" class="mb-3">
    <v-col cols="11" align="center">
      <div class="font-weight-bold text-h5 mt-2">
        Simulation Results
      </div>
    </v-col>
    <v-col cols="11" sm="11" md="6">
      <v-card elevation="3">
      <v-card-title class="font-weight-bold">
        Days Between Arrival to Placement by Area
      </v-card-title>
      <v-card-text>
        <BarChart
          :labels="labels"
          :data="datasetArea"
          :scales="scalesByArea"
        />
      </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="11" sm="11" md="6">
      <v-card elevation="3">
      <v-card-title class="font-weight-bold">
        Packages in the Logistics Center by Size
      </v-card-title>
      <v-card-text>
        <BarChart
          :labels="labels"
          :data="dataset"
          :scales="scalesBySize"
        />
      </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="11" sm="3" align="center">
      <v-card elevation="3" class="mb-3">
        <v-simple-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th v-if="policy == 1" class="text-left">
                  Expected Package Returns
                </th>
                <th class="text-left">
                  Expected Malfunction Revisits
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td v-if="policy == 1">{{ expectedPackageReturns }}</td>
                <td>{{ expectedMalfunctionsRevisits }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import BarChart from "../components/BarChart";
import { mapState } from 'vuex';

export default {
  name: 'Results',
  components: { BarChart },
  computed: {
    ...mapState([
      'policy',
      'expectedPackageReturns',
      'expectedMalfunctionsRevisits',
      'datasetArrivalByArea',
      'datasetPackagesBySize',
    ])
  },
  data: () => ({
      scalesByArea: {
        x: 'Days',
        y: 'Packages',
      },
      scalesBySize: {
        x: 'Packages',
        y: 'Days',
      },
      labels: ['a', 'b', 'c'],
      datasetArea: [
        {
          label: "Area 1",
          backgroundColor: "#F9AA33",
          data: [40, 20, 12]
        },
        {
          label: "Area 2",
          backgroundColor: "#232F34",
          data: [65, 12, 14]
        },
        {
          label: "Area 3",
          backgroundColor: "#FFCF44",
          data: [65, 12, 14]
        },
        {
          label: "Area 4",
          backgroundColor: "#1EB980",
          data: [65, 12, 14]
        },
        {
          label: "Area 5",
          backgroundColor: "#72DEFF",
          data: [65, 12, 14]
        },
        {
          label: "Area 6",
          backgroundColor: "#045D56",
          data: [65, 12, 14]
        },
      ],
      dataset: [
        {
          label: "Small",
          backgroundColor: "#F9AA33",
          data: [40, 20, 12]
        },
        {
          label: "Medium",
          backgroundColor: "#232F34",
          data: [65, 12, 14]
        },
        {
          label: "Medium",
          backgroundColor: "#FFCF44",
          data: [65, 12, 14]
        }
      ],
    })
  }
</script>

<style>

</style>