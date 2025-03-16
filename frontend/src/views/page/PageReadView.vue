<script lang="ts">
import PageSidebarComponent from "@/components/page/PageSidebarComponent.vue";
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
        '<i>Táto stránka nemá žiadny obsah. Kliknite na tlačidlo "Upraviť" na stránke, aby ste mohli pridávať obsah.</i>',
    };
  },
};
</script>

<template>
  <div class="flex flex-col sm:flex-row">
    <PageSidebarComponent :slug="slug" />

    <article>
      <header>
        <nav>
          <RouterLink
            class="button button-green"
            :to="{ name: 'page-edit', params: { slug: slug } }"
            >Upraviť</RouterLink
          >
        </nav>

        <h1>{{ slug }}</h1>
        <hr />
      </header>

      <div id="page-html" v-html="pageHtml"></div>
    </article>
  </div>
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
