<script lang="ts">
import PageSidebarComponent from "@/components/PageSidebarComponent.vue";
import { RouterLink } from "vue-router";

export default {
  name: "PageReadView",
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  components: {
    PageSidebarComponent,
  },
  data() {
    return {
      pageHtml:
        '<i>This page has no content. Click on the "Edit" button to add content.</i>',
    };
  },
};
</script>

<template>
  <PageSidebarComponent :slug="slug" />

  <article>
    <header>
      <nav>
        <RouterLink
          class="button"
          :to="{ name: 'page-edit', params: { slug: slug } }"
          >Edit</RouterLink
        >
      </nav>

      <h1>{{ slug }}</h1>
      <hr />
    </header>

    <div id="page-html" v-html="pageHtml"></div>
  </article>
</template>

<style>
@import "tailwindcss";

article header {
  @apply mb-4;
}

article header nav {
  @apply flex justify-end mb-4 items-center;
}

article h1 {
  @apply text-2xl font-bold uppercase;
}

article {
  @apply w-full p-8;
}
</style>
