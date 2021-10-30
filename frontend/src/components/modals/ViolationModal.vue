<template>
  <v-dialog v-model="show" max-width="1000px" @click:outside="closeModal()">
    <v-card>
      <v-img
        :src="frame.photo"
        class="white--text align-right"
        style="text-shadow: 0 0 1px #000000"
      >
        <v-card-text>
          <v-btn icon @click="closeModal()" class="float-right" color="white"><v-icon>close</v-icon></v-btn>
          <p>{{ frame.dttm }}</p>
        </v-card-text>
      </v-img>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  data() {
    return {};
  },
  computed: {
    show() {
      return this.$route.name == "ViolationPhoto";
    },
    frame() {
      return this.$store.state.violations.filter(
        (v) => v.id == this.$route.params.id
      )[0].frame;
    },
  },
  methods: {
    closeModal() {
      var q = { ...this.$route.query };
      this.$router.replace({
        name: "Violation",
        query: q,
      });
    },
  },
};
</script>
<style>
</style>