import { defineStore } from 'pinia';

interface Page {
  year: number;
  description: string;
}

export const usePagesStore = defineStore('pages', {
  state: () => ({
    pages: JSON.parse(localStorage.getItem('pages') || '[]') as Page[]
  }),
  actions: {
    addPage(year: number, description: string) {
      if (!this.pages.some(page => page.year === year)) {
        const newPage = { year, description };
        this.pages.push(newPage);
        localStorage.setItem('pages', JSON.stringify(this.pages));
      } else {
        alert(`Page for year ${year} already exist.`);
      }
    },
    deletePage(year: number) {
      this.pages = this.pages.filter(page => page.year !== year);
      localStorage.setItem('pages', JSON.stringify(this.pages));
    },
    getPages() {
      this.pages = JSON.parse(localStorage.getItem('pages') || '[]');
    }
  }
});
