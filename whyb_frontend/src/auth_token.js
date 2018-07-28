export default {
  tokenField: 'whyb-auth-token',
  get_auth_token () {
    return window.localStorage.getItem(this.tokenField)
  },
  set_auth_token (newToken) {
    window.localStorage.setItem(this.tokenField, newToken)
  },
  clear_auth_token () {
    window.localStorage.removeItem(this.tokenField)
  },
  is_auth_token () {
    return this.get_auth_token() !== null
  }
}
