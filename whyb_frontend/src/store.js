import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    locations: []
  },
  mutations: {
    addLocation(state, loc){
      state.locations.push(loc)
    }
  },
  getters:{
    locations(state){
      return state.locations;
    }
  }
})
