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
        alert("Prosím, zadajte názov stránky.");
        return;
      }
      if (this.slugConflict) {
        alert("Slug je už zabraný, zvoľte iný.");
        return;
      }
      try {
        await this.pagesStore.addPage(categoryId, this.title, this.slug);
        this.title = "";
        this.slug = "";
        this.slugManuallyEdited = false;
        this.activeCategoryForm = null;
        await this.loadCategoryPages(categoryId);
      } catch {
        alert("Chyba pri pridávaní stránky.");
      }
    },
    async updatePage(page: any) {
      if (!page?.id) return alert("Chýba ID stránky!");
      try {
        await this.pagesStore.updatePage(page.id, {
          title: this.editTitle,
          category_id: this.editCategoryId!,
          slug: this.editSlug,
        });
        this.editingPageId = null;
        this.editCategoryId = null;

        if (page.category_id !== this.editCategoryId) {
          await this.loadCategoryPages(page.category_id);
          await this.loadCategoryPages(this.editCategoryId!);
        } else {
          await this.loadCategoryPages(page.category_id);
        }
      } catch {
        alert("Chyba pri aktualizácii stránky.");
      }
    },
    startEditingPage(page: any) {
      this.editingPageId = page.id;
      this.editTitle = page.title;
      this.editSlug = page.slug;
      this.editCategoryId = page.category_id;
    },
    async addCategory() {
      const title = this.newCategory.trim();
      if (!title) {
        alert("Prosím, zadajte názov kategórie.");
        return;
      }
      try {
        await this.pagesStore.addCategory(title);
        await this.pagesStore.fetchCategories();
        this.newCategory = "";
        this.showAddCategoryForm = false;
      } catch {
        alert("Chyba pri pridávaní kategórie.");
      }
    },
    async deletePage(page: any) {
      if (!page?.id) return alert("Chyba ID stránky");
      if (confirm(`Chcete naozaj vymazať stránku "${page.title}"?`)) {
        try {
          const categoryId = page.category_id;
          await this.pagesStore.deletePage(page);
          await this.loadCategoryPages(categoryId);
        } catch {
          alert("Chyba pri mazaní stránky.");
        }
      }
    },
    toggleAddPageForm(categoryId: number) {
      this.activeCategoryForm =
        this.activeCategoryForm === categoryId ? null : categoryId;
    },
    async loadCategoryPages(categoryId: number) {
      await this.pagesStore.fetchPages(categoryId);
    },
    async loadAllCategoryPages() {
      for (const category of this.sortedCategories) {
        await this.loadCategoryPages(category.id);
      }
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
          <legend class="font-semibold text-xl text-gray-700 mb-2">
            {{ category.title }}
          </legend>

          <div
            v-if="!getPagesForCategory(category.id).length"
            class="text-center text-gray-400 text-sm py-2"
          >
            Žiadne stránky pre túto kategóriu.
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
              <div class="flex flex-wrap gap-2">
                <button
                  @click="startEditingPage(page)"
                  class="bg-yellow-500 text-white py-1 px-3 rounded-md hover:bg-yellow-600 transition"
                >
                  Update
                </button>

                <RouterLink
                  :to="{
                    name: 'page-edit',
                    params: { idSlug: `${page.id}-${page.slug}` },
                  }"
                  class="inline-block bg-blue-600 hover:bg-blue-700 !text-white text-sm font-medium py-1.5 px-4 rounded-md transition"
                >
                  Upraviť obsah
                </RouterLink>

                <RouterLink
                  :to="{
                    name: 'page',
                    params: { idSlug: `${page.id}-${page.slug}` },
                  }"
                  class="inline-block bg-green-600 hover:bg-green-700 !text-white text-sm font-medium py-1.5 px-4 rounded-md transition"
                >
                  Zobraziť
                </RouterLink>

                <button
                  @click="deletePage(page)"
                  class="bg-red-500 text-white py-1 px-3 rounded-md hover:bg-red-600 transition"
                >
                  Delete
                </button>
              </div>
            </div>

            <div v-if="editingPageId === page.id" class="mt-4 space-y-3">
              <input
                v-model="editTitle"
                class="w-full p-2 border rounded-md"
                placeholder="Nový názov stránky"
              />
              <input
                v-model="editSlug"
                @input="slugManuallyEdited = true"
                class="w-full p-2 border rounded-md"
                placeholder="Slug (napr. vlastny-url)"
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
              <button
                @click="updatePage(page)"
                class="bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition"
              >
                Uložiť zmeny
              </button>
            </div>
          </div>

          <div class="text-center mt-6">
            <button
              @click="toggleAddPageForm(category.id)"
              class="bg-green-500 text-white w-full py-2 rounded-md hover:bg-green-600 transition"
            >
              {{
                activeCategoryForm === category.id
                  ? "Skryť formulár"
                  : "Vytvoriť stránku"
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
                placeholder="Názov stránky"
                type="text"
                class="flex-1 border border-gray-300 rounded-md p-2 bg-gray-50"
              />
              <input
                v-model="slug"
                @input="slugManuallyEdited = true"
                placeholder="Slug (automaticky sa vyplní z názvu)"
                type="text"
                class="flex-1 border border-gray-300 rounded-md p-2 bg-gray-50"
                @blur="checkSlugConflict"
              />
              <button
                @click="addPage(category.id)"
                class="bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition w-full md:w-auto"
              >
                Pridať stránku
              </button>
            </div>
            <p v-if="slugConflict" class="text-red-600 text-sm mt-1">
              Tento slug už existuje. Prosím zvoľ iný.
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
          {{
            showAddCategoryForm
              ? "Skryť formulár pre kategóriu"
              : "Pridať novú kategóriu"
          }}
        </button>
      </div>

      <div
        v-if="showAddCategoryForm"
        class="bg-white border border-gray-300 rounded-2xl p-6 shadow space-y-4"
      >
        <div class="flex flex-col md:flex-row gap-4">
          <input
            v-model="newCategory"
            placeholder="Kategória (napr. 2025, Informácie)"
            type="text"
            class="flex-1 border border-gray-300 rounded-md p-2 bg-gray-50"
          />
          <button
            @click="addCategory"
            class="bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition w-full md:w-auto"
          >
            Pridať kategóriu
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
