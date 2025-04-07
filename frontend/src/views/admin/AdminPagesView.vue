<script lang="ts">
import { defineComponent } from 'vue';
import { usePagesStore } from '@/store/pageStore';

export default defineComponent({
  name: 'AdminPagesView',
  data() {
    return {
      pagesStore: usePagesStore(),
      title: '',
      html_content: '',
      newCategory: '',
      showAddCategoryForm: false,
      activeCategoryForm: null as number | null,
      editingPageId: null as number | null,
      editTitle: '',
      editContent: '',
      editCategoryId: null as number | null
    };
  },
  computed: {
    sortedPages() {
      return [...this.pagesStore.pages].sort((a, b) => a.category_id - b.category_id);
    },
    sortedCategories() {
      return [...this.pagesStore.categories].sort((a, b) => a.title.localeCompare(b.title));
    }
  },
  methods: {
    async addPage(categoryId: number) {
      if (!this.title.trim() || !this.html_content.trim()) {
        alert('Prosím, zadajte všetky polia.');
        return;
      }
      try {
        await this.pagesStore.addPage(categoryId, this.title, this.html_content);
        this.title = '';
        this.html_content = '';
        this.activeCategoryForm = null;
      } catch {
        alert('Chyba pri pridávaní stránky.');
      }
    },
    async addCategory() {
      const title = this.newCategory.trim();
      if (!title) {
        alert('Prosím, zadajte názov kategórie.');
        return;
      }
      try {
        await this.pagesStore.addCategory(title);
        await this.pagesStore.fetchCategories();
        this.newCategory = '';
        this.showAddCategoryForm = false;
      } catch {
        alert('Chyba pri pridávaní kategórie.');
      }
    },
    async deletePage(page: any) {
      if (!page?.slug || !page?.id) return alert('Chyba slug alebo ID stranky');
      if (confirm(`Chcete naozaj vymazať stránku "${page.title}"?`)) {
        try {
          await this.pagesStore.deletePage(page);
        } catch {
          alert('Chyba pri mazaní stránky.');
        }
      }
    },
    toggleAddPageForm(categoryId: number) {
      this.activeCategoryForm = this.activeCategoryForm === categoryId ? null : categoryId;
    },
    startEditingPage(page: any) {
      this.editingPageId = page.id;
      this.editTitle = page.title;
      this.editContent = page.html_content;
      this.editCategoryId = page.category_id;
    },
    async updatePage(page: any) {
      if (!page?.slug || !page?.id) return alert('Chýba slug alebo ID stránky!');
      try {
        await this.pagesStore.updatePage(page, {
          title: this.editTitle,
          html_content: this.editContent,
          category_id: this.editCategoryId!
        });

        this.editingPageId = null;
        this.editCategoryId = null;

        await this.pagesStore.fetchPages();
      } catch {
        alert('Chyba pri aktualizácii stránky.');
      }
    }
  },
  async mounted() {
    await this.pagesStore.fetchPages();
    await this.pagesStore.fetchCategories();
  }
});
</script>


<template>
  <div class="p-4 sm:p-6 bg-gray-50 min-h-screen space-y-6">
    <div class="space-y-6">
      <div v-for="category in sortedCategories" :key="category.id"
        class="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm">
        <fieldset>
          <legend class="font-semibold text-xl text-gray-700 mb-2">
            {{ category.title }}
          </legend>

          <div v-if="!pagesStore.pages.some(page => page.category_id === category.id)"
            class="text-center text-gray-400 text-sm py-2">
            Žiadne stránky pre tútu kategóriu.
          </div>

          <div v-for="page in sortedPages.filter(p => p.category_id === category.id)" :key="page.id"
            class="bg-gray-100 border border-gray-200 rounded-xl p-4 my-3">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
              <p class="text-gray-700 break-words">
                <span class="font-medium">{{ page.title }}</span> – {{ page.html_content }}
              </p>
              <div class="flex gap-2">
                <button @click="startEditingPage(page)"
                  class="bg-yellow-500 text-white py-1 px-3 rounded-md hover:bg-yellow-600 transition">
                  Update
                </button>
                <button @click="deletePage(page)"
                  class="bg-red-500 text-white py-1 px-3 rounded-md hover:bg-red-600 transition">
                  Delete
                </button>
              </div>
            </div>

            <div v-if="editingPageId === page.id" class="mt-4 space-y-3">
              <input v-model="editTitle" class="w-full p-2 border rounded-md" placeholder="Nový názov stránky" />
              <input v-model="editContent" class="w-full p-2 border rounded-md" placeholder="Nový obsah stránky" />
              <select v-model.number="editCategoryId" class="w-full p-2 border rounded-md">
                <option v-for="cat in sortedCategories" :key="cat.id" :value="cat.id">
                  {{ cat.title }}
                </option>
              </select>
              <button @click="updatePage(page)"
                class="bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition">
                Uložiť zmeny
              </button>
            </div>
          </div>

          <div class="text-center mt-6">
            <button @click="toggleAddPageForm(category.id)"
              class="bg-green-500 text-white w-full py-2 rounded-md hover:bg-green-600 transition">
              {{ activeCategoryForm === category.id ? 'Skryť formulár' : 'Vytvoriť stránku' }}
            </button>
          </div>

          <div v-if="activeCategoryForm === category.id"
            class="bg-white border border-gray-200 rounded-xl p-4 shadow mt-4">
            <div class="flex flex-col md:flex-row gap-3">
              <input v-model="title" placeholder="Názov stránky" type="text"
                class="flex-1 border border-gray-300 rounded-md p-2 bg-gray-50" />
              <input v-model="html_content" placeholder="Obsah stránky" type="text"
                class="flex-1 border border-gray-300 rounded-md p-2 bg-gray-50" />
              <button @click="addPage(category.id)"
                class="bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition w-full md:w-auto">
                Pridať stránku
              </button>
            </div>
          </div>
        </fieldset>
      </div>
    </div>

    <div class="space-y-4 mt-8">
      <div class="text-center">
        <button @click="showAddCategoryForm = !showAddCategoryForm"
          class="bg-green-500 text-white w-full py-2 rounded-md hover:bg-green-600 transition">
          {{ showAddCategoryForm ? 'Skryť formulár pre kategóriu' : 'Pridať novú kategóriu' }}
        </button>
      </div>

      <div v-if="showAddCategoryForm" class="bg-white border border-gray-300 rounded-2xl p-6 shadow space-y-4">
        <div class="flex flex-col md:flex-row gap-4">
          <input v-model="newCategory" placeholder="Kategória (napr. 2025, Informácie)" type="text"
            class="flex-1 border border-gray-300 rounded-md p-2 bg-gray-50" />
          <button @click="addCategory"
            class="bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition w-full md:w-auto">
            Pridať kategóriu
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
