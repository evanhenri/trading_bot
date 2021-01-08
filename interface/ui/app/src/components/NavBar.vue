<template>
  <b-navbar :variant='navVariant' :type='navType' class='navbar-expand-md'>
    <b-navbar-brand :to='{name: "dashboard"}'>
      <icon name='vue' :scale='iconSize' spin></icon>
    </b-navbar-brand>

    <b-nav is-nav-bar>
      <b-nav-item :to='{name: "dashboard"}'>Dashboard</b-nav-item>
      <b-nav-item :to='{name: "settings"}'>Settings</b-nav-item>

      <b-nav-item-dropdown text="Routes" right>
        <b-dropdown-item :to='{name: "BasicRoute", params: {name: "Evan"}}'>BasicRoute</b-dropdown-item>
        <b-dropdown-item :to='{name: "BasicRouteFirstChild", params: {name: "Evan"}}'>BasicRouteFirstChild</b-dropdown-item>
        <b-dropdown-item :to='{name: "BasicRouteSecondChild", params: {name: "Evan", childName: "Henri"}}'>BasicRouteSecondChild</b-dropdown-item>
      </b-nav-item-dropdown>
    </b-nav>

    <b-nav is-nav-bar class='ml-auto'>
      <b-nav-form>
        <b-form-input v-model='searchText' class='mr-sm-2' type='text' placeholder='Search'></b-form-input>
        <b-button class='my-2 my-sm-0' type='submit' variant='outline-success'>Search</b-button>
      </b-nav-form>
    </b-nav>
  </b-navbar>
</template>

<script>
  import { mapGetters } from 'vuex';

  export default {
    data() {
      return {
        searchText: '',
      };
    },
    computed: {
      ...mapGetters({
        iconSize: 'iconSize',
        navType: 'navType',
        navVariant: 'navVariant',
      }),
    },
  };
</script>

<style>
</style>
