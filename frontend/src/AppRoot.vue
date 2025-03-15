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
  <HeaderComponent />

  <main>
    <RouterView />
  </main>

  <FooterComponent />
</template>

<style>
@import "tailwindcss";

#app {
  @apply h-screen;
}

main {
  @apply h-full;
}

main > div {
  @apply flex flex-col sm:flex-row h-full;
}
</style>
