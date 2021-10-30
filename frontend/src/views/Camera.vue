<template>
  <div>
    <v-row>
      <v-col cols="10">
        <v-card color="black">
          <v-img
            :src="$store.state.selectedCamera.last_frame.photo"
            class="white--text align-end"
            height="88vh"
            contain
            style="text-shadow: 0 0 1px #000000;"
          >
            <v-card-title
              v-text="$store.state.selectedCamera.name"
            ></v-card-title>
            <v-card-text>
              <p>{{ $store.state.selectedCamera.last_frame.dttm }}</p>
              <p>{{ $store.state.selectedCamera.code }}</p></v-card-text
            >
          </v-img>
        </v-card>
      </v-col>
      <v-col cols="2" style="overflow-y: scroll; max-height: 90vh">
        <camera-gallery></camera-gallery>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import CameraGallery from "../components/CameraGallery.vue";
export default {
  components: {
    CameraGallery,
  },
  async mounted() {
    await this.$store.dispatch('setCameras');
  }
};
</script>

<style>
</style>