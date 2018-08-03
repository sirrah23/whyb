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
      return {err: null, data: res.data}
    } catch (err) {
      return {err, data: null}
    }
  },
  async getLocations(token){
    const api = fullAPIPath('locations')
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authorization': `JWT ${token}`
      }
    }
    try {
      const res = await axios.get(api, config)
      return {err: null, data: res.data}
    } catch (err) {
      return {err, data: null}
    }
  },
  async getLocation(token, id){
    const api = `${fullAPIPath('location')}/${id}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authorization': `JWT ${token}`
      }
    }
    try {
      const res = await axios.get(api, config)
      return {err: null, data: res.data}
    } catch (err) {
      return {err, data: null}
    }
  },
  async getLocationsDetail(token){
    const locs = await this.getLocations(token)
    if(locs.err){
      return [];
    }
    const details = []
    for(let i = 0; i < locs.data.data.length; i++){  //TODO: Make this faster with a Array.map await instead
      let curr_loc_id = locs.data.data[i]
      let curr_loc_detail = await this.getLocation(token, curr_loc_id)
      if(!curr_loc_detail.err) details.push(curr_loc_detail.data.data)
    }
    return details
  }
}

export default {
  authAPI,
  locationAPI
}

