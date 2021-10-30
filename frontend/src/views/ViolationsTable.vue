<template>
  <v-row>
    <v-col cols="9">
      <v-data-table
        :headers="headers"
        :items="filtereditems"
        :items-per-page="10"
        class="elevation-1"
        :footer-props="{ 'items-per-page-options': [5, 10, 15] }"
        @click:row="(row) => (selected = row)"
      >
        <template v-slot:top>
          <v-row>
            <v-col cols="4">
              <v-toolbar-title class="ml-5 mt-3">Нарушения</v-toolbar-title>
            </v-col>
            <v-col cols="8">
              <div class="d-flex align-items-center justify-content-end">
                <v-text-field
                  prepend-icon="search"
                  label="Поиск"
                  v-model="search"
                ></v-text-field>
                <filter-date v-model="dates"></filter-date>
              </div>
            </v-col>
          </v-row>
        </template>
      </v-data-table>
    </v-col>
    <v-col cols="3">
      <v-card width="400">
        <v-img
          height="200px"
          contain
          :src="
            selected.frame
              ? selected.frame.photo
              : 'https://lh3.googleusercontent.com/proxy/I5jMTQe_g6KsFDoavPRIAh0injcdnbfDoPyM1-t0feO2BZTpBhOZQHuz9UXCWrGf-iHwZrOFgwxtJU8s6VAd9ij7WT8rRN20FOBj_25CRJEHNZMUaC7x-1lF_segEvMOPsXOXwMeHVHfQzFLVw'
          "
          @click="selected.id ? $router.replace({name: 'ViolationPhoto', params: {id: selected.id}}) : null"
          :style="selected.id ? 'cursor: pointer;' : ''"
        >
        </v-img>

        <v-card-text>
          <div v-if="selected.frame">
            <v-list disabled>
              <v-subheader>Нарушение</v-subheader>
              <v-list-item-group color="primary">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon>mdi-clock</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{
                      selected.frame.dttm
                    }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon>mdi-account</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{
                      selected.employee
                        ? selected.employee.last_name +
                          " " +
                          selected.employee.first_name
                        : "Неизвестно"
                    }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </div>
          <p v-else>Выберите нарушение</p>
        </v-card-text>
      </v-card>
    </v-col>
     <router-view></router-view>
  </v-row>
</template>

<script>
import FilterDate from "../components/FilterDate.vue";
export default {
  components: { FilterDate },
  data() {
    return {
      selected: {},
      search: '',
      headers: [
        {
          text: "Время",
          value: "frame.dttm",
        },
        { text: "Камера", value: "frame.camera_name" },
        { text: "Номер цеха", value: "frame.camera_name" },
      ],
    };
  },
  computed: {
    dates: {
      get() {
        return this.$store.state.dates;
      },
      set(value) {
        this.$store.commit("setDates", value);
      },
    },
    filtereditems() {
      return this.$store.state.violations.filter((item) => {
        return item.frame.camera_name.toLowerCase().match(this.search.toLowerCase());
      });
    },
  },
  watch: {
    async dates() {
      await this.$store.dispatch("setViolations");
      if (
        this.$route.query.dt_from == this.dates[0] &&
        this.$route.query.dt_to == this.dates[1]
      )
        return;
      this.$router.replace({
        name: this.$route.name,
        query: {
          ...this.$route.query,
          dt_from: this.dates[0],
          dt_to: this.dates[1],
        },
      });
    },
  },
  async mounted() {
    if (!this.$store.state.violations.length) {
      this.dates = [
        this.$route.query.dt_from || new Date().toISOString().substr(0, 10),
        this.$route.query.dt_to || new Date().toISOString().substr(0, 10),
      ];
    }
  },
};
</script>

<style>
</style>