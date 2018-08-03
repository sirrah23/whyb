import axios from 'axios'

function fullAPIPath (path) {
    const API_HOST = 'http://localhost:5000'
    return `${API_HOST}/${path}`
}

const authAPI = {
  async tokenRequest (username, password) {
    const api = fullAPIPath('auth')
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

const locationAPI = {
  async addLocation(token, {name, latitude, longitude}){
    const api = fullAPIPath('locations')
    const data = {name, latitude, longitude}
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authorization': `JWT ${token}`
      }
    }
    try {
      const res = await axios.post(api, data, config)
      console.log(res.data)
      return {err: null, data: res.data}
    } catch (err) {
      return {err, data: null}
    }
  }
}

export default {
  authAPI,
  locationAPI
}

