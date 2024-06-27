<template>
  <div class="content center">
    <h1>Welcome to the Graph Coloring Analysis Tool</h1>
    <p>
      This tool provides a comprehensive environment for analyzing and
      experimenting with various graph coloring algorithms. Graph coloring is a
      fundamental topic in graph theory and computer science, where the
      objective is to assign colors to the vertices of a graph such that no two
      adjacent vertices share the same color. This problem has significant
      applications in scheduling, register allocation in compilers, and network
      coloring.
    </p>
    <p>Our Graph Coloring Analysis Tool offers the following features:</p>
    <ul>
      <li>
        <strong>Chromatic Number Calculation:</strong> Determine the minimum
        number of colors required to color a graph.
      </li>
      <li>
        <strong>Random Graph Generation:</strong> Create random graphs with a
        specified number of vertices and edges to test different algorithms.
      </li>
      <li>
        <strong>Algorithm Selection:</strong> Choose from multiple graph
        coloring algorithms, including CBIP (Coloring by Iterative Partitioning)
        and the First Fit algorithm.
      </li>
      <li>
        <strong>Visualization:</strong> Visualize the colored graph to
        understand how the algorithm performs on different types of graphs.
      </li>
      <li>
        <strong>Performance Metrics:</strong> Analyze the performance of
        different algorithms in terms of the number of colors used and the time
        taken for computation.
      </li>
    </ul>
    <p>
      This tool is designed for both educational purposes and practical
      applications. Students, researchers, and professionals can use it to gain
      insights into graph coloring techniques, compare the efficiency of various
      algorithms, and apply these techniques to real-world problems.
    </p>
    <p>
      We hope you find this tool useful and informative. Please explore the
      features and feel free to provide feedback for further improvements.
    </p>
    <router-link to="/graph-coloring"
      ><button>Go to Graph Coloring</button></router-link
    >
  </div>
</template>

<script>
export default {
  name: "LandingPage",
};
</script>

<style scoped>
/* Scoped styles for LandingPage */
p {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 20px;
}

ul {
  text-align: left;
  margin-bottom: 20px;
}

li {
  font-size: 1.1rem;
  margin-bottom: 10px;
}

button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 5px;
}

button:hover {
  background-color: #369f7c;
}
</style>
