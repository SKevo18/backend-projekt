<script lang="ts">
import { defineComponent } from "vue";
import { RouterLink } from "vue-router";
import { usePagesStore } from "@/store/pageStore";

export default defineComponent({
  name: "PageSidebarComponent",
  components: {
    RouterLink,
  },
  props: {
    activeCategoryId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      pagesStore: usePagesStore(),
      categoryPages: [] as any[],
    };
  },
  methods: {
    async fetchSidebarPages() {
      const activeCategory = this.pagesStore.categories.find(
        (cat) => cat.id === this.activeCategoryId
      );

      if (!activeCategory) {
        this.categoryPages = [];
        return;
      }

      this.categoryPages = this.pagesStore.fetchPages(activeCategory.id);
    },
  },
  async mounted() {
    if (this.pagesStore.categories.length === 0) {
      await this.pagesStore.fetchCategories();
    }

    await this.fetchSidebarPages();
  },
});
</script>

<template>
  <aside class="sidebar">
    <ul>
      <li class="text-yellow-400 font-bold px-4 py-2 border-b border-gray-700">
        {{ category }}
      </li>
      <li v-for="page in categoryPages" :key="page.id">
        <RouterLink :to="{ name: 'page', params: { slug: `${page.id}-${page.slug}` } }" class="sidebar-link"
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
