<script lang="ts">
export default {
  name: "AdminView",
};
</script>

<template>
  <div class="p-6">
    <div class="mb-0">
      <nav class="tab-nav">
        <RouterLink
          :to="{ name: 'admin-settings' }"
          class="tab-link"
          active-class="tab-active"
        >
          Nastavenia
        </RouterLink>
        <RouterLink
          :to="{ name: 'admin-users' }"
          class="tab-link"
          active-class="tab-active"
        >
          Používatelia
        </RouterLink>
        <RouterLink
          :to="{ name: 'admin-pages' }"
          class="tab-link"
          active-class="tab-active"
        >
          Stránky
        </RouterLink>
      </nav>
    </div>

    <div class="tab-content">
      <RouterView />
    </div>
  </div>
</template>

<style>
@import "tailwindcss";

.tab-nav {
  @apply flex border-b border-gray-400;
}

.tab-content {
  @apply border border-t-0 border-gray-400 rounded-b-md p-4;
}

.tab-link {
  @apply relative px-4 py-2 text-gray-600 hover:text-gray-800;
}

.tab-active {
  @apply bg-white border-t border-l border-r border-gray-400 rounded-t-md text-gray-900 font-bold -mb-px;
}
</style>
