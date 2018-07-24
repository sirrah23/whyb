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
      'canvas': null,
      'map': null
    }
  },
  mounted () {
    // NOTE: This code was obtained from https://github.com/processing/p5.js/issues/2646

    const mappa = new Mappa('Leaflet')

    this.script = p => {
      p.setup = _ => {
        // Initialize the canvas
        // Make the canvas the same size as the v-flex wrapper around it
        const canvasDiv = this.$refs.canvas
        this.canvas = p.createCanvas(canvasDiv.parentElement.clientWidth, canvasDiv.parentElement.clientHeight)
        this.canvas.parent(canvasDiv)

        // Initialize the map
        const options = {
          lat: 0,
          lng: 0,
          zoom: 4,
          style: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png'
        }
        this.map = mappa.tileMap(options)
        this.map.overlay(this.canvas)
        this.map.onChange(p.drawPoints)
      }

      p.drawPoints = _ => {
        // Draw a dot on the map for each location in the list
        p.clear()
        p.fill(200, 100, 100)
        let locMap
        for (let i = 0; i < this.$store.getters.locations.length; i++) {
          locMap = this.map.latLngToPixel(this.$store.getters.locations[i].latitude, this.$store.getters.locations[i].longitude)
          p.ellipse(locMap.x, locMap.y, 20, 20)
        }
      }
    }

    const P5 = require('p5')
    this.ps = new P5(this.script)
  }
}
</script>

<style>
</style>
