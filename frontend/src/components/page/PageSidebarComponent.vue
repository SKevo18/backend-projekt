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
      required: false,
      default: null,
    },
  },
  data() {
    return {
      pagesStore: usePagesStore(),
      categoryPagesMap: {} as Record<number, any[]>,
      isLoading: true,
    };
  },
  computed: {
    categories() {
      return this.pagesStore.categories;
    },
  },
  methods: {
    async fetchAllCategoryPages() {
      this.isLoading = true;
      for (const category of this.categories) {
        this.categoryPagesMap[category.id] = await this.pagesStore.fetchPages(
          category.id
        );
      }
      this.isLoading = false;
    },
  },
  async mounted() {
    if (this.pagesStore.categories.length === 0) {
      await this.pagesStore.fetchCategories();
    }

    await this.fetchAllCategoryPages();
  },
  watch: {
    activeCategoryId: {
      immediate: true,
      handler(newId) {
        if (this.categories.length > 0) {
          if (newId && !this.categoryPagesMap[newId]) {
            this.pagesStore.fetchPages(newId).then((pages) => {
              this.categoryPagesMap[newId] = pages;
            });
          }
        }
      },
    },
  },
});
</script>

<template>
  <aside class="sidebar">
    <div class="categories-list">
      <div
        v-for="category in categories"
        :key="category.id"
        class="category-item"
      >
        <RouterLink
          :to="{ name: 'category', params: { category: category.id } }"
          class="category-link"
          :class="{ 'category-link-active': category.id === activeCategoryId }"
        >
          {{ category.title }}
        </RouterLink>

        <ul
          v-if="categoryPagesMap[category.id]?.length > 0"
          class="pages-list"
          :class="{ 'active-category': category.id === activeCategoryId }"
        >
          <li v-for="page in categoryPagesMap[category.id]" :key="page.id">
            <RouterLink
              :to="{ name: 'page', params: { idSlug: page.id + '-' + page.slug } }"
              class="sidebar-link"
              active-class="sidebar-link-active"
            >
              {{ page.title }}
            </RouterLink>
          </li>
        </ul>
        <div
          v-else-if="isLoading && category.id === activeCategoryId"
          class="p-2 text-center text-xs text-gray-400"
        >
          Načítavam...
        </div>
        <div
          v-else-if="category.id === activeCategoryId"
          class="p-2 text-center text-xs text-gray-400"
        >
          Žiadne stránky
        </div>
      </div>
    </div>

    <RouterLink
      class="text-center my-4 block px-4 py-2 text-sm text-gray-400 hover:text-white"
      :to="{ name: 'admin-pages' }"
    >
      Upraviť
    </RouterLink>
  </aside>
</template>

<style scoped>
@import "tailwindcss";

.sidebar {
  @apply bg-gray-800 text-white sm:w-[240px] text-center sm:text-left sm:h-[80vh] flex flex-col justify-between overflow-y-auto;
}

.categories-list {
  @apply flex flex-col;
}

.category-item {
  @apply border-b border-gray-700;
}

.category-link {
  @apply block py-2 px-4 font-medium text-gray-200;
}

.category-link:hover {
  @apply bg-gray-700 text-white;
}

.category-link-active {
  @apply bg-gray-900 text-yellow-400 font-bold;
}

.pages-list {
  @apply bg-gray-700;
}

.pages-list.active-category {
  @apply bg-gray-900;
}

.sidebar .sidebar-link {
  @apply text-white block py-2 px-6 text-sm pl-8;
}

.sidebar .sidebar-link-active {
  @apply bg-gray-800 text-yellow-500;
}

.sidebar .sidebar-link:hover {
  @apply bg-gray-700;
}
</style>
