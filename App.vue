<template>
  <v-app>
    <TopNav/>
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
    <Footer/>
  </v-app>
</template>

<script>
import TopNav from "./components/TopNav.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "App",
  components: {
    TopNav,
    Footer
  }
}
</script>
