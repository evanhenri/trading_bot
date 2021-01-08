<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
  </div>
</template>

<script>
  // We can now import this as `import HelloWorld from '@/components/HelloWorld';` as seen in
  // router/index.js
  export default {
    name: 'HelloWorld',
    data() {
      return {
        msg: 'HelloWorld component',
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
