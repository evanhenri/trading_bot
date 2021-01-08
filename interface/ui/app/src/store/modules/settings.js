import types from '../mutation-types';


const state = {
  navType: 'dark',
  navVariant: 'dark',
  iconSize: 3,
};

const getters = {
  iconSize(s) {
    return s.iconSize;
  },
  navType(s) {
    return s.navType;
  },
  navVariant(s) {
    return s.navVariant;
  },
};

/* eslint-disable no-param-reassign */
const mutations = {
  [types.SET_ICON_SIZE](s, iconSize) {
    s.iconSize = iconSize;
  },
  [types.SET_NAV_TYPE](s, navType) {
    s.navType = navType;
  },
  [types.SET_NAV_VARIANT](s, navVariant) {
    s.navVariant = navVariant;
  },
};


export default {
  state,
  getters,
  mutations,
};
