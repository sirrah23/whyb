<template>
  <div class="home">
    <Map/>
    <LocationList/>
  </div>
</template>

<script>
// @ is an alias to /src
import Map from '@/components/Map.vue'
import LocationList from '@/components/LocationList.vue'

export default {
  name: 'home',
  components: {
    Map,
    LocationList
  }
}
</script>
