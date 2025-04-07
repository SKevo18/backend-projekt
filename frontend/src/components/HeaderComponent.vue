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
  computed: {
    sortedCategories() {
      return [...this.pagesStore.categories].sort((a, b) => a.title.localeCompare(b.title));
    },
    pagesByCategory() {
      const map: Record<string, any[]> = {}; // napriklad ["PHP"] = [podstranka1, podstranka2]
      for (const page of this.pagesStore.pages) {
        const category = this.pagesStore.categories.find(c => c.id === page.category_id);
        if (category) {
          const title = category.title;
          if (!map[title]) map[title] = [];
          map[title].push(page);
        }
      }
      return map;
    },
  },
  methods: {
    logout() {
      this.$authStore.logout();
      this.$router.push("/login");
    },
    firstPageLink(categoryTitle: string) {
      const pages = this.pagesByCategory[categoryTitle]; // hovorime pozri sa do kategorii, ak su tam stranky - zobrazi to, ak nie - len kategoriu
      if (pages && pages.length > 0) {
        const page = pages[0];
        return { name: "page", params: { year: categoryTitle, idSlug: `${page.id}-${page.slug}` } };
      } else {
        return { name: "year", params: { year: categoryTitle } };
      }
    },
  },
  async mounted() {
    if (this.pagesStore.categories.length === 0) {
      await this.pagesStore.fetchCategories();
    }
    if (this.pagesStore.pages.length === 0) {
      await this.pagesStore.fetchPages();
    }
  },
}); 
</script>

<template>
  <header>
    <div class="header-topnav" v-if="!$authStore.isAuthenticated">
      <RouterLink :to="{ name: 'login' }" active-class="nav-link-active">Prihlásiť sa</RouterLink>
      <span> | </span>
      <RouterLink :to="{ name: 'register' }" active-class="nav-link-active">Registrácia</RouterLink>
    </div>

    <div class="header-topnav" v-else>
      <RouterLink :to="{ name: 'admin-settings' }" active-class="nav-link-active">Administrácia</RouterLink>
      <span> | </span>
      <a class="logout-link" @click="logout">Odhlásiť sa</a>
    </div>

    <div class="header-content">
      <LogoComponent />
      <nav class="year-nav">
        <RouterLink v-for="category in sortedCategories" :key="category.id" :to="firstPageLink(category.title)"
          class="nav-link" active-class="nav-link-active">
          {{ category.title }}
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
