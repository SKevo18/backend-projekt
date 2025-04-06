import { defineStore } from 'pinia';
import api from '@/services/api';

interface Page {
    id?: number;
    title: string;
    slug: string;
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

        async fetchPageBySlug(slug: string) {
            try {
                const response = await api.get(`/page/${slug}`);
                return response.data;
            } catch (error) {
                console.error(`Chyba pri načítaní stránky so slugom "${slug}":`, error);
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
            const categoryExists = this.categories.some(cat => cat.id === category_id);

            if (!categoryExists) {
                this.error = `Neplatná kategória s ID ${category_id}.`;
                alert(this.error);
                return;
            }

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

        async updatePage(slug: string, updatedData: Partial<Page>) {
            try {
                if (!updatedData.title && !updatedData.html_content && !updatedData.category_id) {
                    console.warn('Žiadne dáta na aktualizáciu stránky.');
                    return;
                }

                await api.put(`/page/${slug}`, updatedData);
                await this.fetchPages();
            } catch (error) {
                this.error = `Nepodarilo sa aktualizovať stránku so slugom "${slug}".`;
                console.error(error);
            }
        },

        async deletePage(slug: string) {
            try {
                await api.delete(`/page/${slug}`);
                await this.fetchPages();
            } catch (error) {
                this.error = `Nepodarilo sa odstrániť stránku so slugom "${slug}".`;
            }
        },
    }
});
