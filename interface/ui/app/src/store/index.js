import Vue from 'vue';
import Vuex from 'vuex';

import actions from './actions';
import settings from './modules/settings';

Vue.use(Vuex);

export default new Vuex.Store({
  actions,
  modules: {
    settings,
  },
  strict: true,
});
