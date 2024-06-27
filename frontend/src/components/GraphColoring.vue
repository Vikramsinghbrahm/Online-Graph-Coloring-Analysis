<template>
  <div class="container">
    <div class="form-container">
      <h1>Graph Coloring</h1>
      <form @submit.prevent="submitForm">
        <label for="chromatic-number">Chromatic Number:</label>
        <input type="number" v-model="chromaticNumber" required />

        <label for="number-of-vertices">Number of Vertices:</label>
        <input type="number" v-model="numberOfVertices" required />

        <label for="number-of-instances">Number of Instances:</label>
        <input type="number" v-model="numberOfInstances" required />

        <label for="coloring-method">Coloring Method:</label>
        <select v-model="coloringMethod" required>
          <option value="cbip">CBIP</option>
          <option value="firstfit">First Fit</option>
        </select>

        <button type="submit">Submit</button>
      </form>
    </div>
    <div class="result-container" v-if="average !== null">
      <h2>Average: {{ average }}</h2>
      <div class="center">
        <img
          v-if="image"
          :src="`http://localhost:5000/static/${image}`"
          alt="Graph Image"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      chromaticNumber: 0,
      numberOfVertices: 0,
      numberOfInstances: 0,
      coloringMethod: "cbip",
      average: null,
      image: null,
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await axios.post(
          "http://localhost:5000/api/graph-coloring",
          {
            chromaticNumber: this.chromaticNumber,
            numberOfVertices: this.numberOfVertices,
            numberOfInstances: this.numberOfInstances,
            coloringMethod: this.coloringMethod,
          }
        );
        this.average = response.data.average;
        this.image = response.data.image;
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
h2 {
  color: #42b983;
}
</style>
