<template>
  <b-container id='login'>
    <h1>{{ msg }}</h1>
  </b-container>
</template>

<script>
  export default {
    name: 'Login',
    data() {
      return {
        msg: 'Login component',
      };
    },
  };
</script>

<style scoped>
</style>
