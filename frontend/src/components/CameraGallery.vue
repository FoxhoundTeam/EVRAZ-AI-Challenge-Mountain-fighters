<template>
  <div>
    <v-row>
      <v-col v-for="camera in $store.state.cameras" :key="camera.id" @click="$store.commit('setSelectedCamera', camera)">
        <v-card :class="camera.id == $store.state.selectedCamera.id ? 'selected-camera' : ''" style="cursor: pointer; text-shadow: 0 0 2px #000000;">
          <v-img
            :src="camera.last_frame.photo"
            class="white--text align-end"
            height="200px"
          >
            <v-card-title v-text="camera.name"></v-card-title>
            <v-card-text>
              <p>{{ camera.last_frame.dttm }}</p>
            </v-card-text>
          </v-img>

        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {};
</script>

<style>

.selected-camera {
    border: 1px solid !important;
    border-color: red !important;
}

</style>