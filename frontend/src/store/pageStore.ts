import { defineStore } from 'pinia';
import api from '@/services/api';

interface Page {
    id?: number;
    title: string;
    html_content: string;
    category_id: number;
    created_at?: string;
}

interface Category {
    id: number;
    title: string;
}

export const usePagesStore = defineStore('pages', {
    state: () => ({
        pages: [] as Page[],
        categories: [] as Category[],
        error: null as string | null
    }),

    actions: {
        async fetchPages() {
            try {
                const response = await api.get('/page/');
                this.pages = response.data;
                this.getCategories();
                await this.fetchCategories();
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
            async fetchCategories() {
            try {
                const response = await api.get('/category/');
                this.categories = response.data;
            } catch (error) {
                this.error = 'Nepodarilo sa načítať kategórie.';
            }
        },
        async addCategory(title: string) {
            if (!this.categories.some(cat => cat.title === title)) {
                try {
                    const newCategory = { title };
                    const response = await api.post('/category/', newCategory);
                    this.categories.push(response.data);
                    await this.fetchPages();
                } catch (error) {
                    throw error;
                }
            } else {
                alert(`Kategória "${title}" už existuje.`);
            }
        },

        async addPage(category_id: number, title: string, description: string) {
            if (!this.pages.some(page => page.title === title)) {
                try {
                    const newPage = {
                        category_id,
                        title,
                        html_content: description
                    };
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
                if (!updatedData.title && !updatedData.html_content && !updatedData.category_id) {
                    console.warn('Žiadne dáta na aktualizáciu stránky.');
                    return;
                }

                await api.put(`/page/${id}`, updatedData);
                await this.fetchPages();
            } catch (error) {
                this.error = `Nepodarilo sa aktualizovať stránku s ID ${id}.`;
                console.error(error);
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
    }
});