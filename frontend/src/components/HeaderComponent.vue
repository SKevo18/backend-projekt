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
      links: [],
    };
  },
  methods: {
    getLinks() {
      // TODO: fetch year links from backend
      for (let year = 2021; year <= 2025; year++) {
        this.links.push({
          id: year,
          title: `Ročník ${year}`,
          href: `/${year}`,
        });
      }
      return this.links;
    },
    logout() {
      this.$authStore.logout();
      this.$router.push("/login");
    },
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
      <a class="cursor-pointer" @click="logout">Odhlásiť sa</a>
    </div>

    <div class="header-content">
      <LogoComponent />
      <nav class="nav">
        <RouterLink
          v-for="link in getLinks()"
          :key="link.id"
          :to="link.href"
          class="nav-link"
        >
          {{ link.title }}
        </RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
@import "tailwindcss";

.header-topnav {
  @apply text-right text-sm text-white bg-green-900 py-1 pr-4 space-x-2;
}

.header-topnav > a {
  @apply text-gray-200;
}

.header-topnav > a.router-link-active {
  @apply text-yellow-500;
}

.header-content {
  @apply bg-green-800 flex flex-col sm:flex-row justify-between items-center px-10 space-x-4;
}

.nav {
  @apply text-white p-4 flex flex-row gap-6 overflow-x-auto;
}

.nav-link {
  @apply text-white text-center;
}

.nav-link.router-link-active {
  @apply text-yellow-500;
}

.nav-link:hover {
  @apply text-yellow-500;
}
</style>
