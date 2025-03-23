import { defineStore } from 'pinia';
import api from '@/services/api';

interface Page {
    id?: number; 
    category: string;
    title: string;
    description: string;
    created_at?: string; 
}

export const usePagesStore = defineStore('pages', {
    state: () => ({
        pages: [] as Page[],
        categories: [] as string[],
        error: null as string | null
    }),

    actions: {
        async fetchPages() {
            try {
                const response = await api.get('/page/');
                this.pages = response.data;
                this.getCategories();
            } catch (error) {
                this.error = 'Nepodarilo sa načítať stránky.';
            }
        },

        async fetchPageById(id: number) {
            try {
                const response = await api.get(`/page/${id}`);
                return response.data;
            } catch (error) {
                console.error(`Chyba pri načítaní stránky s ID ${id}:`, error);
                throw error;
            }
        },

        async addCategory(category: string) {
            if (!this.categories.includes(category)) {
                try {
                    const newCategory = { html_content: category };
                    await api.post('/page/', newCategory); 

                    this.categories.push(category);

                    await this.fetchPages(); 
                } catch (error) {
                    throw error;
                }
            } else {
                alert(`Kategória "${category}" už existuje.`);
            }
        },

        async addPage(category: string, title: string, description: string) {
            if (!this.pages.some(page => page.title === title)) {
                try {
                    const newPage = { category, title, description };
                    const response = await api.post('/page/', newPage);

                    this.pages.push(response.data);

                    await this.fetchPages();
                } catch (error) {
                    this.error = `Nepodarilo sa vytvoriť stránku "${title}".`;
                }
            } else {
                alert(`Stránka s názvom "${title}" už existuje.`);
            }
        },

        async updatePage(id: number, updatedData: Partial<Page>) {
            try {
                await api.put(`/page/${id}`, updatedData);
                await this.fetchPages();
            } catch (error) {
                this.error = `Nepodarilo sa aktualizovať stránku s ID ${id}.`;
            }
        },

        async deletePage(id: number) {
            try {
                await api.delete(`/page/${id}`);
                await this.fetchPages();
            } catch (error) {
                this.error = `Nepodarilo sa odstrániť stránku s ID ${id}.`;
            }
        },

        getCategories() {
            this.categories = [...new Set(this.pages.map(page => page.category))];
        }
    }
});
