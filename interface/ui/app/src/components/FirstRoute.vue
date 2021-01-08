<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <!--'name' is the arg we defined as a part of the FirstRoute path-->
    Your name is {{ $route.params.name }}

    <!--
    This is needed for the FirstRouteFirstChild and FirstRouteSecondChild
    components because in order to display content for a child route, a
    router-view for the child must get added within the context of the parent
    route.
    -->
    <router-view/>
  </div>
</template>

<script>
  // We can now import this as `import HelloWorld from '@/components/HelloWorld';` as seen in
  // router/index.js
  export default {
    name: 'FirstRoute',
    data() {
      return {
        msg: 'FirstRoute component',
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
