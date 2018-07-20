import { expect } from 'chai'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import LocationList from '@/components/LocationList.vue'
import Vuex from 'vuex'
import store from '@/store.js'
import '@/plugins/vuetify'
import Vue from 'vue'

Vue.config.silent = true // Note: Workaround to silence vuetify warnings

const localVue = createLocalVue()
localVue.use(Vuex)

describe('ListLocation.vue', () => {
  it('Renders empty location list when no locations are available', () => {
    const wrapper = shallowMount(LocationList, {store, localVue})
    expect(wrapper.contains('div')).to.equal(true)
    const locations = wrapper.findAll('.location-list-item')
    expect(locations.length).to.equal(0)
  })

  it('Renders locations when locations are available', () => {
      store.commit(
          'addLocation',
          {
            locationName: 'Location A',
            latitude: 30,
            longitude: 30,
            latitudeDirection: 'N',
            longitudeDirection: 'E'
          }
      )
      store.commit(
          'addLocation',
          {
            locationName: 'Location B',
            latitude: 45,
            longitude: 50,
            latitudeDirection: 'S',
            longitudeDirection: 'W'
          }
      )
    const wrapper = shallowMount(LocationList, {store, localVue})
    const locations = wrapper.findAll('.location-list-item')
    expect(locations.length).to.equal(2)
  })
})
