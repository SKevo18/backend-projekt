<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch } from "vue";
import { usePagesStore } from "@/store/pageStore";
import { RouterLink } from "vue-router";

interface Page {
  id: number;
  title: string;
  slug: string;
  category_id: number;
}

interface Category {
  id: number;
  title: string;
}

export default defineComponent({
  name: "AdminPagesView",
  components: { RouterLink },
  setup() {
    const pagesStore = usePagesStore();

    const newPageTitle = ref("");
    const newPageSlug = ref("");
    const newPageSlugManuallyEdited = ref(false);
    const newPageCategoryId = ref<number | null>(null);
    const newPageHtmlContent = ref("");

    const newCategoryTitle = ref("");
    const showAddCategoryModal = ref(false);
    const showAddPageModal = ref(false);

    const editingPage = ref<Page | null>(null);
    const originalEditingPageCategoryId = ref<number | null>(null);
    const editingCategory = ref<Category | null>(null);

    const activeCategoryAccordion = ref<number | null>(null);

    const sortedCategories = computed(() =>
      [...pagesStore.categories].sort((a, b) => a.title.localeCompare(b.title))
    );

    const getPagesForCategory = (categoryId: number) => {
      const categoryData = pagesStore.pagesByCategory[categoryId];
      if (!categoryData || !categoryData.pages) return [];
      return [...categoryData.pages].sort((a, b) =>
        a.title.localeCompare(b.title)
      );
    };

    watch(newPageTitle, (title) => {
      if (!newPageSlugManuallyEdited.value) {
        newPageSlug.value = generateSlug(title);
      }
    });

    const generateSlug = (text: string) => {
      return text
        .toLowerCase()
        .replace(/\s+/g, "-")
        .replace(/[^\w\-]+/g, "")
        .replace(/\-\-+/g, "-")
        .trim();
    };

    const handleAddCategory = async () => {
      if (!newCategoryTitle.value.trim()) {
        alert("Category title cannot be empty.");
        return;
      }
      try {
        await pagesStore.addCategory(newCategoryTitle.value);
        newCategoryTitle.value = "";
        showAddCategoryModal.value = false;
      } catch (error) {
        console.error("Error adding category:", error);
        alert("Failed to add category. Check console for details.");
      }
    };

    const openEditCategoryModal = (category: Category) => {
      editingCategory.value = { ...category }; // mutable copy
    };

    const handleUpdateCategory = async () => {
      if (!editingCategory.value || !editingCategory.value.title.trim()) {
        alert("Category title cannot be empty.");
        return;
      }
      try {
        await pagesStore.updateCategory(editingCategory.value.id, {
          title: editingCategory.value.title,
        });
        editingCategory.value = null;
      } catch (error) {
        console.error("Error updating category:", error);
        alert("Failed to update category.");
      }
    };

    const handleDeleteCategory = async (category: Category) => {
      if (
        confirm(
          `Delete category "${category.title}" and all its pages? This cannot be undone.`
        )
      ) {
        try {
          await pagesStore.deleteCategory(category);
        } catch (error) {
          console.error("Error deleting category:", error);
          alert("Failed to delete category.");
        }
      }
    };

    const openAddPageModal = (categoryId: number) => {
      newPageCategoryId.value = categoryId;
      newPageTitle.value = "";
      newPageSlug.value = "";
      newPageHtmlContent.value = "";
      newPageSlugManuallyEdited.value = false;
      showAddPageModal.value = true;
    };

    const handleAddPage = async () => {
      if (
        !newPageTitle.value.trim() ||
        !newPageSlug.value.trim() ||
        newPageCategoryId.value === null
      ) {
        alert("Page title, slug, and category are required.");
        return;
      }
      try {
        await pagesStore.addPage(
          newPageCategoryId.value,
          newPageTitle.value,
          newPageHtmlContent.value,
          newPageSlug.value
        );
        showAddPageModal.value = false;
      } catch (error) {
        console.error("Error adding page:", error);
        // @ts-ignore
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          // @ts-ignore
          alert(`Failed to add page: ${error.response.data.detail}`);
        } else {
          alert(
            "Failed to add page. Slug might already exist or other server error."
          );
        }
      }
    };

    const openEditPageModal = (page: Page) => {
      editingPage.value = { ...page }; // mutable copy
      originalEditingPageCategoryId.value = page.category_id;
    };

    const handleUpdatePageDetails = async () => {
      if (
        !editingPage.value ||
        !editingPage.value.title.trim() ||
        !editingPage.value.slug.trim()
      ) {
        alert("Page title and slug cannot be empty.");
        return;
      }
      try {
        const pageDetailsToUpdate = {
          title: editingPage.value.title,
          slug: editingPage.value.slug,
          category_id: editingPage.value.category_id,
        };
        const pageIdBeingUpdated = editingPage.value.id;
        const newCategoryId = editingPage.value.category_id;
        const oldCategoryId = originalEditingPageCategoryId.value;

        await pagesStore.updatePage(pageIdBeingUpdated, pageDetailsToUpdate);

        editingPage.value = null;
        originalEditingPageCategoryId.value = null;

        if (oldCategoryId !== null && newCategoryId !== oldCategoryId) {
          await pagesStore.fetchPages(oldCategoryId, 1);
        }
        await pagesStore.fetchPages(newCategoryId, 1);
      } catch (error) {
        console.error("Error updating page details:", error);
        alert(
          `Failed to update page details: ${error.response.data.detail || error.message || "Unknown error"}`
        );
      }
    };

    const handleDeletePage = async (page: Page) => {
      if (confirm(`Delete page "${page.title}"? This cannot be undone.`)) {
        try {
          await pagesStore.deletePage(page);
        } catch (error) {
          console.error("Error deleting page:", error);
          alert("Failed to delete page.");
        }
      }
    };

    const toggleAccordion = (categoryId: number) => {
      activeCategoryAccordion.value =
        activeCategoryAccordion.value === categoryId ? null : categoryId;
      if (
        activeCategoryAccordion.value === categoryId &&
        (!pagesStore.pagesByCategory[categoryId] ||
          pagesStore.pagesByCategory[categoryId].pages.length === 0) &&
        !pagesStore.pagesByCategory[categoryId]?.isLoading
      ) {
        pagesStore.fetchPages(categoryId, 1);
      }
    };

    const loadAllPagesAdmin = async () => {
      for (const category of sortedCategories.value) {
        if (
          !pagesStore.pagesByCategory[category.id] ||
          pagesStore.pagesByCategory[category.id].pages.length === 0
        ) {
          await pagesStore.fetchPages(category.id, 1);
        }
      }
    };

    onMounted(async () => {
      if (pagesStore.categories.length === 0) {
        await pagesStore.fetchCategories();
      }
      watch(
        sortedCategories,
        async (newCats) => {
          if (newCats.length > 0) {
            let needsLoad = false;
            for (const cat of newCats) {
              if (
                !pagesStore.pagesByCategory[cat.id] ||
                pagesStore.pagesByCategory[cat.id].pages.length === 0
              ) {
                needsLoad = true;
                break;
              }
            }
            if (needsLoad) {
              await loadAllPagesAdmin();
            }
          }
        },
        { immediate: true }
      );
    });

    watch(
      () => pagesStore.categories.length,
      async (newLength, oldLength) => {
        if (newLength > oldLength) {
          await loadAllPagesAdmin();
        }
      }
    );

    return {
      pagesStore,
      newPageTitle,
      newPageSlug,
      newPageSlugManuallyEdited,
      newPageCategoryId,
      newCategoryTitle,
      showAddCategoryModal,
      showAddPageModal,
      editingPage,
      editingCategory,
      activeCategoryAccordion,
      sortedCategories,
      getPagesForCategory,
      generateSlug,
      handleAddCategory,
      openEditCategoryModal,
      handleUpdateCategory,
      handleDeleteCategory,
      openAddPageModal,
      handleAddPage,
      openEditPageModal,
      handleUpdatePageDetails,
      handleDeletePage,
      toggleAccordion,
    };
  },
});
</script>

