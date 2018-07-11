<template>
  <div class="home">
    <LocationList/>
  </div>
</template>

<script>
// @ is an alias to /src
import LocationList from '@/components/LocationList.vue'

export default {
  name: 'home',
  components: {
    LocationList
  }
}
</script>
