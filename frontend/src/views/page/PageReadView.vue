<script lang="ts">
import api from "@/services/api";
import PageSidebarComponent from "@/components/page/PageSidebarComponent.vue";
import { RouterLink } from "vue-router";

export default {
  name: "PageReadView",
  props: {
    slug: {
      type: String,
      required: false,
      default: "_",
    },
    year: {
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
        '<i>Táto stránka nemá žiadny obsah. Kliknite na tlačidlo "Upraviť", aby ste mohli pridávať obsah.</i>',
      files: [],
    };
  },
  computed: {
    readableSlug() {
      if (this.slug === "_") {
        return `Ročník ${this.year}`;
      }
      return this.slug.replace(/[-_]/g, " ");
    },
  },
  async created() {
    await this.loadExistingFiles();
  },
  methods: {
    async loadExistingFiles() {
      try {
        const response = await api.get(`/page/${this.slug}/upload`);
        this.files = response.data;
      } catch (error) {
        console.error("Failed to load existing files:", error);
      }
    },
  },
};
</script>

<template>
  <div class="flex flex-col sm:flex-row">
    <PageSidebarComponent :year :slug />

    <article>
      <div class="top-container">
        <header>
          <h1 class="uppercase">{{ readableSlug }}</h1>
          <hr />
        </header>
        <div id="page-html" v-html="pageHtml"></div>
      </div>

      <footer>
        <div v-if="files.length > 0" class="files-container">
          <h2 class="big mb-2">Priložené súbory</h2>
          <div class="files-list">
            <div class="file-item" v-for="file in files" :key="file.name">
              <a
                :href="`/api/page/${slug}/upload/${file.name}`"
                target="_blank"
                >{{ file.name }}</a
              >
              <span class="text-sm text-gray-500">{{ file.size }} B</span>
            </div>
          </div>
        </div>

        <nav>
          <!-- TODO: iba ak je editor pre daný ročník alebo admin -->
          <RouterLink
            class="button button-green"
            :to="{ name: 'page-edit', params: { slug: slug } }"
          >
            Upraviť
          </RouterLink>
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

.files-container {
  @apply my-6 border border-gray-300 rounded-md p-4;
}

.files-list {
  @apply flex flex-col gap-2;
}

.files-list .file-item {
  @apply flex justify-between items-center;
}

.files-list .file-item a {
  @apply text-blue-500 hover:underline;
}
</style>
