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
  computed: {
    readableSlug() {
      return this.slug.replace(/[-_]/g, " ");
    },
  },
};
</script>

<template>
  <div class="flex flex-col sm:flex-row">
    <PageSidebarComponent :slug="slug" />

    <article>
      <div class="top-container">
        <header>
          <h1>{{ readableSlug }}</h1>
          <hr />
        </header>
        <div id="page-html" v-html="pageHtml"></div>
      </div>

      <footer>
        <nav>
          <RouterLink
            class="button button-green"
            :to="{ name: 'page-edit', params: { slug: slug } }"
            >Upraviť</RouterLink
          >
        </nav>
      </footer>
    </article>
  </div>
</template>

<style scoped>
@import "tailwindcss";

#page-html {
  @apply h-full;
}

article nav {
  @apply flex justify-end mb-4 items-center;
}

article header {
  @apply mb-4;
}

article header h1 {
  @apply text-2xl font-bold uppercase;
}

article {
  @apply w-full p-8 flex flex-col justify-between;
}
</style>
