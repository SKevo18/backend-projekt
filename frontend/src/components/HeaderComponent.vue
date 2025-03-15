<script lang="ts">
import { RouterLink } from "vue-router";
import LogoComponent from "@/components/LogoComponent.vue";

export default {
  name: "HeaderComponent",
  components: {
    RouterLink,
    LogoComponent,
  },
};
</script>

<template>
  <header>
    <LogoComponent />
    <nav class="nav">
      <RouterLink to="/" class="nav-link">Home</RouterLink>
      <RouterLink to="/login" class="nav-link">Login</RouterLink>
      <RouterLink to="/register" class="nav-link">Registration</RouterLink>
      <RouterLink to="/contact" class="nav-link">Contact</RouterLink>
      <RouterLink to="/text-editor" class="nav-link">Text-Editor</RouterLink>
    </nav>
  </header>
</template>

<style>
@import "tailwindcss";

header {
  @apply bg-green-800 flex flex-col sm:flex-row justify-between items-center px-10;
}

.nav {
  @apply text-white p-4 flex flex-row gap-6;
}

.nav-link {
  @apply text-white;
}

.nav-link:hover {
  @apply text-yellow-500;
}
</style>
