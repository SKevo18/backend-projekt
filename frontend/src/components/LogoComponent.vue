<script lang="ts">
import { RouterLink } from "vue-router";

export default {
  name: "LogoComponent",
  components: {
    RouterLink,
  },
};
</script>

<template>
  <RouterLink to="/" tabindex="-1">
    <img src="/logo.png" class="logo" alt="Animal Science Days Logo" />
  </RouterLink>
</template>

<style scoped>
@import "tailwindcss";

.logo {
  @apply w-20 h-20;
}
</style>
