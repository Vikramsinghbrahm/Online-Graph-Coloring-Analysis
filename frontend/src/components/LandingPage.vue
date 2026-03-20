<template>
  <section class="landing">
    <div class="banner-panel">
      <p class="eyebrow">Algorithms • Systems Thinking • Reproducible Experiments</p>
      <h1 class="banner-title">Online graph coloring analysis for reproducible algorithm experiments.</h1>
      <p class="banner-copy">
        This workspace compares online coloring strategies on randomly generated
        k-partite graphs, exposes the results through a documented Flask API,
        and presents each run in a clean experimental dashboard.
      </p>
      <div class="banner-actions">
        <router-link to="/graph-coloring" class="button-primary">Open Workbench</router-link>
        <a
          href="https://en.wikipedia.org/wiki/Graph_coloring"
          class="button-secondary"
          target="_blank"
          rel="noreferrer"
        >
          Graph Coloring Context
        </a>
      </div>
    </div>

    <div class="panel-grid">
      <article class="info-card">
        <p class="card-kicker">Why it matters</p>
        <h2>Reliable algorithm tooling needs more than code that produces output.</h2>
        <p>
          This refactor emphasizes architecture, validation, testing,
          experiment reproducibility, and maintainability so the project can
          support analysis, iteration, and review with confidence.
        </p>
      </article>

      <article class="info-card">
        <p class="card-kicker">Algorithms</p>
        <ul class="feature-list">
          <li><strong>First Fit:</strong> a deterministic greedy baseline for online coloring.</li>
          <li><strong>CBIP:</strong> a bipartite-only strategy with explicit validation in the API.</li>
          <li><strong>Metrics:</strong> average color ratio, runtime, validity, and per-instance summaries.</li>
        </ul>
      </article>

      <article class="info-card">
        <p class="card-kicker">Engineering focus</p>
        <ul class="feature-list">
          <li>Clear separation between algorithm logic, experiment orchestration, and visualization.</li>
          <li>Structured validation to keep experimental inputs consistent with domain constraints.</li>
          <li>Reproducible runs and benchmark outputs for reliable comparison over time.</li>
        </ul>
      </article>
    </div>
  </section>
</template>

<script>
export default {
  name: "LandingPage",
};
</script>
