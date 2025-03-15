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
  <RouterLink to="/">
    <img src="/logo.png" class="logo" alt="Animal Science Days Logo" />
  </RouterLink>
</template>

<style>
@import "tailwindcss";

.logo {
  @apply w-20 h-20;
}
</style>
