import types from './mutation-types';


const setIconSize = ({ commit }, iconSize) => {
  commit(types.SET_ICON_SIZE, iconSize);
};

const setNavType = ({ commit }, navType) => {
  commit(types.SET_NAV_TYPE, navType);
};

const setNavVariant = ({ commit }, navVariant) => {
  commit(types.SET_NAV_VARIANT, navVariant);
};


export default {
  setIconSize,
  setNavType,
  setNavVariant,
};
