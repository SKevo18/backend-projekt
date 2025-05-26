<script lang="ts">
import { defineComponent } from "vue";
import { usePagesStore } from "@/store/pageStore";
import PageSidebarComponent from "@/components/page/PageSidebarComponent.vue";

export default defineComponent({
  name: "CategoryRedirectView",
  components: {
    PageSidebarComponent,
  },
  props: {
    category: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      loading: true,
      info: "Loading...",
      categoryId: null as number | null,
      categoryTitle: "",
      pagesStore: usePagesStore(),
    };
  },
  async created() {
    await this.loadCategory();
  },
  watch: {
    category: {
      immediate: true,
      handler(newCategory) {
        this.loadCategory();
      },
    },
  },
  methods: {
    async loadCategory() {
      try {
        this.loading = true;
        this.categoryId = parseInt(this.category);

        if (isNaN(this.categoryId)) {
          this.loading = false;
          this.info = `Invalid category ID: "${this.categoryId}"`;
          return;
        }

        if (this.pagesStore.categories.length === 0) {
          await this.pagesStore.fetchCategories();
        }

        const foundCategory = this.pagesStore.categories.find(
          (cat) => cat.id === this.categoryId
        );

        if (!foundCategory) {
          this.loading = false;
          this.info = `Category with ID "${this.categoryId}" was not found.`;
          return;
        }

        this.categoryTitle = foundCategory.title;

        const pages = await this.pagesStore.fetchPages(this.categoryId);

        if (pages && pages.length > 0) {
          this.$router.replace(`/page/${pages[0].id}-${pages[0].slug}`);
        } else {
          this.loading = false;
          this.info = `Category "${this.categoryTitle}" has no pages.`;
        }
      } catch (error) {
        console.error("Error loading category:", error);
        this.loading = false;
        this.info = "There was an error loading the category.";
      }
    },
  },
});
</script>

<template>
  <div class="flex flex-col sm:flex-row">
    <PageSidebarComponent :activeCategoryId="categoryId" />

    <div class="flex-1 p-8 flex items-center justify-center">
      <div class="text-center">
        <div v-if="loading" class="spinner mb-4"></div>
        <p>{{ info }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import "tailwindcss";

.spinner {
  @apply w-8 h-8 border-4 border-gray-300 border-t-green-600 rounded-full mx-auto;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
