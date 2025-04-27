<script lang="ts">
import { defineComponent } from "vue";
import { useAuthStore } from "@/store/authStore";

export default defineComponent({
  name: "AdminView",
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
});
</script>

<template>
  <div class="p-6">
    <div v-if="!authStore.isAdmin" class="text-center p-8">
      <h1 class="text-xl font-bold">Access Denied</h1>
      <p>You don't have permission to view this page</p>
    </div>
    <template v-else>
      <div class="mb-0">
        <nav class="tab-nav">
          <RouterLink
            :to="{ name: 'admin-settings' }"
            class="tab-link"
            active-class="tab-active"
          >
            Settings
          </RouterLink>
          <RouterLink
            :to="{ name: 'admin-users' }"
            class="tab-link"
            active-class="tab-active"
          >
            Users
          </RouterLink>
          <RouterLink
            :to="{ name: 'admin-pages' }"
            class="tab-link"
            active-class="tab-active"
          >
            Pages
          </RouterLink>
        </nav>
      </div>

      <div class="tab-content">
        <RouterView />
      </div>
    </template>
  </div>
</template>

<style>
@import "tailwindcss";
@import "./admin_form.css";

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
