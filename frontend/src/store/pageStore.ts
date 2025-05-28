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

interface PaginatedPages {
  pages: Page[];
  currentPage: number;
  hasMore: boolean;
  isLoading: boolean;
}

export const usePagesStore = defineStore("pages", {
  state: () => ({
    pages: [] as Page[],
    categories: [] as Category[],
    error: null as string | null,
    isLoadingCategories: false,
    pagesByCategory: {} as Record<number, PaginatedPages>,
    activePageCategoryId: null as number | null,
  }),

  actions: {
    async fetchPages(
      category_id: number,
      pageNumber: number = 1,
      pageSize: number = 10
    ) {
      if (this.pagesByCategory[category_id]?.isLoading) {
        return;
      }

      try {
        if (!this.pagesByCategory[category_id]) {
          this.pagesByCategory[category_id] = {
            pages: [],
            currentPage: 0,
            hasMore: true,
            isLoading: false,
          };
        }

        this.pagesByCategory[category_id].isLoading = true;
        const response = await api.get("/page/", {
          params: { category_id, page: pageNumber, limit: pageSize },
        });
        const newPages = response.data as Page[];

        if (pageNumber === 1) {
          this.pagesByCategory[category_id].pages = newPages;
        } else {
          this.pagesByCategory[category_id].pages.push(...newPages);
        }

        this.pagesByCategory[category_id].currentPage = pageNumber;
        this.pagesByCategory[category_id].hasMore =
          newPages.length === pageSize;
        return newPages;
      } catch (error) {
        this.error = "Failed to load pages.";
        if (this.pagesByCategory[category_id]) {
          this.pagesByCategory[category_id].hasMore = false;
        }
        return [];
      } finally {
        if (this.pagesByCategory[category_id]) {
          this.pagesByCategory[category_id].isLoading = false;
        }
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
      this.isLoadingCategories = true;
      try {
        const response = await api.get("/category/");
        this.categories = response.data;
      } catch (error) {
        this.error = "Failed to load categories.";
        this.categories = [];
      } finally {
        this.isLoadingCategories = false;
      }
    },

    async addCategory(title: string) {
      if (!this.categories.some((cat) => cat.title === title)) {
        try {
          const newCategory = { title };
          const response = await api.post("/category/", newCategory);
          this.categories.push(response.data);
          // @ts-ignore
          this.pagesByCategory[response.data.id] = {
            pages: [],
            currentPage: 0,
            hasMore: true,
            isLoading: false,
          };
        } catch (error) {
          throw error;
        }
      } else {
        alert(`Kategória "${title}" už existuje.`);
      }
    },
    async updateCategory(category_id: number, updatedData: Partial<Category>) {
      try {
        const response = await api.put(`/category/${category_id}`, updatedData);
        const updatedCategoryFromServer = response.data as Category;

        const index = this.categories.findIndex(
          (cat) => cat.id === category_id
        );
        if (index !== -1) {
          this.categories.splice(index, 1, updatedCategoryFromServer);
        }
      } catch (error) {
        this.error = `Failed to update category ${category_id}. Details: ${error}`;
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
        this.error = `Failed to update page ${page_id}: ${error?.response?.data?.detail || error?.message || "Unknown error"}`;
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
    setActivePageCategoryId(categoryId: number | null) {
      this.activePageCategoryId = categoryId;
    },
  },
});
