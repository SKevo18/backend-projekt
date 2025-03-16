<script lang="ts">
export default {
  name: "NotFoundView",
};
</script>

<template>
  <div class="not-found-container">
    <h1 class="title mb-2">404 - Stránka nenájdená</h1>
    <p>Stránka ktorú hľadáte neexistuje.</p>
    <RouterLink to="/">Vrátiť sa domov</RouterLink>
  </div>
</template>

<style scoped>
@import "tailwindcss";

.not-found-container {
  @apply flex flex-col items-center justify-center h-[70vh];
}
</style>
