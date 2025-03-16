<script lang="ts">
export default {
  name: "AdminView",
};
</script>

<template>
  <div>
    <h1 class="title">Admin</h1>

    <nav>
      <RouterLink :to="{ name: 'admin-settings' }">Settings</RouterLink>
      <RouterLink :to="{ name: 'admin-users' }">Users</RouterLink>
      <RouterLink :to="{ name: 'admin-sidebar' }">Sidebar</RouterLink>
    </nav>

    <RouterView />
  </div>
</template>

<style scoped>
@import "tailwindcss";

nav {
  @apply flex gap-4 mx-auto w-fit;
}
</style>
