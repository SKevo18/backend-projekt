<script lang="ts">
import { defineComponent, onMounted, watch } from "vue";
import { RouterLink } from "vue-router";
import { usePagesStore } from "@/store/pageStore";

export default defineComponent({
  name: "PageSidebarComponent",
  components: {
    RouterLink,
  },
  data() {
    return {
      pagesStore: usePagesStore(),
      year: "",
      categoryPages: [] as any[],
    };
  },
  methods: {
    async fetchSidebarPages() {
      this.year = this.$route.params.year as string;

      const category = this.pagesStore.categories.find(
        (cat) => cat.title === this.year
      );

      if (!category) {
        this.categoryPages = [];
        return;
      }

      this.categoryPages = this.pagesStore.pages.filter(
        (page) => page.category_id == category.id 
      );
    },
  },
  async mounted() {
    if (this.pagesStore.categories.length === 0) {
      await this.pagesStore.fetchCategories();
    }
    if (this.pagesStore.pages.length === 0) {
      await this.pagesStore.fetchPages();
    }

    await this.fetchSidebarPages();

    watch(
      () => this.$route.params.year,
      async () => {
        await this.fetchSidebarPages();
      }
    );
  },
});
</script>

<template>
  <aside class="sidebar">
    <ul>
      <li class="text-yellow-400 font-bold px-4 py-2 border-b border-gray-700">
        {{ year }}
      </li>
      <li v-for="page in categoryPages" :key="page.id">
        <RouterLink :to="{ name: 'page', params: { year, idSlug: `${page.id}-${page.slug}` } }" class="sidebar-link"
          active-class="sidebar-link-active">
          {{ page.title }}
        </RouterLink>
      </li>
    </ul>

    <RouterLink class="text-center my-4 block px-4 py-2 text-sm text-gray-400 hover:text-white"
      :to="{ name: 'admin-pages' }">
      Upraviť
    </RouterLink>
  </aside>
</template>

<style scoped>
@import "tailwindcss";

.sidebar {
  @apply bg-gray-800 text-white sm:w-[240px] text-center sm:text-left sm:h-[80vh] flex flex-col justify-between overflow-y-auto;
}

.sidebar .sidebar-link {
  @apply text-white block py-2 px-6 text-sm;
}

.sidebar .sidebar-link-active {
  @apply bg-gray-900 text-yellow-500;
}

.sidebar .sidebar-link:hover {
  @apply bg-gray-900;
}
</style>
