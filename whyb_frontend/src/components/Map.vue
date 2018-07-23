<template>
  <div data-app>
      <v-flex xs12 sm6 offset-sm3 fill-height>
        <v-card height=500>
          <div ref="canvas"></div>
        </v-card>
      </v-flex>
    </div>
</template>

<script>
import Mappa from 'mappa-mundi'

export default {
  name: 'Map',
  data () {
    return {
      'ps': null,
      'script': null,
      'width': 0,
      'height': 0,
      'canvas': null,
      'map': null
    }
  },
  mounted () {
    // NOTE: This code was obtained from https://github.com/processing/p5.js/issues/2646
    // TODO: Clean this code up

    const mappa = new Mappa('Leaflet')

    this.script = p => {
      p.setup = _ => {
        this.canvas = p.createCanvas(0, 0)
        this.canvas.parent(this.$refs.canvas)
        console.log(this.canvas.parent())
        this.canvas.width = this.canvas.parent().parentElement.clientWidth // gross code
        this.canvas.height = this.canvas.parent().parentElement.clientHeight
        const options = {
          lat: 0,
          lng: 0,
          zoom: 4,
          style: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png'
        }
        this.map = mappa.tileMap(options)
        this.map.overlay(this.canvas)
      }

      p.draw = _ => {
      }
    }

    const P5 = require('p5')
    this.ps = new P5(this.script)
  }
}
</script>

<style>
</style>
