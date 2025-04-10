<script lang="ts">
import { defineComponent } from "vue";
import { usePagesStore } from "@/store/pageStore";
import PageSidebarComponent from "@/components/page/PageSidebarComponent.vue";
import { RouterLink, onBeforeRouteUpdate } from "vue-router";

export default defineComponent({
  name: "PageReadView",
  components: {
    PageSidebarComponent,
    RouterLink,
  },
  props: {
    year: {
      type: String,
      required: true,
    },
    idSlug: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      pagesStore: usePagesStore(),
      pageId: null as number | null,
      slug: "",
      pageHtml: "<i>Táto stránka nemá žiadny obsah.</i>",
      files: [] as any[],
      title: ""
    };
  },
  computed: {
    readableSlug(): string {
      return !this.slug || this.slug === "_"
        ? `Ročník ${this.year}`
        : this.slug.replace(/[-_]/g, " ");
    },
    fullIdSlug(): string {
      return this.pageId && this.slug ? `${this.pageId}-${this.slug}` : "_";
    },
  },  
  created() {
    this.loadPage(this.idSlug);

    onBeforeRouteUpdate((to, _from, next) => {
      const newIdSlug = to.params.idSlug as string;
      if (newIdSlug && newIdSlug !== this.fullIdSlug) {
        this.loadPage(newIdSlug);
      }
      next();
    });
  },
  methods: {
    async loadPage(idSlug: string) {
      const [idStr, ...slugParts] = idSlug.split("-");
      const parsedId = parseInt(idStr);
      const joinedSlug = slugParts.join("-");

      if (isNaN(parsedId) || !joinedSlug) {
        console.warn("Neplatný formát idSlug:", idSlug);
        return;
      }

      this.pageId = parsedId;
      this.slug = joinedSlug;

      try {
        const page = await this.pagesStore.fetchPageByIdSlug(parsedId);
        this.pageHtml = page?.html_content || "<i>Táto stránka nemá žiadny obsah.</i>";
        this.title = page?.title || "";
      } catch (error) {
        console.error("Nepodarilo sa načítať stránku:", error);
      }

      await this.loadExistingFiles();
    },

    async loadExistingFiles() {
      if (!this.pageId) return;

      try {
        const response = await fetch(`http://127.0.0.1:8000/api/page/${this.pageId}/upload/`);
        const contentType = response.headers.get("content-type") || "";

        if (!response.ok) {
          throw new Error(`Server response: ${response.status}`);
        }

        if (!contentType.includes("application/json")) {
          const text = await response.text();
          console.warn("Očakával sa JSON, ale server vrátil:", text);
          this.files = [];
          return;
        }

        const json = await response.json();
        this.files = Array.isArray(json) ? json : [];
      } catch (error) {
        console.error("Chyba pri načítaní súborov:", error);
        this.files = [];
      }
    }
  },
});
</script>

<template>
  <div class="flex flex-col sm:flex-row">
    <PageSidebarComponent :year="year" :slug="slug" />

    <article>
      <div class="top-container">
        <header>
          <h1 class="uppercase">{{ title }}</h1>
          <hr />
        </header>

        <div id="page-html" v-html="pageHtml"></div>
      </div>

      <footer>
        <div v-if="files.length > 0" class="files-container">
         <h2 class="big mb-2">Priložené súbory</h2>
          <div class="files-list">
            <div class="file-item" v-for="file in files" :key="file.name">
              <a :href="`/api/page/${pageId}/upload/${file.name}`" target="_blank">
                {{ file.name }}
              </a>
              <span class="text-sm text-gray-500">{{ file.size }} B</span>
            </div>
          </div>
        </div>

        <nav>
          <RouterLink class="button button-green" :to="{ name: 'page-edit', params: { year, idSlug: fullIdSlug } }">
            Upraviť stránku
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
