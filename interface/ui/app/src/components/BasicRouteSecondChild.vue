<template>
  <b-container id='basic-second'>
    <h1>{{ msg }}</h1>
    Second child 'name' url arg is {{ $route.params.childName }}
  </b-container>
</template>

<script>
  export default {
    name: 'basic-second',
    data() {
      return {
        msg: 'BasicRouteSecondChild component',
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
