import { createApp } from "vue";
import AppRoot from "./AppRoot.vue";
import router from "./router";
import { createPinia } from "pinia";

const app = createApp(AppRoot);

app.use(router);
app.use(createPinia());
app.mount("#app");
