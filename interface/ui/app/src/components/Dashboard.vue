<template>
  <b-container id='dashboard'>
    <h1>{{ msg }}</h1>

    <h2>Current time: {{ current_time }}</h2>
    <h2>API host: {{ hostname }}</h2>

    <b-button @click.prevent='requestBtnClick' :variant='btnVariant'>
      {{ btnCaption }}
    </b-button>

    <b-button @click.prevent='resetBtnClick' variant='secondary'>
      Reset
    </b-button>

    <b-button @click.prevent='clearBtnClick' variant='info'>
      Clear
    </b-button>

    <div v-for='resp in responses'>
      <b>{{ resp.id }}) {{ resp.title | uppercase }}</b>
      <p>{{ resp.body | snippet }}</p>
    </div>
  </b-container>
</template>

<script>
  export default {
    name: 'Dashboard',
    data() {
      return {
        btnCaption: 'Requests 0',
        btnClicks: 0,
        btnVariant: 'primary',
        msg: 'Dashboard component',
        responses: [],
        current_time: null,
        hostname: null,
      };
    },
    methods: {
      clearBtnClick() {
        this.responses.splice(0, this.responses.length);
      },
      resetBtnClick() {
        this.btnClicks = 0;
        this.btnCaption = `Requests ${this.btnClicks}`;
        this.btnVariant = 'primary';
        this.responses.splice(0, this.responses.length);
      },
      requestBtnClick() {
        this.btnClicks += 1;
        this.btnCaption = `Requests ${this.btnClicks}`;

        if (this.btnClicks >= 5) {
          this.btnVariant = 'warning';
        }
        if (this.btnClicks >= 10) {
          this.btnVariant = 'danger';
        }

        const requestId = this.responses.length + 1;
        this.$http.get(
          `https://jsonplaceholder.typicode.com/posts/${requestId}`,
        ).then(
          (response) => {
            response.json().then(
              (json) => {
                this.responses.push({
                  id: requestId,
                  title: json.title,
                  body: json.body,
                });
              },
            );
          },
        );
      },
    },
    mounted() {
      this.$http.get(
        'http://ui.k8s.nonce.ch/api/v1/time',
      ).then(
        (response) => {
          response.json().then(
          (json) => {
            this.current_time = json.time;
          });
        },
      );
      this.$http.get(
        'http://ui.k8s.nonce.ch/api/v1/hostname',
      ).then(
        (response) => {
          response.json().then(
          (json) => {
            this.hostname = json.hostname;
          });
        },
      );
    },
  };
</script>

<style scoped>
</style>
