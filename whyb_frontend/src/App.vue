<template>
  <div id="app">
    <div id="header">
      <h1 class="display-4">Where have you been?</h1>
    </div>
    <router-view @authenticated="setAuthenticated" />
    <router-link v-if="authenticated" to="/login" @click.native="logout" replace>Logout</router-link>
  </div>
</template>

<script>
import auth from '@/auth_token.js'

export default{
  name: 'App',
  data () {
    return {
      authenticated: false
    }
  },
  mounted () {
    if (!this.checkAuthentication()) {
      this.$router.replace({name: 'login'})
    } else {
      this.$router.replace({name: 'home'})
    }
  },
  methods: {
    isAuthenticated () {
      return this.authenticated
    },
    checkAuthentication () {
      this.authenticated = auth.is_auth_token()
      return this.authenticated
    },
    setAuthenticated (status) {
      this.authenticated = status
      if (status && auth.is_auth_token()) {
        this.$router.replace({name: 'home'})
      }
    },
    clearSessionData (){
      this.$store.commit('reset')
    },
    logout () {
      this.clearSessionData()
      this.setAuthenticated(false)
      auth.clear_auth_token()
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
