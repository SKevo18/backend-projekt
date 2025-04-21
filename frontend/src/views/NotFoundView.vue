<script lang="ts">
export default {
  name: "NotFoundView",
};
</script>

<template>
  <div class="not-found-container">
    <h1 class="title mb-2">404 - Page not found</h1>
    <p>The page you are looking for does not exist.</p>
    <RouterLink :to="{ name: 'home' }">Returning home</RouterLink>
  </div>
</template>

<style scoped>
@import "tailwindcss";

.not-found-container {
  @apply flex flex-col items-center justify-center h-[70vh];
}
</style>
