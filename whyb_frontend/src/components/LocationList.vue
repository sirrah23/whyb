<template>
  <div id="location-list">
    <h2>Locations</h2>
    <form id="location-list-form">
      <input type="text" name="location" placeholder="Location" v-model="location">
      <input type="text" name="latitude" placeholder="Latitude" v-model="latitude">
      <input type="text" name="longitude" placeholder="Longitude" v-model="longitude">
      <button id="location-list-add" type="button" @click="locationListAppend">Add</button>
    </form>
    <ul>
      <div class="location-list-item" v-for="(location, index) in locations" :key="index">
        <li>Location: {{ location.location }}</li>
        <li>Latitide: {{ location.latitude }}</li>
        <li>Longitude: {{ location.longitude }}</li>
      </div>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'LocationList',
  data: function () {
    return {
      location: '',
      latitude: '',
      longitude: ''
    }
  },
  methods: {
    buildLocObj () {
      return {
        location: this.location,
        latitude: this.latitude,
        longitude: this.longitude
      }
    },
    clearUIInput () {
      this.location = ''
      this.latitude = ''
      this.longitude = ''
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
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
