<script lang="ts">
import { defineComponent } from "vue";
import { usePagesStore } from "@/store/pageStore";
import { RouterLink } from "vue-router";

export default defineComponent({
  name: "AdminPagesView",
  components: { RouterLink },
  data() {
    return {
      pagesStore: usePagesStore(),
      title: "",
      slug: "",
      newCategory: "",
      showAddCategoryForm: false,
      activeCategoryForm: null as number | null,
      editingPageId: null as number | null,
      editTitle: "",
      editSlug: "",
      editCategoryId: null as number | null,
      slugConflict: false,
      slugManuallyEdited: false,
      editingCategoryId: null as number | null,
      editCategoryTitle: "",
      activePageDropdownId: null as number | null,
    };
  },
  computed: {
    sortedCategories() {
      return [...this.pagesStore.categories].sort((a, b) =>
        a.title.localeCompare(b.title)
      );
    },
    getPagesForCategory() {
      return (categoryId: number) => {
        const pages = this.pagesStore.pagesByCategory[categoryId] || [];
        return [...pages].sort((a, b) => a.title.localeCompare(b.title));
      };
    },
  },
  watch: {
    title(newTitle) {
      if (!this.slugManuallyEdited) {
        this.slug = this.generateSlug(newTitle);
      }
    },
  },
  methods: {
    generateSlug(text: string) {
      return text
        .toLowerCase()
        .replace(/\s+/g, "-")
        .replace(/[^\w\-]+/g, "")
        .replace(/\-\-+/g, "-")
        .trim();
    },
    async checkSlugConflict() {
      try {
        const response = await this.pagesStore.checkSlug(this.slug);
        this.slugConflict = response.exists;
      } catch {
        this.slugConflict = false;
      }
    },
    async addPage(categoryId: number) {
      if (!this.title.trim()) {
        alert("Please enter the name of the page.");
        return;
      }
      if (this.slugConflict) {
        alert("Slug is already taken, choose another.");
        return;
      }
      try {
        await this.pagesStore.addPage(categoryId, this.title, "", this.slug);
        this.title = "";
        this.slug = "";
        this.slugManuallyEdited = false;
        this.activeCategoryForm = null;
        await this.loadCategoryPages(categoryId);
      } catch {
        alert("Error when adding the page.");
      }
    },
    async updatePage(page: any) {
      if (!page?.id) return alert("Page ID is missing!");
      const oldCategoryId = page.category_id;
      const newCategoryId = this.editCategoryId!;

      try {
        await this.pagesStore.updatePage(page.id, {
          title: this.editTitle,
          category_id: newCategoryId,
          slug: this.editSlug,
        });

        this.editingPageId = null;
        this.editCategoryId = null;
        this.activePageDropdownId = null;

        if (oldCategoryId !== newCategoryId) {
          await Promise.all([
            this.pagesStore.fetchPages(oldCategoryId),
            this.pagesStore.fetchPages(newCategoryId),
          ]);
          this.pagesStore.pagesByCategory = {
            ...this.pagesStore.pagesByCategory,
          };
        } else {
          await this.pagesStore.fetchPages(oldCategoryId);
          this.pagesStore.pagesByCategory = {
            ...this.pagesStore.pagesByCategory,
          };
        }
      } catch {
        alert("Error when updating the page.");
      }
    },
    startEditingPage(page: any) {
      this.editingPageId = page.id;
      this.editTitle = page.title;
      this.editSlug = page.slug;
      this.editCategoryId = page.category_id;
      this.activePageDropdownId = null;
    },
    async addCategory() {
      const title = this.newCategory.trim();
      if (!title) {
        alert("Please enter the name of the category.");
        return;
      }
      try {
        await this.pagesStore.addCategory(title);
        await this.pagesStore.fetchCategories();
        this.newCategory = "";
        this.showAddCategoryForm = false;
      } catch {
        alert("Error when adding the category.");
      }
    },
    async deletePage(page: any) {
      if (!page?.id) return alert("Page ID error");
      if (confirm(`Do you really want to delete the page "${page.title}"?`)) {
        try {
          const categoryId = page.category_id;
          await this.pagesStore.deletePage(page);
          await this.loadCategoryPages(categoryId);
          this.activePageDropdownId = null;
        } catch {
          alert("Error when deleting the page.");
        }
      }
    },
    startEditingCategory(category: any) {
      this.editingCategoryId = category.id;
      this.editCategoryTitle = category.title;
    },

    async updateCategory(category: any) {
      const newTitle = this.editCategoryTitle.trim();
      if (!newTitle) return alert("The category name cannot be empty.");

      try {
        await this.pagesStore.updateCategory(category.id, { title: newTitle });
        this.editingCategoryId = null;
        await this.pagesStore.fetchCategories();
      } catch {
        alert("Category update error.");
      }
    },

    async deleteCategory(category: any) {
      if (
        confirm(
          `Do you really want to delete the category "${category.title}"? This will also remove all the pages in it.`
        )
      ) {
        try {
          await this.pagesStore.deleteCategory(category);
          await this.pagesStore.fetchCategories();
        } catch {
          alert("Error when deleting the category.");
        }
      }
    },
    toggleAddPageForm(categoryId: number) {
      this.activeCategoryForm =
        this.activeCategoryForm === categoryId ? null : categoryId;
    },
    togglePageDropdown(pageId: number) {
      this.activePageDropdownId =
        this.activePageDropdownId === pageId ? null : pageId;
    },
    async loadCategoryPages(categoryId: number) {
      await this.pagesStore.fetchPages(categoryId);
    },
    async loadAllCategoryPages() {
      for (const category of this.sortedCategories) {
        await this.loadCategoryPages(category.id);
      }
    },
    cancelEditingPage() {
      this.editingPageId = null;
      this.editTitle = "";
      this.editSlug = "";
      this.editCategoryId = null;
      this.activePageDropdownId = null;
    },
  },
  async mounted() {
    if (this.pagesStore.categories.length === 0) {
      await this.pagesStore.fetchCategories();
    }
    await this.loadAllCategoryPages();
  },
});
</script>

