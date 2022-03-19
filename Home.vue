<template>
  <div>
    <v-row justify="space-around" class="mt-2">
      <v-col align-self="center" cols="10" sm="6">
        <div class="text-h5">
          Welcome to the world's best
        </div>
        <div class="text-h2 font-weight-bold">
          Parcel Delivery Simulator
        </div>
      </v-col>
      <v-col align="center" cols="9" sm="4">
        <v-img
        alt="Menny's Parcel Logo"
        contain
        :src="require('../assets/logo.svg')"
        transition="scale-transition"
      />
      </v-col>
    </v-row>
    <v-divider></v-divider>
    <v-row justify="space-around" class="my-5">
      <v-col align="center" align-self="center" cols="12">
        <div class="text-h5">
          Meet our A-List team of experts
        </div>
        <div class="text-h3 font-weight-bold">
          Menny's Parents
        </div>
      </v-col>
      <v-col v-for="member of team" :key="member.name" align="center" cols="9" sm="4">
        <v-card
          class="mx-auto"
          max-width="434"
          tile
        >
          <v-row
            align="end"
            class="fill-height"
          >
            <v-col
              align-self="start"
              class="pb-0"
              cols="12"
            >
              <v-avatar
                class="profile"
                color="grey"
                size="164"
              >
                <v-img :src="require(`../assets/${member.img}`)"></v-img>
              </v-avatar>
            </v-col>
            <v-col class="py-0">
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title class="text-h6">
                    {{ member.name }}
                  </v-list-item-title>
                  <v-list-item-subtitle>{{ member.info }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'Home',
  components: {
  },
  data: () => ({
    team: [
      {
        name: 'Almog',
        img: 'almog.png',
        info: 'Chief Simulation Officer',
      },
      {
        name: 'Daniel',
        img: 'daniel.png',
        info: 'Chief Assignment Officer',
      },
      {
        name: 'Nir',
        img: 'nir.png',
        info: 'Chief Parcelling Officer',
      },
    ]
  })
}
</script>
