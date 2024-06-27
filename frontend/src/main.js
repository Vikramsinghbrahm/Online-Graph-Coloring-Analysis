import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { VuelidatePlugin } from "@vuelidate/core";
import "./assets/styles.css"; // Import global stylesheet

const app = createApp(App);
app.use(router);
app.use(VuelidatePlugin);
app.mount("#app");
