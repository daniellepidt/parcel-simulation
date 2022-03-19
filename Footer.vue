<template>
  <v-footer
    padless
  >
    <v-card
      class="flex text--primary"
      flat
      tile
      color="background"
    >
      <v-row align="center" justify="space-between" class="pt-2" no-gutters>
        <v-col cols="12" sm="4" align="center" align-self="center">
          <div class="text-b1">
            0571311001 - Simulation, Industrial Engineering B.Sc
          </div>
        </v-col>
        <v-col cols="12" sm="2" align="center" align-self="center">
          <v-img
            alt="Tel Aviv University Logo"
            contain
            :src="require('../assets/tau_logo.png')"
            max-width="100"
          />
        </v-col>
      </v-row>
        
      <v-card-text class="py-2 text--primary text-center">
        {{ new Date().getFullYear() }} — <strong>Menny's Parents</strong> — All rights reserved
      </v-card-text>
    </v-card>
  </v-footer>
</template>

<script>
export default {

}
</script>

<style>

</style>