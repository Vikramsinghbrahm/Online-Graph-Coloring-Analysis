

# Graph Coloring Analysis Tool

Welcome to the Graph Coloring Analysis Tool! This tool provides a comprehensive environment for analyzing and experimenting with various graph coloring algorithms. Graph coloring is a fundamental topic in graph theory and computer science, where the objective is to assign colors to the vertices of a graph such that no two adjacent vertices share the same color. This problem has significant applications in scheduling, register allocation in compilers, and network coloring.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)

## Introduction

Graph coloring is a critical concept in computer science and discrete mathematics. It has numerous applications in real-world scenarios, such as:

- **Scheduling**: Assigning time slots or resources without conflicts.
- **Register Allocation**: Efficiently assigning variables to CPU registers in compiler design.
- **Network Coloring**: Frequency assignment in wireless networks to avoid interference.

This tool allows users to:

- Generate random graphs.
- Apply different graph coloring algorithms.
- Visualize the results.
- Analyze the performance of the algorithms.

## Features

### Chromatic Number Calculation

Determine the minimum number of colors required to color a graph without two adjacent vertices having the same color.

### Random Graph Generation

Create random graphs with a specified number of vertices and edges to test different algorithms.

### Algorithm Selection

Choose from multiple graph coloring algorithms, including:

- **CBIP (Coloring by Iterative Partitioning)**: An efficient algorithm for coloring bipartite graphs.
- **First Fit Algorithm**: A simple heuristic for graph coloring.

### Visualization

Visualize the colored graph to understand how the algorithm performs on different types of graphs.

### Performance Metrics

Analyze the performance of different algorithms in terms of the number of colors used and the time taken for computation.

## Installation

### Prerequisites

- Python 3.x
- Node.js and npm
- Git

### Backend Setup

1. **Clone the Repository**

   ```sh
   git clone https://github.com/yourusername/graph-coloring-analysis.git
   cd graph-coloring-analysis/backend
   ```

2. **Create a Virtual Environment**

   ```sh
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:

     ```sh
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```sh
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

5. **Run the Backend Server**

   ```sh
   python app.py
   ```

### Frontend Setup

1. **Navigate to the Frontend Directory**

   ```sh
   cd ../frontend
   ```

2. **Install Dependencies**

   ```sh
   npm install
   ```

3. **Run the Frontend Development Server**

   ```sh
   npm run serve
   ```

## Usage

1. **Start the Backend Server**

   ```sh
   cd backend
   python app.py
   ```

2. **Start the Frontend Development Server**

   ```sh
   cd frontend
   npm run serve
   ```

3. **Access the Application**

   Open your web browser and navigate to \`http://localhost:8080`.

## API Endpoints

### GET 

Renders the main page.

### POST /api/graph-coloring

Generates and colors a random graph based on the provided parameters.

**Request Body:**

```json
{
  "chromaticNumber": 3,
  "numberOfVertices": 10,
  "numberOfInstances": 1,
  "coloringMethod": "cbip"
}
```

**Response:**

```json
{
  "average": 1.0,
  "image": "graph_1633062802.png",
  "method": "cbip"
}
```

### GET /plot

Returns the generated plot image.

## Technologies Used

- **Backend:**
  - Flask
  - NetworkX
  - Matplotlib
  - Flask-CORS

- **Frontend:**
  - Vue.js
  - Axios
  - Vuelidate

## Contributing

Contributions are welcome! 

   Open a pull request from your fork's branch to the main repository's branch.
