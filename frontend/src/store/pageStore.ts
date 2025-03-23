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
                this.error = 'Failed to fetch pages.';
            }
        },

        async fetchPageById(id: number) {
            try {
                const response = await api.get(`/page/${id}`);
                return response.data;
            } catch (error) {
                console.error(`Error loading page with ID ${id}:`, error);
                throw error;
            }
        },

        async addCategory(category: string) {
            if (!this.categories.includes(category)) {
                try {
                    const newCategory = { html_content: category };  
                    await api.post('/page/', newCategory); 
                    await this.fetchPages();
                } catch (error) {
                    console.error(' Error adding category:', error);
                    throw error;
                }
            } else {
                alert(`Category "${category}" already exists.`);
            }
        },

        async addPage(category: string, title: string, description: string) {
            if (!this.pages.some(page => page.title === title)) {
                try {
                    const newPage = { category, title, description };
                    await api.post('/page/', newPage);
                    await this.fetchPages();
                } catch (error) {
                    this.error = `Failed to create page "${title}".`;
                }
            } else {
                alert(`Page with the title "${title}" already exists.`);
            }
        },

        async updatePage(id: number, updatedData: Partial<Page>) {
            try {
                await api.put(`/page/${id}`, updatedData);
                await this.fetchPages();
            } catch (error) {
                this.error = `Failed to update page with ID ${id}.`;
            }
        },

        async deletePage(id: number) {
            try {
                await api.delete(`/page/${id}`);
                await this.fetchPages();
            } catch (error) {
                this.error = `Failed to delete page with ID ${id}.`;
            }
        },

        getCategories() {
            this.categories = [...new Set(this.pages.map(page => page.category))];
        }
    }
});
