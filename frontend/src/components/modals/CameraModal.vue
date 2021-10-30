<template>
  <v-dialog v-model="show" max-width="800px" @click:outside="closeModal()">
    <v-card>
      <v-card-title class="text-h5">
        Редактирование параметров камеры {{ camera.name }}
      </v-card-title>
      <v-container>
        <v-row>
          <v-col cols="6">
            <v-text-field
              type="number"
              label="Вертикальный угол наклона камеры"
              suffix="°"
              outlined
              v-model="camera.vertical_angle"
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              type="number"
              label="Горизонтальный угол наклона камеры"
              suffix="°"
              outlined
              v-model="camera.horizontal_angle"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6">
            <v-text-field
              type="number"
              label="Высота установки камеры"
              suffix="м"
              outlined
              v-model="camera.height"
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              type="number"
              label="Расстояние от камеры до ограничительной линии"
              suffix="м"
              outlined
              v-model="camera.distance_to_line"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6">
            <v-text-field
              type="number"
              label="Фокусное расстояние объектива"
              suffix="мм"
              outlined
              v-model="camera.focus"
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              type="number"
              label="Размер сенсора"
              suffix="дюйм"
              outlined
              v-model="camera.sensor_size"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-container>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="green darken-1" text @click="closeModal()">
          Отмена
        </v-btn>
        <v-btn color="green darken-1" text @click="save()">
          Сохранить
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import http from '../../http'

export default {
  data() {
    return {};
  },
  computed: {
    show() {
      return this.$route.name == "CameraConfig";
    },
    camera: {
      get() {
        let ind = this.$store.state.cameras.findIndex(
          (v) => v.id == this.$route.params.id
        );
        if (ind != -1) {
          return { ...this.$store.state.cameras[ind] };
        }
        return {};
      },
      set(value) {
        let ind = this.$store.state.cameras.findIndex(
          (v) => v.id == this.$route.params.id
        );
        let cameras = [...this.$store.state.cameras];
        cameras[ind] = value;
        this.$store.commit("setCameras", cameras);
      },
    },
  },
  methods: {
    closeModal() {
      var q = { ...this.$route.query };
      this.$router.replace({
        name: "Camera",
        query: q,
      });
    },
    async save() {
        let response = await http.updateItem('Camera', this.camera.id, this.camera, true);
        this.camera = response.data;
    }
  },
};
</script>
<style>
</style>