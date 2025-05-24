import { defineStore } from "pinia";
import api from "@/services/api";

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

export const usePagesStore = defineStore("pages", {
  state: () => ({
    pages: [] as Page[],
    categories: [] as Category[],
    error: null as string | null,
    pagesByCategory: {} as Record<number, Page[]>,
  }),

  actions: {
    async fetchPages(category_id: number) {
      try {
        const response = await api.get("/page/", { params: { category_id } });
        const pages = response.data;
        this.pagesByCategory[category_id] = pages;
        return pages;
      } catch (error) {
        this.error = "Failed to load pages.";
        return [];
      }
    },

    async fetchPageById(id: number): Promise<Page> {
      try {
        const response = await api.get(`/page/${id}`);
        return response.data as Page;
      } catch (error) {
        throw error;
      }
    },

    async fetchCategories() {
      try {
        const response = await api.get("/category/");
        this.categories = response.data;
      } catch (error) {
        this.error = "Failed to load categories.";
      }
    },

    async addCategory(title: string) {
      if (!this.categories.some((cat) => cat.title === title)) {
        try {
          const newCategory = { title };
          const response = await api.post("/category/", newCategory);
          this.categories.push(response.data);
          // @ts-ignore
          await this.fetchPages(response.data.id);
        } catch (error) {
          throw error;
        }
      } else {
        alert(`Kategória "${title}" už existuje.`);
      }
    },
    async updateCategory(category_id: number, updatedData: Partial<Category>) {
      try {
        await api.put(`/category/${category_id}`, updatedData);
      } catch (error) {
        this.error = `Failed to update category ${category_id}.`;
        throw error;
      }
    },
    async deleteCategory(category: Category) {
      try {
        await api.delete(`/category/${category.id}`);
        this.categories = this.categories.filter(
          (cat) => cat.id !== category.id
        );
        delete this.pagesByCategory[category.id];
        this.pages = this.pages.filter(
          (page) => page.category_id !== category.id
        );
      } catch (error) {
        this.error = `Failed to remove category ${category.id}.`;
        throw error;
      }
    },

    async addPage(category_id: number, title: string, description: string) {
      const categoryExists = this.categories.some(
        (cat) => cat.id === category_id
      );

      if (!categoryExists) {
        this.error = `Invalid category with ID ${category_id}.`;
        alert(this.error);
        return;
      }

      if (!this.pages.some((page) => page.title === title)) {
        try {
          const newPage = {
            category_id,
            title,
            html_content: description,
          };
          const response = await api.post("/page/", newPage);
          this.pages.push(response.data);
          await this.fetchPages(category_id);
        } catch (error) {
          this.error = `Failed to create page "${title}".`;
        }
      } else {
        alert(`The page called "${title}" already exists.`);
      }
    },

    async updatePage(page_id: number, updatedData: Partial<Page>) {
      try {
        await api.put(`/page/${page_id}`, updatedData);
      } catch (error) {
        this.error = `Failed to update page ${page_id}.`;
        throw error;
      }
    },

    async deletePage(page: Page) {
      try {
        await api.delete(`/page/${page.id}`);
        await this.fetchPages(page.category_id);
      } catch (error) {
        this.error = `Failed to delete page ${page.id}.`;
      }
    },
  },
});
