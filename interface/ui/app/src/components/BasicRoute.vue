<template>
  <b-container id='basic'>
    <h1>{{ msg }}</h1>
    Your name is {{ $route.params.name }}
    <router-view/>
  </b-container>
</template>

<script>
  // We can now import this as `import HelloWorld from '@/components/HelloWorld';` as seen in
  // router/index.js
  export default {
    name: 'basic',
    data() {
      return {
        msg: 'BasicRoute component',
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
