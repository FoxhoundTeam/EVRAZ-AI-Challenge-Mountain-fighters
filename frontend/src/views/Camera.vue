<template>
  <div>
    <v-row>
      <v-col cols="10">
        <v-hover>
          <template v-slot:default="{ hover }">
            <v-card color="black" v-if="$store.state.selectedCamera.id">
              <v-img
                :src="$store.state.selectedCamera.last_frame.photo"
                class="white--text align-end"
                height="88vh"
                contain
                style="text-shadow: 0 0 1px #000000"
              >
                <v-card-title
                  v-text="$store.state.selectedCamera.name"
                ></v-card-title>
                <v-card-text>
                  <p>{{ $store.state.selectedCamera.last_frame.dttm }}</p>
                  <p>{{ $store.state.selectedCamera.code }}</p></v-card-text
                >
              </v-img>
              <v-fade-transition>
                <v-overlay v-if="hover" absolute>
                  <v-btn
                    @click="
                      $router.push({
                        name: 'CameraConfig',
                        params: { id: $store.state.selectedCamera.id },
                      })
                    "
                    >Настроить</v-btn
                  >
                </v-overlay>
              </v-fade-transition>
            </v-card>
          </template>
        </v-hover>
      </v-col>
      <v-col cols="2" style="overflow-y: scroll; max-height: 90vh">
        <v-card class="text-center mb-3">
          <v-card-title style="word-break: normal !important;"><span class="text-body-1 text-no-break">Остановить предупреждения</span></v-card-title>
          <v-btn block class='mb-3' color="warning">На 5 минут</v-btn>
          <v-btn block class="text-light" color="#E53935">На 15 минут</v-btn>
        </v-card>
        <camera-gallery></camera-gallery>
      </v-col>
    </v-row>
    <router-view></router-view>
  </div>
</template>

<script>
import CameraGallery from "../components/CameraGallery.vue";
export default {
  components: {
    CameraGallery,
  },
  async mounted() {
    await this.$store.dispatch("setCameras");
  },
};
</script>

<style>
</style>