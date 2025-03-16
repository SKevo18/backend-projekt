import AppRoot from "@/AppRoot.vue";
import router from "@/router";
import { createApp } from "vue";
import { createPinia } from "pinia";
import { useUmoEditor } from "@umoteam/editor";

import umoSkTranslations from "@/umo-sk.json";
import { useAuthStore } from "@/store/authStore";

// type `authStore`
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

// UMO Editor
app.use(useUmoEditor, {
  locale: "ru-RU",
  translations: {
    ru_RU: umoSkTranslations,
  },
  document: {
    title: "",
    placeholder: {
      ru_RU: "Začni písať...",
    },
    enableMarkdown: false,
  },
});

app.mount("#app");
