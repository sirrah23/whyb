<template>
  <div class="login">
      <Login
      @authenticated="propogateAuthenticated"
      />
  </div>
</template>

<script>
import Login from '@/components/Login.vue'

export default {
  name: 'login',
  data () {
    return {}
  },
  methods: {
    propogateAuthenticated () {
      this.$emit('authenticated', true)
    }
  },
  components: {
    Login
  }
}
</script>
