<template>
  <div data-app id="location-list">
    <v-flex xs12 sm6 offset-sm3 mt-4>
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
        <v-text-field
          v-model="uiLongitude"
          label="Longitude"
          required
        ></v-text-field>
        <v-btn
          @click="locationListAppend"
        >
        Add
        </v-btn>
      </v-form>
    </v-flex>
    <div class="location-list-item" v-for="location in locations" :key="location.id">
      <v-layout>
          <v-flex xs12 sm6 offset-sm3 mt-3 mb-3>
            <v-card>
              <v-container fill-height fluid>
                <v-layout fill-height>
                  <v-flex xs12 align-end flexbox>
                      <span class="headline">{{location.name}}</span>
                        <div>
                          <span>Latitude: {{location.latitude}}</span><br>
                          <span>Longitude: {{location.longitude}}</span>
                        </div>
                  </v-flex>
                </v-layout>
              </v-container>
          <v-card-actions>
            <v-btn flat color="red" @click="locationListDelete(location.id)">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
      </v-layout>
    </div>
  </div>
</template>

<script>
import auth from '@/auth_token.js'
import api from '@/api.js'

export default {
  name: 'LocationList',
  data: function () {
    return {
      uiLocationName: '',
      uiLatitude: '',
      uiLongitude: ''
    }
  },
  methods: {
    buildLocObj () {
      return {
        name: this.uiLocationName,
        latitude: this.uiLatitude,
        longitude: this.uiLongitude
      }
    },
    clearUIInput () {
      this.uiLocationName = ''
      this.uiLatitude = ''
      this.uiLongitude = ''
    },
    locationListAppend () {
      const token = auth.get_auth_token()
      const loc = this.buildLocObj()
      api.locationAPI.addLocation(token, loc)
        .then((res) => {
          if (res.err) {
            console.log(res.err) // TODO: Do something useful?
            return
          }
          this.$store.commit('addLocation', res.data.data)
          this.clearUIInput()
        })
        .catch(e => console.log(e))
    },
    locationListDelete (locId) {
      const token = auth.get_auth_token()
      api.locationAPI.deleteLocation(token, locId)
        .then((res) => {
          if (res.err) {
            console.log(res.err) // TODO: Do something useful?
            return
          }
          this.$store.commit('deleteLocation', locId)
        })
        .catch(e => console.log(e))
    }
  },
  computed: {
    locations () {
      return this.$store.getters.locations
    }
  },
  mounted () {
    const token = auth.get_auth_token()
    if (!token) return
    api.locationAPI.getLocationsDetail(token)
      .then(locs => {
        for (let i = 0; i < locs.length; i++) { this.$store.commit('addLocation', locs[i]) }
      })
      .catch(e => console.log(e))
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
a {
  color: #42b983;
}
</style>
