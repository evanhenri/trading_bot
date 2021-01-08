<template>
  <b-container id='basic-first'>
    <h1>{{ msg }}</h1>
  </b-container>
</template>

<script>
  export default {
    name: 'basic-first',
    data() {
      return {
        msg: 'BasicRouteFirstChild component',
      };
    },
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }
</style>
