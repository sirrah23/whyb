import axios from 'axios'

const API_HOST = 'http://localhost:5000'

export default {
  fullAPIPath (path) {
    return `${API_HOST}/${path}`
  },
  async auth (username, password) {
    const api = this.fullAPIPath('auth')
    const data = {username, password}
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    }
    try {
      const res = await axios.post(api, data, config)
      return {err: null, data: res.data.access_token}
    } catch (err) {
      return {err, data: null}
    }
  }
}
