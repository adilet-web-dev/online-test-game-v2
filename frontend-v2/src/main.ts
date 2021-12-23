import Vue from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import router from './router';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

import VueCookies from "vue-cookies-ts";


Vue.config.productionTip = false;
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

Vue.use(VueCookies);

export let app = new Vue({
  router,

  render: (h) => h(App),
})

app.$mount?.('#app');
