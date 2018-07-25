<template>
    <div data-app id="login">
        <v-flex xs12 sm6 offset-sm3 mt-4>
            <v-form>
                <v-text-field
                    label="Username"
                    v-model="username"
                    required
                ></v-text-field>
                <v-text-field
                    label="Password"
                    v-model="password"
                    :type="'password'"
                    required
                ></v-text-field>
                <v-btn
                    @click="submit"
                >Login</v-btn>
            </v-form>
        </v-flex>
    </div>
</template>

<script>
export default {
  name: 'Login',
  data: function () {
    return {
        username: null,
        password: null
    }
  },
  methods: {
      submit(){
          if(this.username == this.$parent.fakeAccount.username && this.password == this.$parent.fakeAccount.password){
              this.$emit("authenticated", true)
          }
      }
  }
}
</script>

<style scoped>
a {
  color: #42b983;
}
</style>