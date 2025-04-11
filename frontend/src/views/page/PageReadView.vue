<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { usePagesStore } from "@/store/pageStore";
import PageSidebarComponent from "@/components/page/PageSidebarComponent.vue";
import {
  RouterLink,
  useRoute,
  useRouter,
  onBeforeRouteUpdate,
} from "vue-router";
import api from "@/services/api";

export default defineComponent({
  name: "PageReadView",
  components: {
    PageSidebarComponent,
    RouterLink,
  },
  props: {
    idSlug: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();

    onBeforeRouteUpdate((to, from) => {
      if (to.params.idSlug !== from.params.idSlug) {
        const pageReadView =
          document.querySelector("#page-read-view")?.__vueParentComponent?.ctx;
        if (pageReadView) {
          pageReadView.loadPage(to.params.idSlug.toString());
        }
      }
    });

    return {};
  },
  data() {
    return {
      pagesStore: usePagesStore(),
      slug: "",
      categoryId: null as number | null,
      pageHtml: "<i>Stránka sa nenašla.</i>",
      files: [] as any[],
      title: "",
      pageFound: false,
      pageId: null as number | null,
    };
  },
  created() {
    this.loadPage(this.idSlug);
  },
  methods: {
    async loadPage(idSlug: string) {
      try {
        const id = parseInt(idSlug.split("-")[0]);
        if (isNaN(id)) {
          this.pageFound = false;
          this.pageHtml = "<i>Neplatné ID stránky.</i>";
          return;
        }

        this.pageId = id;
        const page = await this.pagesStore.fetchPageById(this.pageId);

        this.pageFound = true;
        this.slug = page.slug;
        this.pageHtml =
          page?.html_content || "<i>Stránka nemá žiadny obsah.</i>";
        this.title = page?.title || "";
        this.categoryId = page?.category_id || null;
      } catch (error) {
        this.pageFound = false;
        this.pageHtml = "<i>Stránka sa nenašla.</i>";
        this.categoryId = null;
      }

      await this.loadExistingFiles();
    },

    async loadExistingFiles() {
      if (!this.pageId) return;

      try {
        const response = await api.get(`/page/${this.pageId}/upload/`);
        this.files = response.data;
      } catch (error) {
        console.error("Chyba pri načítaní súborov:", error);
        this.files = [];
      }
    },
  },
});
</script>

<template>
  <div id="page-read-view" class="flex flex-col sm:flex-row">
    <PageSidebarComponent :activeCategoryId="categoryId" />

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
              <a
                :href="`/api/page/${pageId}/upload/${file.name}`"
                target="_blank"
              >
                {{ file.name }}
              </a>
              <span class="text-sm text-gray-500">{{ file.size }} B</span>
            </div>
          </div>
        </div>

        <nav>
          <RouterLink
            class="button button-green"
            :to="{ name: 'page-edit', params: { idSlug: `${pageId}-${slug}` } }"
            v-if="pageFound"
          >
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

<style>
@import "tailwindcss";

.ck-table-resized {
  @apply table-fixed my-2;
}

.ck-table-resized td,
.ck-table-resized th {
  @apply border-black border-1 p-1;
}
</style>
