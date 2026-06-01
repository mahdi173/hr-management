import { createApp } from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import { createPinia } from "pinia";
import router from "./router";
import { MotionPlugin } from "@vueuse/motion";

const app = createApp(App);

app.use(vuetify);
app.use(createPinia());
app.use(router);
app.use(MotionPlugin);

app.mount("#app");
