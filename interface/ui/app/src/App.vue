<template>
  <div id='app'>
    <NavBar></NavBar>

    <router-view/>
  </div>
</template>

<script>
  import NavBar from './components/NavBar';

  export default {
    name: 'app',
    components: {
      NavBar,
    },
    data() {
      return {
      };
    },
  };
</script>

<style>
</style>
