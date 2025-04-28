<script lang="ts">
import { defineComponent, ref, onBeforeRouteUpdate } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "@/store/authStore";
import { usePagesStore } from "@/store/pageStore";
import PageSidebarComponent from "@/components/page/PageSidebarComponent.vue";
import api from "@/services/api";

export default defineComponent({
  name: "PageReadView",
  components: {
    PageSidebarComponent,
  },
  props: {
    idSlug: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const pagesStore = usePagesStore();
    const authStore = useAuthStore();
    const route = useRoute();
    
    // Состояния компонента
    const slug = ref("");
    const categoryId = ref<number | null>(null);
    const pageHtml = ref("<i>Loading page...</i>");
    const files = ref<any[]>([]);
    const title = ref("");
    const pageFound = ref(false);
    const pageId = ref<number | null>(null);
    const apiUrl = api.defaults.baseURL;
    const canEdit = ref(false);
    const isLoading = ref(true);

    // Загрузка страницы
    const loadPage = async (idSlug: string) => {
      isLoading.value = true;
      pageFound.value = false;
      canEdit.value = false;

      try {
        const id = parseInt(idSlug.split("-")[0]);
        if (isNaN(id)) {
          pageHtml.value = "<i>Invalid page ID.</i>";
          return;
        }

        pageId.value = id;
        const page = await pagesStore.fetchPageById(pageId.value);

        pageFound.value = true;
        slug.value = page.slug;
        pageHtml.value = page?.html_content || "<i>The page has no content.</i>";
        title.value = page?.title || "";
        categoryId.value = page?.category_id || null;

        if (authStore.isAuthenticated) {
          canEdit.value = await checkEditPermission();
        }
      } catch (error) {
        console.error("Error loading page:", error);
        pageHtml.value = "<i>Page not found.</i>";
        categoryId.value = null;
      } finally {
        isLoading.value = false;
      }

      await loadExistingFiles();
    };

    // Проверка прав на редактирование
    const checkEditPermission = async (): Promise<boolean> => {
      if (!authStore.user || !pageId.value || !categoryId.value) {
        return false;
      }

      if (authStore.user.role === 2) {
        return true;
      }

      if (authStore.user.role === 0) {
        return false;
      }

      try {
        const pageResponse = await api.get(
          `/permissions/${authStore.user.id}/pages/${pageId.value}`
        );
        if (pageResponse.data.has_permission) {
          return true;
        }

        const categoryResponse = await api.get(
          `/permissions/${authStore.user.id}/categories/${categoryId.value}`
        );
        return categoryResponse.data.has_permission;
      } catch (error) {
        console.error("Error checking permissions:", error);
        return false;
      }
    };

    // Загрузка существующих файлов
    const loadExistingFiles = async () => {
      if (!pageId.value) return;

      try {
        const response = await api.get(`/page/${pageId.value}/upload/`);
        files.value = response.data;
      } catch (error) {
        console.error("Error loading files:", error);
        files.value = [];
      }
    };

    // Обновление данных при изменении маршрута
    onBeforeRouteUpdate((to) => {
      const idSlug = to.params.idSlug as string;
      loadPage(idSlug); // Загружаем новую страницу при изменении маршрута
    });

    // Инициализация компонента при первом рендере
    loadPage(props.idSlug);

    return {
      slug,
      categoryId,
      pageHtml,
      files,
      title,
      pageFound,
      pageId,
      apiUrl,
      canEdit,
      isLoading,
    };
  },
});
</script>

<template>
  <div >
    <PageSidebarComponent :activeCategoryId="categoryId" />

    <div class="page-content">
      <div v-if="isLoading" class="loading-indicator">
        Loading...
      </div>

      <template v-else>
        <div v-if="!pageFound" class="error-message">
          Page not found
        </div>

        <template v-else>
          <article class="page-article">
            <header>
              <h1>{{ title }}</h1>
              <hr />
            </header>

            <div class="page-html-content" v-html="pageHtml"></div>
          </article>

          <footer class="page-footer">
            <div v-if="files.length > 0" class="attached-files">
              <h2>Attached Files</h2>
              <ul class="files-list">
                <li v-for="file in files" :key="file.name" class="file-item">
                  <a :href="`${apiUrl}/page/${pageId}/upload/${file.name}`" target="_blank" class="file-link">
                    {{ file.name }}
                  </a>
                  <span class="file-size">{{ file.size }} B</span>
                </li>
              </ul>
            </div>

            <div v-if="authStore.isAuthenticated && !canEdit" class="read-only-notice">
              You have read-only access to this page
            </div>

            <router-link v-if="pageFound && canEdit"
              :to="{ name: 'page-edit', params: { idSlug: `${pageId}-${slug}` } }" class="edit-button">
              Edit Page
            </router-link>
          </footer>
        </template>
      </template>
    </div>
  </div>
</template>

<style scoped lang="postcss">
.page-read-view {
  @apply flex flex-col md:flex-row min-h-screen;
}

.page-content {
  @apply flex-1 p-6;
}

.loading-indicator {
  @apply text-center py-8 text-gray-500;
}

.error-message {
  @apply text-red-500 text-lg p-4;
}

.page-article {
  @apply mb-8;
}

.page-article header {
  @apply mb-6;
}

.page-article header h1 {
  @apply text-2xl font-bold;
}

.page-html-content {
  @apply prose max-w-none;
}

.page-footer {
  @apply mt-8;
}

.attached-files {
  @apply mb-6 border border-gray-200 rounded-lg p-4;
}

.attached-files h2 {
  @apply text-lg font-semibold mb-3;
}

.files-list {
  @apply space-y-2;
}

.file-item {
  @apply flex justify-between items-center py-2;
}

.file-link {
  @apply text-blue-600 hover:underline;
}

.file-size {
  @apply text-sm text-gray-500;
}

.read-only-notice {
  @apply bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4;
}

.edit-button {
  @apply inline-block bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg;
}

.page-html-content table {
  @apply w-full my-4 border-collapse;
}

.page-html-content table td,
.page-html-content table th {
  @apply border border-gray-300 p-2;
}

.page-html-content table th {
  @apply bg-gray-100;
}

.page-html-content img {
  @apply max-w-full h-auto my-2;
}
</style>
