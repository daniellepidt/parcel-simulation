<template>
  <v-app-bar
      app
      color="background"
      elevate-on-scroll
    >
      <v-img
        alt="Menny's Parcel Logo"
        class="shrink me-2"
        contain
        :src="require('../assets/logo.svg')"
        transition="scale-transition"
        width="40"
      />
      <v-toolbar-title color="text--primary">
        Menny's Parcel
      </v-toolbar-title>
      
      <v-spacer></v-spacer>
      
      <div v-if="!$vuetify.breakpoint.mobile" class="me-5">
        <v-btn
          v-for="b of buttons"
          :key="b.text"
          exact
          :to="b.to"
          :disabled="!b.show"
          class="mx-2"
          outlined
          color="primary"
          active-class="secondary"
        >
          <v-icon left>{{ b.icon }}</v-icon>
          {{ b.text }}
        </v-btn>
      </div>
    
      <template v-slot:extension v-if="$vuetify.breakpoint.mobile">
        <v-tabs grow>
          <v-tabs-slider></v-tabs-slider>
          <v-tab
            v-for="b of buttons"
            :key="b.text"
            :to="b.to"
            :disabled="!b.show"
          >
            <v-icon>{{ b.icon }}</v-icon>
          </v-tab>
        </v-tabs>
      </template>
    </v-app-bar>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState([
      'simulationRunning',
      'simulationDone',
    ]),
  },
  data: () => ({
    buttons: [
      {
        text: 'Home',
        to: { name: 'Home' },
        icon: 'mdi-home',
        show: true,
      },
      {
        text: 'Run',
        to: { name: 'Run' },
        icon: 'mdi-run',
        show: true,
      },
      {
        text: 'Simulation',
        to: { name: 'Simulation' },
        icon: 'mdi-view-dashboard',
        show: false,
      },
      {
        text: 'Results',
        to: { name: 'Results' },
        icon: 'mdi-google-analytics',
        show: false,
      },
    ]
  }),
  watch: {
    simulationRunning: function(val) {
      this.buttons[2].show = val;
    },
    simulationDone: function(val) {
      this.buttons[3].show = val;
    },
  }
}
</script>

<style>

</style>