<template>
  <div class="admin-pages-view">
    <header class="admin-header">
      <h1 class="text-2xl font-semibold text-gray-800">
        Manage Pages & Categories
      </h1>
      <button @click="showAddCategoryModal = true" class="btn btn-primary">
        Add New Category
      </button>
    </header>

    <div
      v-if="!sortedCategories.length && !pagesStore.isLoading"
      class="text-center py-10 text-gray-500"
    >
      No categories found. Add a category to get started.
    </div>
    <div v-if="pagesStore.isLoading" class="text-center py-10 text-gray-500">
      Loading categories...
    </div>

    <div class="categories-accordion space-y-2">
      <div
        v-for="category in sortedCategories"
        :key="category.id"
        class="category-item"
      >
        <button @click="toggleAccordion(category.id)" class="category-header">
          <span class="font-medium text-lg">{{ category.title }}</span>
          <div class="category-actions">
            <button
              @click.stop="openEditCategoryModal(category)"
              class="btn-icon text-blue-600 hover:text-blue-800"
              title="Edit Category"
            >
              ⚙️
            </button>
            <button
              @click.stop="handleDeleteCategory(category)"
              class="btn-icon text-red-600 hover:text-red-800"
              title="Delete Category"
            >
              🗑️
            </button>
            <span class="accordion-icon">
              <svg
                class="w-6 h-6 transition-transform duration-200"
                :class="{
                  'rotate-180': activeCategoryAccordion === category.id,
                }"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 9l-7 7-7-7"
                ></path>
              </svg>
            </span>
          </div>
        </button>

        <div
          v-if="activeCategoryAccordion === category.id"
          class="category-content"
        >
          <div class="flex justify-end mb-3">
            <button
              @click="openAddPageModal(category.id)"
              class="btn btn-secondary btn-sm"
            >
              Add New Page to {{ category.title }}
            </button>
          </div>
          <div
            v-if="
              pagesStore.pagesByCategory[category.id]?.isLoading &&
              (!pagesStore.pagesByCategory[category.id]?.pages ||
                pagesStore.pagesByCategory[category.id]?.pages.length === 0)
            "
            class="text-sm text-gray-500 py-3 text-center"
          >
            Loading pages...
          </div>
          <ul
            v-else-if="getPagesForCategory(category.id).length"
            class="space-y-2"
          >
            <li
              v-for="page in getPagesForCategory(category.id)"
              :key="page.id"
              class="page-list-item"
            >
              <span
                >{{ page.title }}
                <em class="text-xs text-gray-500">(/{{ page.slug }})</em></span
              >
              <div class="page-actions">
                <RouterLink
                  :to="{
                    name: 'page-edit',
                    params: { idSlug: `${page.id}-${page.slug}` },
                  }"
                  class="btn-icon text-green-600 hover:text-green-800"
                  title="Edit Content"
                >
                  📝
                </RouterLink>
                <button
                  @click.stop="openEditPageModal(page)"
                  class="btn-icon text-blue-600 hover:text-blue-800"
                  title="Edit Details (Title/Slug/Category)"
                >
                  ⚙️
                </button>
                <RouterLink
                  :to="{
                    name: 'page',
                    params: { idSlug: `${page.id}-${page.slug}` },
                  }"
                  target="_blank"
                  class="btn-icon text-indigo-600 hover:text-indigo-800"
                  title="View Page"
                >
                  👁️
                </RouterLink>
                <button
                  @click="handleDeletePage(page)"
                  class="btn-icon text-red-600 hover:text-red-800"
                  title="Delete Page"
                >
                  🗑️
                </button>
              </div>
            </li>
          </ul>
          <p
            v-else-if="!pagesStore.pagesByCategory[category.id]?.isLoading"
            class="text-sm text-gray-500 py-3 text-center"
          >
            No pages in this category yet.
          </p>
          <div
            v-if="
              pagesStore.pagesByCategory[category.id] &&
              pagesStore.pagesByCategory[category.id].hasMore &&
              !pagesStore.pagesByCategory[category.id].isLoading
            "
            class="text-center mt-2"
          >
            <button
              @click="
                pagesStore.fetchPages(
                  category.id,
                  pagesStore.pagesByCategory[category.id].currentPage + 1
                )
              "
              class="btn btn-link btn-sm"
            >
              Load More Pages
            </button>
          </div>
          <div
            v-if="
              pagesStore.pagesByCategory[category.id]?.isLoading &&
              pagesStore.pagesByCategory[category.id]?.pages.length > 0
            "
            class="text-sm text-gray-500 py-3 text-center"
          >
            Loading more pages...
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Category Modal -->
    <div v-if="showAddCategoryModal || editingCategory" class="modal-overlay">
      <div class="modal-content">
        <h3 class="text-lg font-medium leading-6 text-gray-900 mb-4">
          {{ editingCategory ? "Edit Category" : "Add New Category" }}
        </h3>
        <input
          v-if="editingCategory"
          v-model="editingCategory.title"
          placeholder="Category Title (e.g., 2024, Announcements)"
          class="input w-full mb-4"
          @keyup.enter="handleUpdateCategory()"
        />
        <input
          v-else
          v-model="newCategoryTitle"
          placeholder="Category Title (e.g., 2024, Announcements)"
          class="input w-full mb-4"
          @keyup.enter="handleAddCategory()"
        />
        <div class="modal-actions">
          <button
            @click="
              editingCategory
                ? (editingCategory = null)
                : (showAddCategoryModal = false)
            "
            class="btn btn-neutral"
          >
            Cancel
          </button>
          <button
            @click="
              editingCategory ? handleUpdateCategory() : handleAddCategory()
            "
            class="btn btn-primary"
          >
            {{ editingCategory ? "Save Changes" : "Add Category" }}
          </button>
        </div>
      </div>
    </div>

    <!-- Add/Edit Page Modal -->
    <div v-if="showAddPageModal || editingPage" class="modal-overlay">
      <div class="modal-content">
        <h3 class="text-lg font-medium leading-6 text-gray-900 mb-4">
          {{ editingPage ? "Edit Page Details" : "Add New Page" }}
        </h3>
        <div v-if="editingPage">
          <label class="label">Title</label>
          <input
            v-model="editingPage.title"
            placeholder="Page Title"
            class="input w-full"
          />
          <div class="mt-2">
            <label class="label">Slug</label>
            <input
              v-model="editingPage.slug"
              placeholder="page-slug"
              class="input w-full"
            />
          </div>
          <div class="mt-2">
            <label class="label">Category</label>
            <select
              v-model.number="editingPage.category_id"
              class="input w-full"
            >
              <option
                v-for="cat in sortedCategories"
                :key="cat.id"
                :value="cat.id"
              >
                {{ cat.title }}
              </option>
            </select>
          </div>
        </div>
        <div v-else>
          <label class="label">Title</label>
          <input
            v-model="newPageTitle"
            placeholder="Page Title"
            class="input w-full"
          />
          <div class="mt-2">
            <label class="label">Slug</label>
            <input
              v-model="newPageSlug"
              @input="newPageSlugManuallyEdited = true"
              placeholder="page-slug (auto-generated or custom)"
              class="input w-full"
            />
          </div>
        </div>
        <!-- HTML content editor is not part of this modal, only title/slug/category -->
        <div class="modal-actions mt-6">
          <button
            @click="
              editingPage ? (editingPage = null) : (showAddPageModal = false)
            "
            class="btn btn-neutral"
          >
            Cancel
          </button>
          <button
            @click="editingPage ? handleUpdatePageDetails() : handleAddPage()"
            class="btn btn-primary"
          >
            {{ editingPage ? "Save Details" : "Add Page" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import "tailwindcss";

.admin-pages-view {
  @apply p-4 sm:p-6 bg-gray-100 min-h-screen;
}
.admin-header {
  @apply flex justify-between items-center mb-6 pb-4 border-b border-gray-300;
}

.btn {
  @apply px-4 py-2 rounded-md font-medium transition-colors duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2;
}
.btn-sm {
  @apply px-3 py-1 text-sm;
}
.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500;
}
.btn-secondary {
  @apply bg-green-500 text-white hover:bg-green-600 focus:ring-green-500;
}
.btn-neutral {
  @apply bg-gray-200 text-gray-700 hover:bg-gray-300 focus:ring-gray-400;
}
.btn-danger {
  @apply bg-red-600 text-white hover:bg-red-700 focus:ring-red-500;
}
.btn-link {
  @apply text-blue-600 hover:text-blue-800 hover:underline;
}
.btn-icon {
  @apply p-1 rounded-full hover:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-gray-400;
}

.category-item {
  @apply bg-white shadow-sm rounded-lg overflow-hidden border border-gray-200;
}
.category-header {
  @apply flex justify-between items-center w-full p-4 text-left text-gray-700 hover:bg-gray-50 focus:outline-none;
}
.category-actions {
  @apply flex items-center space-x-2;
}
.accordion-icon svg {
  @apply text-gray-500;
}
.category-content {
  @apply p-4 border-t border-gray-200 bg-gray-50;
}

.page-list-item {
  @apply flex justify-between items-center p-3 bg-white rounded-md border border-gray-200 hover:shadow-md transition-shadow;
}
.page-actions {
  @apply flex items-center space-x-2;
}

.modal-overlay {
  @apply fixed inset-0 bg-black/75 flex items-center justify-center p-4 z-50;
}
.modal-content {
  @apply bg-white p-6 rounded-lg shadow-xl w-full max-w-md;
}
.modal-actions {
  @apply flex justify-end space-x-3 mt-4;
}

.input {
  @apply block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm;
}
.label {
  @apply block text-sm font-medium text-gray-700 mb-1;
}
</style>
