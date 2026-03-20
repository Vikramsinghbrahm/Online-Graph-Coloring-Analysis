<template>
  <div class="app-shell">
    <header class="topbar">
      <router-link to="/" class="brand">OGCA</router-link>
      <nav class="topbar-links">
        <router-link to="/" class="topbar-link">Overview</router-link>
        <router-link to="/graph-coloring" class="topbar-link">Workbench</router-link>
      </nav>
    </header>
    <main class="page-shell">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>
