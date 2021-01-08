<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    Second child 'name' url arg is {{ $route.params.childName }}
  </div>
</template>

<script>
  export default {
    name: 'FirstRouteSecondChild',
    data() {
      return {
        msg: 'FirstRouteSecondChild component',
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
