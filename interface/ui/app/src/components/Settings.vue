<template>
  <b-container id='settings'>
    <b-form-row>
      <b-col sm='3'>
        <label>Icon Size</label>
      </b-col>
      <b-col sm='9'>
        <b-form-input type='range' v-model='iconSize'></b-form-input>
      </b-col>
    </b-form-row>

    <b-form-row>
      <b-col sm='3'>
        <label>Nav Type</label>
      </b-col>
      <b-col sm='9'>
        <b-form-select v-model='navTypeSelected' :options='navTypeOptions'></b-form-select>
      </b-col>
    </b-form-row>

    <b-form-row>
      <b-col sm="3">
        <label>Nav Options</label>
      </b-col>
      <b-col sm='9'>
        <b-form-select v-model='navVariantSelected' :options='navVariantOptions'></b-form-select>
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex';

  export default {
    name: 'Settings',
    data() {
      return {
        msg: 'Settings Component',
        iconSize: 3,
        navTypeSelected: null,
        navVariantSelected: null,
        navTypeOptions: [
          { value: null, text: 'Navbar Type' },
          { value: 'dark', text: 'dark' },
          { value: 'light', text: 'light' },
        ],
        navVariantOptions: [
          { value: null, text: 'Navbar Variant' },
          { value: 'primary', text: 'primary' },
          { value: 'danger', text: 'danger' },
          { value: 'warning', text: 'warning' },
          { value: 'success', text: 'success' },
        ],
      };
    },
    computed: {
      ...mapGetters({
        getIconSize: 'iconSize',
        getNavType: 'navType',
        getNavVariant: 'navVariant',
      }),
    },
    methods: mapActions([
      'setIconSize',
      'setNavType',
      'setNavVariant',
    ]),
    watch: {
      iconSize(value) {
        if (value > 0) {
          this.setIconSize(value);
        }
      },
      navTypeSelected(value) {
        if (value !== null) {
          this.setNavType(value);
        }
      },
      navVariantSelected(value) {
        if (value !== null) {
          this.setNavVariant(value);
        }
      },
    },
  };
</script>

<style lang='scss' scoped>
  @import '~bootstrap/scss/_functions.scss';
  @import '~bootstrap/scss/_variables.scss';
</style>
