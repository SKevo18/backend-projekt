import AppRoot from "@/AppRoot.vue";
import router from "@/router";
import { createApp } from "vue";
import { createPinia } from "pinia";

import { useAuthStore } from "@/store/authStore";

declare module "vue" {
  interface ComponentCustomProperties {
    $authStore: ReturnType<typeof useAuthStore>;
  }
}

const app = createApp(AppRoot);

app.use(createPinia());
app.config.globalProperties.$authStore = useAuthStore();
app.config.globalProperties.$authStore.loadSavedToken();
app.config.globalProperties.$authStore.fetchUserData();

app.use(router);
app.mount("#app");
