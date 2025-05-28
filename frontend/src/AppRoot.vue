<script lang="ts">
import { RouterView } from "vue-router";
import HeaderComponent from "@/components/HeaderComponent.vue";
import FooterComponent from "@/components/FooterComponent.vue";

export default {
  name: "AppRoot",
  components: {
    HeaderComponent,
    RouterView,
    FooterComponent,
  },
};
</script>

<template>
  <div class="app-container">
    <HeaderComponent />
    <main class="main-content">
      <RouterView />
    </main>
    <FooterComponent />
  </div>
</template>

<style scoped>
.app-container {
  @apply flex flex-col min-h-screen;
}
</style>
