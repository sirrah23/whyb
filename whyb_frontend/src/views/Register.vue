<template>
    <div data-app id="register">
        <v-flex xs12 sm6 offset-sm3 mt-4>
            <div id="register-success" class="green--text" v-if="registerSuccessMessage.length > 0">
                {{registerSuccessMessage}}
            </div>
            <div id="register-warn" class="red--text" v-if="registerErrorMessage.length > 0">
                {{registerErrorMessage}}
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
                <v-text-field
                    label="Confirm Password"
                    v-model="confirm_password"
                    :type="'password'"
                    required
                ></v-text-field>
                <v-btn
                    @click="submit"
                >Register</v-btn>
            </v-form>
        </v-flex>
    </div>
</template>

<script>
import api from '@/api.js'

export default {
  name: 'Register',
  data: function () {
    return {
      username: '',
      password: '',
      confirm_password: '',
      registerSuccessMessage: '',
      registerErrorMessage: ''
    }
  },
  methods: {
    submit () {
      const valid = this.validate()
      if (!valid) { return }
      api.authAPI.registerRequest(this.username, this.password)
        .then(res => {
          console.log(res)
          if (res.success === true) {
            this.setSuccess()
          } else {
            this.setFail(res.err.response.data)
          }
        })
        .catch(err => console.log(err))
    },
    validate () {
      let errMsg = ''
      if (!this.username) {
        errMsg = 'Missing username'
      } else if ((!this.password) || (!this.confirm_password)) {
        errMsg = 'Missing password'
      } else if (this.password !== this.confirm_password) {
        errMsg = 'Passwords do not match'
      }
      if (errMsg.length > 0) { this.setFail(errMsg) }
      return this.registerErrorMessage.length === 0
    },
    setSuccess () {
      this.registerSuccessMessage = 'Registration was successful!'
    },
    setFail (errMsg) {
      this.registerErrorMessage = errMsg
    }
  }

}
</script>

<style scoped>
a {
  color: #42b983;
}
</style>
