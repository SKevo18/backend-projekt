<script lang="ts">
import { defineComponent } from 'vue';
import { usePagesStore } from '@/store/pageStore';

export default defineComponent({
  name: 'AdminPagesView',
  data() {
    return {
      pagesStore: usePagesStore(),
      title: '',
      description: '',
      newCategory: '',
      showAddCategoryForm: false,
      activeCategoryForm: null
    };
  },
  computed: {
    sortedPages() {
      return [...this.pagesStore.pages].sort((a, b) => a.category.localeCompare(b.category));
    },
    sortedCategories() {
      return [...this.pagesStore.categories].sort((a, b) => a.localeCompare(b));
    }
  },
  methods: {
    async addPage(category: string) {
      if (!this.title.trim()) {
        alert('Prosím, zadajte názov stránky.');
        return;
      }

      if (!this.description.trim()) {
        alert('Prosím, zadajte popis stránky.');
        return;
      }

      try {
        await this.pagesStore.addPage(category, this.title, this.description);
        this.title = '';
        this.description = '';
        this.activeCategoryForm = null;
      } catch (error) {
        alert('Chyba pri pridávaní stránky.');
      }
    },

    async addCategory() {
      const categoryValue = this.newCategory.trim();

      if (!categoryValue) {
        alert('Prosím, zadajte správnu kategóriu.');
        return;
      }

      try {
        if (!this.pagesStore.categories.includes(categoryValue)) {
          await this.pagesStore.addCategory(categoryValue);
        } else {
          alert(`Kategória "${categoryValue}" už existuje.`);
        }

        this.newCategory = '';
        this.showAddCategoryForm = false;
      } catch (error) {
        alert('Chyba pri pridávaní kategórie.');
      }
    },

    async deletePage(title: string) {
      if (confirm(`Ste si istý, že chcete odstrániť stránku "${title}"?`)) {
        try {
          await this.pagesStore.deletePage(title);
        } catch (error) {
          alert('Chyba pri odstraňovaní stránky.');
        }
      }
    },

    toggleAddPageForm(category: string) {
      this.activeCategoryForm = this.activeCategoryForm === category ? null : category;
    }
  },
  async mounted() {
    await this.pagesStore.fetchPages(); // load data from FastAPI
  }
});
</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen space-y-6">
    <div class="space-y-6">
      <div v-for="category in sortedCategories" :key="category" class="bg-white border border-gray-300 rounded-xl p-4 shadow-md">
        <fieldset>
          <legend class="font-bold text-lg text-gray-700">{{ category }}</legend>

          <div v-if="!pagesStore.pages.some(page => page.category === category)" class="text-center text-gray-400">
            Žiadne stránky pre túto kategóriu.
          </div>

          <div v-for="page in sortedPages.filter(page => page.category === category)" 
               :key="page.title"
               class="bg-gray-100 border border-gray-200 rounded-lg p-3 my-2 flex items-center justify-between">
            <p class="text-gray-600">{{ page.title }} - {{ page.description }}</p>
            <button @click="deletePage(page.title)"
                    class="text-red-400 hover:text-red-500 font-medium">
              delete
            </button>
          </div>

          <div class="text-center mt-4">
            <button @click="toggleAddPageForm(category)"
                    class="bg-green-500 text-white w-full py-2 rounded-md hover:bg-green-600 transition">
              {{ activeCategoryForm === category ? 'Skryť formulár' : 'Vytvoriť stránku' }}
            </button>
          </div>

          <div v-if="activeCategoryForm === category" class="bg-white border border-gray-200 rounded-lg p-4 shadow-md mt-4">
            <div class="flex gap-4">
              <input
                v-model="title"
                placeholder="Názov stránky"
                type="text"
                class="flex-1 border border-gray-300 rounded-md p-2 bg-gray-50 focus:ring-2 focus:ring-green-300 focus:outline-none"
              />

              <input
                v-model="description"
                placeholder="Popis"
                type="text"
                class="flex-1 border border-gray-300 rounded-md p-2 bg-gray-50 focus:ring-2 focus:ring-green-300 focus:outline-none"
              />

              <button @click="addPage(category)" 
                      class="bg-green-500 text-white py-2 px-6 rounded-md hover:bg-green-600 transition">
                Pridať stránku
              </button>
            </div>
          </div>
        </fieldset>
      </div>
    </div>

    <div class="space-y-4 mt-4">
      <div class="text-center">
        <button @click="showAddCategoryForm = !showAddCategoryForm"
                class="bg-blue-500 text-white w-full py-2 rounded-md hover:bg-blue-600 transition">
          {{ showAddCategoryForm ? 'Skryť formulár pre kategóriu' : 'Pridať novú kategóriu' }}
        </button>
      </div>

      <div v-if="showAddCategoryForm" class="bg-white border border-gray-300 rounded-xl p-6 shadow-md space-y-4">
        <div class="flex gap-4">
          <input
            v-model="newCategory"
            placeholder="Kategória (napr. 2025, Informácie)"
            type="text"
            class="flex-1 border border-gray-300 rounded-md p-2 bg-gray-50 focus:ring-2 focus:ring-blue-300 focus:outline-none"
          />
          <button @click="addCategory"
                  class="bg-blue-500 text-white py-2 px-6 rounded-md hover:bg-blue-600 transition">
            Pridať kategóriu
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
