/**
This mock version of localStorage is used when the window
version of it is unavailable...it doesn't really do anything
and is here so that unit tests pass when window is unavailable
*/
const mockStorage = {
  getItem () {},
  setItem () {},
  removeItem () {}
}

export default {
  tokenField: 'whyb-auth-token',
  storage: window.localStorage || mockStorage,
  get_auth_token () {
    return this.storage.getItem(this.tokenField)
  },
  set_auth_token (newToken) {
    this.storage.setItem(this.tokenField, newToken)
  },
  clear_auth_token () {
    this.storage.removeItem(this.tokenField)
  },
  is_auth_token () {
    return this.get_auth_token() !== null
  }
}
