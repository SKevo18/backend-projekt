<script lang="ts">
import { defineComponent } from "vue";
import { RouterLink } from "vue-router";
import { usePagesStore } from "@/store/pageStore";
import { useAuthStore } from "@/store/authStore";

export default defineComponent({
  name: "PageSidebarComponent",
  components: {
    RouterLink,
  },
  props: {
    activeCategoryId: {
      type: Number as () => number | null,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      authStore: useAuthStore(),
      pagesStore: usePagesStore(),
    };
  },
  computed: {
    activeCategoryData() {
      if (this.activeCategoryId === null) return null;
      return this.pagesStore.pagesByCategory[this.activeCategoryId];
    },
    activeCategoryPages() {
      return this.activeCategoryData?.pages || [];
    },
    canLoadMore() {
      return (
        this.activeCategoryData?.hasMore && !this.activeCategoryData?.isLoading
      );
    },
    isLoadingPages() {
      return this.activeCategoryData?.isLoading;
    },
  },
  methods: {
    async loadPagesForActiveCategory(isLoadMore = false) {
      if (this.activeCategoryId === null) return;

      const currentPage = this.activeCategoryData?.currentPage || 0;
      const nextPage = isLoadMore ? currentPage + 1 : 1;

      await this.pagesStore.fetchPages(this.activeCategoryId, nextPage);
    },
    async ensureActiveCategoryPagesExist() {
      if (
        this.activeCategoryId !== null &&
        (!this.activeCategoryData ||
          this.activeCategoryData.pages.length === 0) &&
        !this.activeCategoryData?.isLoading
      ) {
        await this.loadPagesForActiveCategory();
      }
    },
  },
  watch: {
    activeCategoryId: {
      immediate: true,
      async handler(newId) {
        if (newId !== null) {
          await this.ensureActiveCategoryPagesExist();
        }
      },
    },
  },
});
</script>

<template>
  <aside class="sidebar">
    <div v-if="activeCategoryId !== null">
      <ul
        v-if="activeCategoryPages.length > 0"
        class="pages-list active-category"
      >
        <li v-for="page in activeCategoryPages" :key="page.id">
          <RouterLink
            :to="{
              name: 'page',
              params: { idSlug: page.id + '-' + page.slug },
            }"
            class="sidebar-link"
            active-class="sidebar-link-active"
          >
            {{ page.title }}
          </RouterLink>
        </li>
      </ul>
      <div
        v-if="isLoadingPages && activeCategoryPages.length === 0"
        class="p-2 text-center text-xs text-gray-400"
      >
        Loading pages...
      </div>
      <div
        v-else-if="!isLoadingPages && activeCategoryPages.length === 0"
        class="p-2 text-center text-xs text-gray-400"
      >
        No pages in this category.
      </div>

      <button
        v-if="canLoadMore"
        @click="loadPagesForActiveCategory(true)"
        class="w-full mt-2 px-4 py-2 text-sm text-gray-300 hover:bg-gray-700 hover:text-white focus:outline-none"
      >
        Load more...
      </button>
      <div
        v-if="isLoadingPages && activeCategoryPages.length > 0"
        class="p-2 text-center text-xs text-gray-400"
      >
        Loading more pages...
      </div>
    </div>
    <div v-else class="p-4 text-center text-gray-400">
      Select a category to see its pages.
    </div>

    <RouterLink
      v-if="authStore.isAdmin"
      class="text-center my-4 block px-4 py-2 text-sm text-gray-400 hover:text-white"
      :to="{ name: 'admin-pages' }"
    >
      Edit Pages
    </RouterLink>
  </aside>
</template>

<style scoped>
@import "tailwindcss";

.sidebar {
  @apply bg-gray-800 text-white sm:w-[240px] text-center sm:text-left sm:min-h-[calc(100vh-var(--header-height,64px))] flex flex-col justify-between overflow-y-auto;
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
