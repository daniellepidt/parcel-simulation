import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import './registerServiceWorker'
import store from './store'
import router from './router'
import { firestorePlugin } from 'vuefire'

Vue.use(firestorePlugin)
Vue.config.productionTip = false

new Vue({
  vuetify,
  store,
  router,
  render: h => h(App)
}).$mount('#app')
