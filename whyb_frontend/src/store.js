import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    locations: []
  },
  mutations: {
    addLocation (state, loc) {
      state.locations.push(loc)
    },
    deleteLocation (state, locId) {
      state.locations = state.locations.filter(loc => loc.id !== locId)
    },
    reset (state) {
      state.locations = []
    }
  },
  getters: {
    locations (state) {
      return state.locations
    }
  }
})
