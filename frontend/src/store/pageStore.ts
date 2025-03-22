import { defineStore } from 'pinia';

interface Page {
  category: string;  // Changed from year to category
  title: string;
  description: string;
}

export const usePagesStore = defineStore('pages', {
  state: () => ({
    pages: [] as Page[],
    categories: [] as string[]
  }),
  actions: {
    addPage(category: string, title: string, description: string) {
      if (!this.pages.some(page => page.title === title)) {
        const newPage = { category, title, description };
        this.pages.push(newPage);

        if (!this.categories.includes(category)) {
          this.categories.push(category); 
        }
      } else {
        alert(`Stránka s názvom "${title}" už existuje.`);
      }
    },

    addCategory(category: string) {
      if (!this.categories.includes(category)) {
        this.categories.push(category);
      } else {
        alert(`Kategória "${category}" už existuje.`);
      }
    },

    deletePage(title: string) {
      const pageToDelete = this.pages.find(page => page.title === title);

      if (!pageToDelete) return;

      const { category } = pageToDelete;

      this.pages = this.pages.filter(page => page.title !== title);

      const remainingPagesInCategory = this.pages.some(page => page.category === category);
      if (!remainingPagesInCategory) {
        this.categories = this.categories.filter(cat => cat !== category);
      }
    },

     // This method can be enhanced later to load data dynamically from an API.
    getPages() {
      this.pages = [];
      this.categories = [];
    },

    getCategories() {
      this.categories = [...new Set(this.pages.map(page => page.category))];
    }
  }
});
