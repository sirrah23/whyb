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
  export default{
    name: "App",
    data(){
      return {
        authenticated: false
      }
    },
    mounted(){
      if(!this.authenticated){
        this.$router.replace({name:"login"})
      }
    },
    methods: {
      setAuthenticated(status){
        this.authenticated = status
        if(status){
          this.$router.replace({name: "home"})
        }
      },
      logout(){
        this.setAuthenticated(false)
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
