<template>
  <v-sheet :color="color" rounded="lg">
    <v-row>
      <v-col cols="9">
        <h5 class="text-light ml-3">{{ type }} {{ data }}</h5>
      </v-col>
      <v-col cols="3">
        <v-icon x-large color="white">{{ icon }}</v-icon>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script>
export default {
  props: ["color", "type", "data", "icon"],
};
</script>

<style>
</style>