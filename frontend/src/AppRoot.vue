<script lang="ts">
import { RouterView } from "vue-router";
import HeaderComponent from "@/components/HeaderComponent.vue";

export default {
  name: "AppRoot",
  components: {
    HeaderComponent,
    RouterView,
  },
};
</script>

<template>
  <HeaderComponent />

  <main>
    <RouterView />
  </main>
</template>

<style>
@import "tailwindcss";

main > div {
  @apply flex flex-col sm:flex-row;
}
</style>
