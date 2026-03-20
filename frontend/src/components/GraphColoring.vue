<template>
  <section class="workbench">
    <div class="section-heading">
      <div>
        <p class="eyebrow">Experiment Workbench</p>
        <h1>Run reproducible graph coloring experiments.</h1>
      </div>
      <p class="section-copy">
        Configure the graph family, choose an online algorithm, and compare
        color efficiency against the target chromatic number.
      </p>
    </div>

    <div class="workbench-grid">
      <article class="panel form-panel">
        <div class="panel-header">
          <div>
            <p class="card-kicker">Configuration</p>
            <h2>Experiment input</h2>
          </div>
          <span class="status-chip">{{ methodLabel }}</span>
        </div>

        <form class="experiment-form" @submit.prevent="submitForm">
          <label>
            <span>Coloring method</span>
            <select v-model="form.coloringMethod" @change="normalizeMethodSelection">
              <option value="first_fit">First Fit</option>
              <option value="cbip">CBIP</option>
            </select>
          </label>

          <label>
            <span>Target chromatic number</span>
            <input v-model.number="form.chromaticNumber" type="number" min="2" max="12" />
          </label>

          <label>
            <span>Vertices</span>
            <input v-model.number="form.numberOfVertices" type="number" min="2" max="150" />
          </label>

          <label>
            <span>Instances</span>
            <input v-model.number="form.numberOfInstances" type="number" min="1" max="100" />
          </label>

          <label>
            <span>Edge probability</span>
            <input v-model.number="form.edgeProbability" type="number" min="0" max="1" step="0.05" />
          </label>

          <label>
            <span>Seed</span>
            <input v-model.number="form.seed" type="number" min="0" placeholder="Optional but recommended" />
          </label>

          <p class="helper-copy">{{ methodDescription }}</p>

          <button type="submit" class="button-primary" :disabled="loading">
            {{ loading ? "Running experiment..." : "Run experiment" }}
          </button>
        </form>

        <div v-if="errorMessage" class="message-banner error-banner">
          {{ errorMessage }}
        </div>
      </article>

      <article class="panel insight-panel">
        <div class="panel-header">
          <div>
            <p class="card-kicker">Results</p>
            <h2>{{ result ? "Experiment summary" : "Ready for analysis" }}</h2>
          </div>
          <span class="status-chip" :class="{ success: result?.summary.valid_colorings }">
            {{ result ? validityLabel : "Awaiting run" }}
          </span>
        </div>

        <div v-if="result" class="results-stack">
          <div class="metrics-grid">
            <div class="metric-card">
              <p class="metric-label">Average ratio</p>
              <p class="metric-value">{{ result.summary.average_ratio }}</p>
            </div>
            <div class="metric-card">
              <p class="metric-label">Average colors</p>
              <p class="metric-value">{{ result.summary.average_colors_used }}</p>
            </div>
            <div class="metric-card">
              <p class="metric-label">Avg runtime</p>
              <p class="metric-value">{{ result.summary.average_runtime_ms }} ms</p>
            </div>
            <div class="metric-card">
              <p class="metric-label">Best / Worst</p>
              <p class="metric-value">{{ result.summary.best_ratio }} / {{ result.summary.worst_ratio }}</p>
            </div>
          </div>

          <div class="sample-card">
            <div>
              <p class="card-kicker">Sample graph</p>
              <h3>Representative visualization</h3>
              <p class="helper-copy">
                Seed {{ result.sample_graph.seed }} • {{ result.sample_graph.vertexCount }}
                vertices • {{ result.sample_graph.edgeCount }} edges
              </p>
            </div>
            <img :src="sampleGraphUrl" alt="Sample colored graph" class="graph-image" />
          </div>

          <div class="table-card">
            <div class="table-header">
              <div>
                <p class="card-kicker">Per-instance details</p>
                <h3>Reproducible experiment runs</h3>
              </div>
            </div>
            <div class="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Run</th>
                    <th>Seed</th>
                    <th>Colors</th>
                    <th>Ratio</th>
                    <th>Runtime</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="instance in result.instances" :key="instance.instance">
                    <td>{{ instance.instance }}</td>
                    <td>{{ instance.seed }}</td>
                    <td>{{ instance.colors_used }}</td>
                    <td>{{ instance.ratio }}</td>
                    <td>{{ instance.runtime_ms }} ms</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <p class="empty-state-title">No experiment has been run yet.</p>
          <p class="helper-copy">
            Start with the default settings to see how the greedy baseline
            behaves on a 3-partite graph family, then compare it with CBIP on
            bipartite inputs.
          </p>
        </div>
      </article>
    </div>
  </section>
</template>

<script>
import axios from "axios";
import { computed, reactive, ref } from "vue";
import { API_BASE_URL } from "../config";

export default {
  name: "GraphColoring",
  setup() {
    const form = reactive({
      chromaticNumber: 3,
      numberOfVertices: 24,
      numberOfInstances: 8,
      coloringMethod: "first_fit",
      edgeProbability: 0.35,
      seed: 42,
    });

    const loading = ref(false);
    const errorMessage = ref("");
    const result = ref(null);

    const methodLabel = computed(() =>
      form.coloringMethod === "cbip" ? "CBIP (bipartite only)" : "First Fit baseline"
    );

    const methodDescription = computed(() =>
      form.coloringMethod === "cbip"
        ? "CBIP is validated for bipartite graphs only, so the target chromatic number is locked to 2."
        : "First Fit is a deterministic online greedy algorithm that provides a clean baseline for color usage."
    );

    const validityLabel = computed(() =>
      result.value?.summary.valid_colorings ? "All colorings valid" : "Check failed"
    );

    const sampleGraphUrl = computed(() =>
      result.value ? `${API_BASE_URL}${result.value.sample_graph.imageUrl}` : ""
    );

    const normalizeMethodSelection = () => {
      if (form.coloringMethod === "cbip") {
        form.chromaticNumber = 2;
      }
    };

    const validateForm = () => {
      if (form.coloringMethod === "cbip" && Number(form.chromaticNumber) !== 2) {
        return "CBIP is only supported for bipartite graphs, so chromatic number must be 2.";
      }

      if (Number(form.numberOfVertices) < Number(form.chromaticNumber)) {
        return "The number of vertices must be at least the target chromatic number.";
      }

      if (Number(form.edgeProbability) < 0 || Number(form.edgeProbability) > 1) {
        return "Edge probability must be between 0 and 1.";
      }

      return "";
    };

    const submitForm = async () => {
      errorMessage.value = validateForm();
      if (errorMessage.value) {
        return;
      }

      loading.value = true;

      try {
        const response = await axios.post(`${API_BASE_URL}/api/experiments`, {
          chromaticNumber: Number(form.chromaticNumber),
          numberOfVertices: Number(form.numberOfVertices),
          numberOfInstances: Number(form.numberOfInstances),
          coloringMethod: form.coloringMethod,
          edgeProbability: Number(form.edgeProbability),
          seed: form.seed === "" || form.seed === null ? null : Number(form.seed),
        });

        result.value = response.data;
      } catch (error) {
        errorMessage.value =
          error.response?.data?.error ||
          "The experiment could not be completed. Check that the backend is running and try again.";
      } finally {
        loading.value = false;
      }
    };

    return {
      errorMessage,
      form,
      loading,
      methodDescription,
      methodLabel,
      normalizeMethodSelection,
      result,
      sampleGraphUrl,
      submitForm,
      validityLabel,
    };
  },
};
</script>
