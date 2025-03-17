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
    },
    logout() {
      this.$authStore.logout();
      this.$router.push("/login");
    },
  },
  mounted() {
    this.getLinks();
  },
};
</script>

<template>
  <header>
    <div class="header-topnav" v-if="!$authStore.isAuthenticated">
      <RouterLink :to="{ name: 'login' }" active-class="nav-link-active"
        >Prihlásiť sa</RouterLink
      >
      <span> | </span>
      <RouterLink :to="{ name: 'register' }" active-class="nav-link-active"
        >Registrácia</RouterLink
      >
    </div>
    <div class="header-topnav" v-else>
      <RouterLink
        :to="{ name: 'admin-settings' }"
        active-class="nav-link-active"
        >Administrácia</RouterLink
      >
      <span> | </span>
      <a class="logout-link" @click="logout">Odhlásiť sa</a>
    </div>

    <div class="header-content">
      <LogoComponent />
      <nav class="year-nav">
        <RouterLink
          v-for="link in links"
          :key="link.id"
          :to="link.href"
          class="nav-link"
          active-class="nav-link-active"
        >
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

.header-topnav a {
  @apply text-gray-200;
}

.header-topnav .logout-link {
  @apply cursor-pointer hover:text-red-400;
}

.header-content {
  @apply bg-green-800 flex flex-col sm:flex-row justify-between items-center px-10 space-x-4;
}

.year-nav {
  @apply text-white p-4 flex flex-row gap-6 overflow-x-auto;
}

/* higher specificity, so it takes precedence */
a.nav-link-active {
  @apply text-yellow-500;
}

.year-nav .nav-link {
  @apply text-white text-center;
}

.year-nav .nav-link:hover {
  @apply text-yellow-500;
}
</style>
