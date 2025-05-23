<script lang="ts">
import { defineComponent } from "vue";
import { RouterLink } from "vue-router";
import LogoComponent from "@/components/LogoComponent.vue";
import { usePagesStore } from "@/store/pageStore";

export default defineComponent({
  name: "HeaderComponent",
  components: {
    RouterLink,
    LogoComponent,
  },
  data() {
    return {
      pagesStore: usePagesStore(),
    };
  },
  methods: {
    logout() {
      this.$authStore.logout();
      this.$router.push("/login");
    },
  },
  async mounted() {
    if (this.pagesStore.categories.length === 0) {
      await this.pagesStore.fetchCategories();
    }
  },
});
</script>

<template>
  <header>
    <div class="header-topnav" v-if="!$authStore.isAuthenticated">
      <RouterLink :to="{ name: 'login' }" active-class="nav-link-active"
        >Login</RouterLink
      >
      <span class="mx-2">|</span>
      <RouterLink :to="{ name: 'register' }" active-class="nav-link-active"
        >Register</RouterLink
      >
    </div>

    <div class="header-topnav" v-else>
      <div class="inline-block" v-if="$authStore.isAdmin">
        <RouterLink
          :to="{ name: 'admin-settings' }"
          active-class="nav-link-active"
          >Administration</RouterLink
        >
        <span class="mx-2">|</span>
      </div>
      <RouterLink :to="{ name: 'profile' }" active-class="nav-link-active"
        >Profile</RouterLink
      >
      <span class="mx-2">|</span>
      <a class="logout-link" @click="logout">Logout</a>
    </div>

    <div class="header-content">
      <LogoComponent />
      <nav class="year-nav">
        <RouterLink
          v-for="category in sortedCategories"
          :key="category.id"
          :to="{ name: 'category', params: { category: category.title } }"
          class="nav-link"
          active-class="nav-link-active"
        >
          {{ category.title }}
        </RouterLink>
      </nav>
    </div>
  </header>
</template>

<style>
@import "tailwindcss";

.header-topnav {
  @apply text-right text-sm text-white bg-green-900 py-1 pr-4;
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

.year-nav a.nav-link-active {
  @apply text-yellow-500;
}

.year-nav .nav-link {
  @apply text-white text-center;
}

.year-nav .nav-link:hover {
  @apply text-yellow-500;
}
</style>
