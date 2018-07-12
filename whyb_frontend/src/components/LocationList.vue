<template>
  <div data-app id="location-list">
    <v-flex xs12 sm6 offset-sm3>
      <v-form id="location-list-form"  lazy-validation>
        <v-text-field
          v-model="uiLocationName"
          :counter="40"
          label="Location Name"
          required
        ></v-text-field>
        <v-text-field
          v-model="uiLatitude"
          label="Latitude"
          required
        ></v-text-field>
        <v-select
          v-model="uiLatitudeDirection"
          :items="latitudeDirections"
          label="Latitude Direction"
          required
        ></v-select>
        <v-text-field
          v-model="uiLongitude"
          label="Longitude"
          required
        ></v-text-field>
        <v-select
          v-model="uiLongitudeDirection"
          :items="longitudeDirections"
          label="Longitude Direction"
          required
        ></v-select>
        <v-btn
          @click="locationListAppend"
        >
        Add
        </v-btn>
      </v-form>
    </v-flex>
    <div class="location-list-item" v-for="(location, index) in locations" :key="index">
      <v-layout>
          <v-flex xs12 sm6 offset-sm3>
            <v-expansion-panel>
              <v-expansion-panel-content>
              <div slot="header">{{location.locationName}}</div>
              <v-card>
                <v-card-text>Latitude: {{location.latitude}}{{location.latitudeDirection[0]}}</v-card-text>
                <v-card-text>Longitude: {{location.longitude}}{{location.longitudeDirection[0]}}</v-card-text>
              </v-card>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-flex>
        </v-layout>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LocationList',
  data: function () {
    return {
      uiLocationName: '',
      uiLatitude: '',
      uiLongitude: '',
      uiLatitudeDirection:'',
      uiLongitudeDirection:'',
      latitudeDirections: ['North', 'South'],
      longitudeDirections: ['East', 'West']
    }
  },
  methods: {
    buildLocObj () {
      return {
        locationName: this.uiLocationName,
        latitude: this.uiLatitude,
        longitude: this.uiLongitude,
        latitudeDirection: this.uiLatitudeDirection,
        longitudeDirection: this.uiLongitudeDirection
      }
    },
    clearUIInput () {
      this.uiLocationName = ''
      this.uiLatitude = ''
      this.uiLongitude = ''
      this.uiLatitudeDirection = ''
      this.uiLongitudeDirection = ''
    },
    locationListAppend () {
      const loc = this.buildLocObj()
      this.$store.commit('addLocation', loc)
      this.clearUIInput()
    }
  },
  computed: {
    locations () {
      return this.$store.getters.locations
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
a {
  color: #42b983;
}
</style>
