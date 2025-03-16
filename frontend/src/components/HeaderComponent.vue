<script lang="ts">
import { RouterLink } from "vue-router";
import LogoComponent from "@/components/LogoComponent.vue";

export default {
  name: "HeaderComponent",
  components: {
    RouterLink,
    LogoComponent,
  },
  data() {
    return {
      // TODO: fetch year links from backend
      links: [{ id: 1, title: "Home", href: "/" }],
    };
  },
};
</script>

<template>
  <header>
    <div class="header-topnav" v-if="!$authStore.isAuthenticated">
      <RouterLink to="/login">Prihlásiť sa</RouterLink>
      <span> | </span>
      <RouterLink to="/register">Registrácia</RouterLink>
    </div>
    <div class="header-topnav" v-else>
      <a class="cursor-pointer" @click="$authStore.logout()">Logout</a>
    </div>

    <div class="header-content">
      <LogoComponent />
      <nav class="nav" v-for="link in links" :key="link.id">
        <RouterLink :to="link.href" class="nav-link">
          {{ link.title }}
        </RouterLink>
      </nav>
    </div>
  </header>
</template>

<style>
@import "tailwindcss";

.header-topnav {
  @apply text-right text-sm text-white bg-green-900 py-1 pr-4 space-x-2;
}

.header-topnav > a {
  @apply text-gray-200;
}

.header-content {
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