<template>
  <div class="p-4 sm:p-6 bg-gray-50 min-h-screen space-y-6">
    <div class="space-y-6">
      <div
        v-for="category in sortedCategories"
        :key="category.id"
        class="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm"
      >
        <fieldset>
          <div class="flex items-center justify-between mb-2">
            <legend class="font-semibold text-xl text-gray-700">
              <span v-if="editingCategoryId !== category.id">{{
                category.title
              }}</span>
              <input
                v-else
                v-model="editCategoryTitle"
                class="border px-2 py-1 rounded-md text-base"
                @keyup.enter="updateCategory(category)"
              />
            </legend>
            <div class="flex gap-2 ml-4">
              <button
                v-if="editingCategoryId !== category.id"
                @click="startEditingCategory(category)"
                class="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded-md text-sm"
              >
                Update
              </button>
              <button
                v-else
                @click="updateCategory(category)"
                class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded-md text-sm"
              >
                Save
              </button>
              <button
                @click="deleteCategory(category)"
                class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-md text-sm"
              >
                Delete
              </button>
            </div>
          </div>

          <div
            v-if="!getPagesForCategory(category.id).length"
            class="text-center text-gray-400 text-sm py-2"
          >
            No pages for this category.
          </div>

          <div
            v-for="page in getPagesForCategory(category.id)"
            :key="page.id"
            class="bg-gray-100 border border-gray-200 rounded-xl p-4 my-3"
          >
            <div
              class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3"
            >
              <p class="text-gray-700 break-words font-medium">
                {{ page.title }}
              </p>
              <div class="relative inline-block text-left">
                <button
                  @click="togglePageDropdown(page.id)"
                  type="button"
                  class="dropdown-button"
                >
                  Actions
                  <svg
                    class="-mr-1 ml-2 h-5 w-5"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </button>

                <div
                  v-if="activePageDropdownId === page.id"
                  class="dropdown"
                  role="menu"
                  aria-orientation="vertical"
                  aria-labelledby="menu-button"
                  tabindex="-1"
                >
                  <div class="py-1" role="none">
                    <a
                      href="#"
                      @click.prevent="startEditingPage(page)"
                      class="dropdown-item"
                      role="menuitem"
                      tabindex="-1"
                      id="menu-item-0"
                      >Update Page</a
                    >
                    <RouterLink
                      :to="{
                        name: 'page-edit',
                        params: { idSlug: `${page.id}-${page.slug}` },
                      }"
                      class="dropdown-item"
                      role="menuitem"
                      tabindex="-1"
                      >Edit Content</RouterLink
                    >
                    <RouterLink
                      :to="{
                        name: 'page',
                        params: { idSlug: `${page.id}-${page.slug}` },
                      }"
                      class="dropdown-item"
                      role="menuitem"
                      tabindex="-1"
                      >View Page</RouterLink
                    >
                    <button
                      @click="deletePage(page)"
                      type="button"
                      class="dropdown-item-danger"
                      role="menuitem"
                      tabindex="-1"
                    >
                      Delete Page
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="editingPageId === page.id" class="mt-4 space-y-3">
              <input
                v-model="editTitle"
                class="w-full p-2 border rounded-md"
                placeholder="New page title"
              />
              <input
                v-model="editSlug"
                @input="slugManuallyEdited = true"
                class="w-full p-2 border rounded-md"
                placeholder="Slug (e.g. my-url)"
              />
              <select
                v-model.number="editCategoryId"
                class="w-full p-2 border rounded-md"
              >
                <option
                  v-for="cat in sortedCategories"
                  :key="cat.id"
                  :value="cat.id"
                >
                  {{ cat.title }}
                </option>
              </select>
              <div class="flex gap-2">
                <button
                  @click="updatePage(page)"
                  class="bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition"
                >
                  Save changes
                </button>
                <button
                  @click="cancelEditingPage()"
                  class="bg-gray-300 text-gray-800 py-2 px-4 rounded-md hover:bg-gray-400 transition"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>

          <div class="text-center mt-6">
            <button
              @click="toggleAddPageForm(category.id)"
              class="bg-green-500 text-white w-full py-2 rounded-md hover:bg-green-600 transition"
            >
              {{
                activeCategoryForm === category.id
                  ? "Hide form"
                  : "Create new page"
              }}
            </button>
          </div>

          <div
            v-if="activeCategoryForm === category.id"
            class="bg-white border border-gray-200 rounded-xl p-4 shadow mt-4"
          >
            <div class="flex flex-col md:flex-row gap-3">
              <input
                v-model="title"
                placeholder="Page title"
                type="text"
                class="flex-1 border border-gray-300 rounded-md p-2 bg-gray-50"
              />
              <input
                v-model="slug"
                @input="slugManuallyEdited = true"
                placeholder="Slug (auto-generated from title)"
                type="text"
                class="flex-1 border border-gray-300 rounded-md p-2 bg-gray-50"
                @blur="checkSlugConflict"
              />
              <button
                @click="addPage(category.id)"
                class="bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition w-full md:w-auto"
              >
                Add page
              </button>
            </div>
            <p v-if="slugConflict" class="text-red-600 text-sm mt-1">
              This slug already exists. Please choose another one.
            </p>
          </div>
        </fieldset>
      </div>
    </div>

    <div class="space-y-4 mt-8">
      <div class="text-center">
        <button
          @click="showAddCategoryForm = !showAddCategoryForm"
          class="bg-green-500 text-white w-full py-2 rounded-md hover:bg-green-600 transition"
        >
          {{ showAddCategoryForm ? "Hide category form" : "Add new category" }}
        </button>
      </div>

      <div
        v-if="showAddCategoryForm"
        class="bg-white border border-gray-300 rounded-2xl p-6 shadow space-y-4"
      >
        <div class="flex flex-col md:flex-row gap-4">
          <input
            v-model="newCategory"
            placeholder="Category (e.g. 2025, Information)"
            type="text"
            class="flex-1 border border-gray-300 rounded-md p-2 bg-gray-50"
          />
          <button
            @click="addCategory"
            class="bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition w-full md:w-auto"
          >
            Add category
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@import "tailwindcss";

.dropdown {
  @apply origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black focus:outline-none z-10;
}

.dropdown-button {
  @apply inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none;
}

.dropdown .dropdown-item {
  @apply text-black hover:text-gray-500 block px-4 py-2 text-sm hover:bg-gray-100 hover:underline cursor-pointer;
}

.dropdown .dropdown-item-danger {
  @apply text-red-500 hover:text-red-600 block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 hover:underline cursor-pointer;
}
</style>
