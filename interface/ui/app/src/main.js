import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import 'vue-awesome/icons';
import Icon from 'vue-awesome/components/Icon';
import VueResource from 'vue-resource';

import './assets/scss/global.scss';
import filters from './filters';
import router from './router';
import store from './store';

import App from './App';

Vue.use(BootstrapVue);
Vue.use(VueResource);

Vue.component('icon', Icon);

Vue.filter('snippet', filters.snippet);
Vue.filter('uppercase', filters.uppercase);

Vue.config.productionTip = false;

Vue.http.options.root = '';
Vue.http.options.responseType = 'application/json';
Vue.http.options.timeout = 30 * 1000;  // 30 seconds

Icon.register({
  vue: {
    width: 256,
    height: 221,
    polygons: [
      {
        style: 'fill:#41B883',
        points: '0,0 128,220.8 256,0 204.8,0 128,132.48 50.56,0 0,0',
      },
      {
        style: 'fill:#35495E',
        points: '50.56,0 128,133.12 204.8,0 157.44,0 128,51.2 97.92,0 50.56,0',
      },
    ],
  },
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: {
    App,
  },
});
