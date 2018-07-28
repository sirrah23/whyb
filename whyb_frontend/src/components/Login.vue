<template>
    <div data-app id="login">
        <v-flex xs12 sm6 offset-sm3 mt-4>
            <div id="auth-warn" class="red--text" v-if="authFail">
                Invalid Credentials
            </div>
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
import api from '@/api.js'
import auth from '@/auth_token.js'

export default {
  name: 'Login',
  data: function () {
    return {
      username: null,
      password: null,
      authFail: false
    }
  },
  methods: {
    submit () {
      api.auth(this.username, this.password)
        .then(res => {
          if (res.err) {
            this.authFail = true
            return
          }
          this.authFail = false
          auth.set_auth_token(res.data)
          this.$emit('authenticated', true)
        })
    }
  }
}
</script>

<style scoped>
a {
  color: #42b983;
}
</style>
