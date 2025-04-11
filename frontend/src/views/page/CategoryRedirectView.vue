<script lang="ts">
import { usePagesStore } from "@/store/pageStore";

export default {
  name: "CategoryRedirectView",
  props: {
    category: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      info: "Redirecting...",
    };
  },
  async created() {
    const categoryId = parseInt(this.category);
    const firstPageInCategory = await usePagesStore().fetchPages(categoryId)[0];

    if (firstPageInCategory) {
      this.$router.replace(`/page/${firstPageInCategory.id}`);
    } else {
      this.info =
        "No pages found in this category. Redirecting to home page...";
    }
  },
};
</script>

<template>
  <PageSidebarComponent :activeCategoryId="categoryId" />

  <div class="text-center my-10">{{ info }}</div>
</template>
