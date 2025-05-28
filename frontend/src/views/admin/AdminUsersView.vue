<script lang="ts">
import { useAuthStore } from "@/store/authStore";
import api from "@/services/api";

interface Page {
  id: number;
  title: string;
  category_id: number;
}

export default {
  name: "AdminUsersView",
  data() {
    return {
      users: [] as {
        id: number;
        first_name: string;
        last_name: string;
        user_email: string;
        role: number;
        registered_at: string;
        edited_at: string | null;
      }[],
      editedRoles: {} as Record<number, string>,
      allPages: {} as Record<
        number,
        {
          pages: Page[];
          currentPage: number;
          hasMore: boolean;
          isLoading: boolean;
        }
      >,
      userPermissions: {
        pages: {} as Record<number, number[]>,
        categories: {} as Record<number, number[]>,
      },
      selectedUser: null as {
        id: number | null;
        first_name: string;
        last_name: string;
      } | null,
      showPermissionsModal: false,
      categories: [] as { id: number; title: string }[],
      activeTab: "pages" as "pages" | "categories",
      isLoading: false,
    };
  },
  methods: {
    async getUsers() {
      const authStore = useAuthStore();
      if (!authStore.isAuthenticated) {
        alert("Please log in to access this page.");
        return;
      }

      try {
        const response = await api.get("/user/", {
          headers: { Authorization: `Bearer ${authStore.token}` },
        });
        this.users = response.data;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },

    async deleteUser(id: number) {
      if (!confirm("Are you sure you want to delete this user?")) {
        return;
      }

      const authStore = useAuthStore();
      try {
        await api.delete(`/user/${id}`, {
          headers: { Authorization: `Bearer ${authStore.token}` },
        });
        this.users = this.users.filter((user) => user.id !== id);
      } catch (error: any) {
        console.error("Error deleting user:", error);
        alert(error.response?.data?.detail || "Error deleting user");
      }
    },

    async changeUserRole(id: number, event: Event) {
      const role = (event.target as HTMLSelectElement).value;
      if (this.users.find((user) => user.id === id)?.role !== parseInt(role)) {
        this.editedRoles[id] = role;
      } else {
        delete this.editedRoles[id];
      }
    },

    async confirmRoleChange(userId: number) {
      const authStore = useAuthStore();
      const newRole = this.editedRoles[userId];
      try {
        await api.patch(
          `/user/${userId}/role`,
          { role: newRole },
          { headers: { Authorization: `Bearer ${authStore.token}` } }
        );
        delete this.editedRoles[userId];
        await this.getUsers();
      } catch (error) {
        console.error("Error updating role:", error);
        alert("Failed to update role.");
      }
    },

    async getAllPages() {
      const authStore = useAuthStore();
      try {
        const response = await api.get("/page/", {
          headers: { Authorization: `Bearer ${authStore.token}` },
        });
        this.allPages = response.data;
      } catch (error) {
        console.error("Error fetching pages:", error);
      }
    },

    async getCategories() {
      const authStore = useAuthStore();
      try {
        const response = await api.get("/category/", {
          headers: { Authorization: `Bearer ${authStore.token}` },
        });
        this.categories = response.data;
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    },

    async getUserPermissions(userId: number) {
      try {
        const [pagesRes, categoriesRes] = await Promise.all([
          api.get(`/permissions/${userId}/pages`),
          api.get(`/permissions/${userId}/categories`),
        ]);
        this.userPermissions.pages[userId] = pagesRes.data;
        this.userPermissions.categories[userId] = categoriesRes.data;
      } catch (error) {
        console.error("Error fetching permissions:", error);
      }
    },

    async fetchPagesForCategory(
      categoryId: number,
      page: number = 1,
      limit: number = 10
    ) {
      const authStore = useAuthStore();
      if (!this.allPages[categoryId]) {
        this.allPages[categoryId] = {
          pages: [],
          currentPage: 0,
          hasMore: true,
          isLoading: false,
        };
      }

      if (this.allPages[categoryId].isLoading) return;

      this.allPages[categoryId].isLoading = true;

      try {
        const response = await api.get(`/page/`, {
          params: { category_id: categoryId, page: page, limit: limit },
          headers: { Authorization: `Bearer ${authStore.token}` },
        });

        const fetchedPages = response.data as Page[];

        if (page === 1) {
          this.allPages[categoryId].pages = fetchedPages;
        } else {
          this.allPages[categoryId].pages.push(...fetchedPages);
        }
        this.allPages[categoryId].currentPage = page;
        this.allPages[categoryId].hasMore = fetchedPages.length === limit;
      } catch (error) {
        console.error(
          `Error fetching pages for category ${categoryId}:`,
          error
        );
        this.allPages[categoryId].hasMore = false;
      } finally {
        this.allPages[categoryId].isLoading = false;
      }
    },

    async loadInitialPagesForCategories() {
      if (this.activeTab === "pages") {
        for (const category of this.categories) {
          const categoryData = this.allPages[category.id];
          if (
            !categoryData ||
            (categoryData.pages.length === 0 && !categoryData.isLoading)
          ) {
            await this.fetchPagesForCategory(category.id, 1);
          }
        }
      }
    },

    async togglePermission(userId: number, pageId: number) {
      const authStore = useAuthStore();
      const hasPermission =
        this.userPermissions.pages[userId]?.includes(pageId);

      try {
        if (hasPermission) {
          await api.delete("/permissions/", {
            params: { user_id: userId, page_id: pageId },
            headers: { Authorization: `Bearer ${authStore.token}` },
          });
        } else {
          await api.post("/permissions/", null, {
            params: { user_id: userId, page_id: pageId },
            headers: { Authorization: `Bearer ${authStore.token}` },
          });
        }
        await this.getUserPermissions(userId);
      } catch (error) {
        console.error("Error updating permission:", error);
        alert("Failed to update permission.");
      }
    },

    async toggleCategoryPermission(userId: number, categoryId: number) {
      const authStore = useAuthStore();
      const hasPermission =
        this.userPermissions.categories[userId]?.includes(categoryId);

      try {
        if (hasPermission) {
          await api.delete("/permissions/category", {
            params: { user_id: userId, category_id: categoryId },
            headers: { Authorization: `Bearer ${authStore.token}` },
          });
        } else {
          await api.post("/permissions/category", null, {
            params: { user_id: userId, category_id: categoryId },
            headers: { Authorization: `Bearer ${authStore.token}` },
          });
        }
        await this.getUserPermissions(userId);
      } catch (error) {
        console.error("Error updating category permission:", error);
        alert("Failed to update category permission.");
      }
    },

    openPermissionsModal(userId: number) {
      const user = this.users.find((u) => u.id === userId);
      if (user) {
        this.selectedUser = {
          id: userId,
          first_name: user.first_name,
          last_name: user.last_name,
        };
        this.showPermissionsModal = true;
        this.getUserPermissions(userId);
        this.activeTab = "pages";
        this.loadInitialPagesForCategories();
      }
    },

    closePermissionsModal() {
      this.selectedUser = null;
      this.showPermissionsModal = false;
    },

    getPagesByCategory(categoryId: number) {
      return this.allPages[categoryId]?.pages || [];
    },

    switchTab(tab: "pages" | "categories") {
      this.activeTab = tab;
      if (tab === "pages") {
        this.loadInitialPagesForCategories();
      }
    },
  },

  async mounted() {
    const authStore = useAuthStore();
    if (!authStore.isAuthenticated || authStore.user?.role !== 2) {
      alert("Admin access required");
      this.$router.push("/");
      return;
    }
    this.isLoading = true;
    try {
      await Promise.all([this.getUsers(), this.getCategories()]);
    } finally {
      this.isLoading = false;
    }
  },
};
</script>

<template>
  <div class="admin-users-view">
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>

    <div class="hidden md:block">
      <table class="users-table table-fixed">
        <thead>
          <tr>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Created At</th>
            <th>Edited At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.first_name }}</td>
            <td>{{ user.last_name }}</td>
            <td class="break-words">{{ user.user_email }}</td>
            <td>
              <select
                class="role-select"
                @change="changeUserRole(user.id, $event)"
                :value="user.role"
              >
                <option :value="2">Admin</option>
                <option :value="1">Editor</option>
                <option :value="0">User</option>
              </select>
            </td>
            <td>{{ user.registered_at }}</td>
            <td>{{ user.edited_at ? user.edited_at : "Not Edited" }}</td>
            <td>
              <button class="delete-btn" @click="deleteUser(user.id)">
                🗑️
              </button>
              <button
                v-if="editedRoles[user.id]"
                class="confirm-btn"
                @click="confirmRoleChange(user.id)"
              >
                Confirm
              </button>
              <button
                v-if="user.role === 1"
                class="permissions-btn"
                @click="openPermissionsModal(user.id)"
              >
                🔐
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="md:hidden">
      <div v-for="user in users" :key="user.id" class="mobile-user-card">
        <div class="user-field">
          <span class="field-label">First name:</span>
          <span>{{ user.first_name }}</span>
        </div>
        <div class="user-field">
          <span class="field-label">Last name:</span>
          <span>{{ user.last_name }}</span>
        </div>
        <div class="user-field">
          <span class="field-label">Email:</span>
          <span>{{ user.user_email }}</span>
        </div>
        <div class="user-field">
          <span class="field-label">Role:</span>
          <select
            class="role-select"
            @change="changeUserRole(user.id, $event)"
            :value="user.role"
          >
            <option :value="2">Admin</option>
            <option :value="1">Editor</option>
            <option :value="0">User</option>
          </select>
        </div>
        <div class="user-field">
          <span class="field-label">Created:</span>
          <span>{{ user.registered_at }}</span>
        </div>
        <div class="user-field">
          <span class="field-label">Edited:</span>
          <span>{{ user.edited_at ? user.edited_at : "Not Edited" }}</span>
        </div>
        <div class="user-field">
          <span class="field-label">Actions:</span>
          <button class="delete-btn" @click="deleteUser(user.id)">
            Delete
          </button>
          <button
            v-if="editedRoles[user.id]"
            class="confirm-btn"
            @click="confirmRoleChange(user.id)"
          >
            Confirm
          </button>
          <button
            v-if="user.role === 1"
            class="permissions-btn"
            @click="openPermissionsModal(user.id)"
          >
            Permissions
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="showPermissionsModal"
      class="permissions-modal-overlay"
      @click.self="closePermissionsModal"
    >
      <div class="permissions-modal">
        <h3 class="modal-title">
          Manage Permissions for: {{ selectedUser?.first_name }}
          {{ selectedUser?.last_name }}
        </h3>

        <div class="tabs">
          <button
            class="tab-btn"
            :class="{ 'active-tab': activeTab === 'pages' }"
            @click="switchTab('pages')"
          >
            Page Permissions
          </button>
          <button
            class="tab-btn"
            :class="{ 'active-tab': activeTab === 'categories' }"
            @click="switchTab('categories')"
          >
            Category Permissions
          </button>
        </div>

        <div class="permissions-content">
          <div v-if="activeTab === 'pages'" class="page-permissions">
            <div
              v-if="categories.length === 0 && !isLoading"
              class="text-center py-4 text-gray-500"
            >
              No categories found. Page permissions cannot be set.
            </div>
            <div
              v-for="category in categories"
              :key="category.id"
              class="category-section"
            >
              <h4 class="category-title">{{ category.title }}</h4>
              <div
                v-if="
                  getPagesByCategory(category.id).length === 0 &&
                  !allPages[category.id]?.isLoading
                "
                class="text-sm text-gray-500 py-2 text-center"
              >
                No pages in this category.
              </div>
              <div class="pages-grid">
                <div
                  v-for="page in getPagesByCategory(category.id)"
                  :key="page.id"
                  class="page-item"
                >
                  <input
                    type="checkbox"
                    :id="`page-${page.id}`"
                    :checked="
                      selectedUser &&
                      userPermissions.pages[selectedUser.id]?.includes(page.id)
                    "
                    @change="togglePermission(selectedUser?.id || 0, page.id)"
                  />
                  <label :for="`page-${page.id}`">
                    {{ page.title }}
                  </label>
                </div>
              </div>
              <div
                v-if="
                  allPages[category.id]?.isLoading &&
                  (!allPages[category.id]?.pages ||
                    allPages[category.id]?.pages.length === 0)
                "
                class="text-sm text-gray-500 py-2 text-center"
              >
                Loading pages...
              </div>
              <div
                v-if="
                  allPages[category.id]?.isLoading &&
                  allPages[category.id]?.pages &&
                  allPages[category.id]?.pages.length > 0
                "
                class="text-sm text-gray-500 py-2 text-center"
              >
                Loading more pages...
              </div>
              <button
                v-if="
                  allPages[category.id]?.hasMore &&
                  !allPages[category.id]?.isLoading
                "
                @click="
                  fetchPagesForCategory(
                    category.id,
                    (allPages[category.id]?.currentPage || 0) + 1
                  )
                "
                class="mt-2 px-3 py-1 text-sm text-white bg-blue-500 hover:bg-blue-600 rounded"
              >
                Load more...
              </button>
            </div>
          </div>

          <div v-if="activeTab === 'categories'" class="category-permissions">
            <div
              v-if="categories.length === 0 && !isLoading"
              class="text-center py-4 text-gray-500"
            >
              No categories available to set permissions for.
            </div>
            <div class="categories-grid">
              <div
                v-for="category in categories"
                :key="category.id"
                class="category-item"
              >
                <input
                  type="checkbox"
                  :id="`category-${category.id}`"
                  :checked="
                    selectedUser &&
                    userPermissions.categories[selectedUser.id]?.includes(
                      category.id
                    )
                  "
                  @change="
                    toggleCategoryPermission(selectedUser?.id || 0, category.id)
                  "
                />
                <label :for="`category-${category.id}`">
                  {{ category.title }}
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button @click="closePermissionsModal" class="close-btn">
            Save & Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import "tailwindcss";

.admin-users-view {
  @apply relative;
}

.loading-overlay {
  @apply fixed inset-0 bg-black/75 flex items-center justify-center z-50;
}

.loading-spinner {
  @apply w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin;
}

.users-table {
  @apply w-full;
}

.users-table thead {
  @apply bg-green-700 text-white;
}

.users-table tbody tr:nth-child(even) {
  @apply bg-green-100;
}

.users-table tbody tr:nth-child(odd) {
  @apply bg-green-50;
}

.users-table th,
.users-table td {
  @apply p-3 text-left;
}

.role-select {
  @apply cursor-pointer rounded-lg text-sm text-white bg-green-600 hover:bg-green-700 px-2 py-1;
}

.delete-btn {
  @apply cursor-pointer rounded-lg text-sm text-white bg-red-400 hover:bg-red-500 px-2 py-1;
}

.confirm-btn {
  @apply cursor-pointer rounded-lg text-sm text-white bg-green-600 hover:bg-green-700 px-2 py-1 ml-2;
}

.permissions-btn {
  @apply cursor-pointer rounded-lg text-sm text-white bg-blue-600 hover:bg-blue-700 px-2 py-1 ml-2;
}

.mobile-user-card {
  @apply bg-green-100 p-4 mb-4 rounded-lg;
}

.mobile-user-card:nth-child(even) {
  @apply bg-green-50;
}

.user-field {
  @apply flex justify-between items-center mb-2;
}

.field-label {
  @apply font-semibold text-green-700;
}

.permissions-modal-overlay {
  @apply fixed inset-0 bg-black/75 flex items-center justify-center z-50;
}

.permissions-modal {
  @apply bg-white rounded-lg px-6 py-3 max-w-4xl w-full max-h-[95vh] overflow-y-auto;
}

.modal-title {
  @apply text-xl font-bold mb-4 text-gray-800;
}

.tabs {
  @apply flex border-b mb-4;
}

.tab-btn {
  @apply px-4 py-2 font-medium text-gray-600;
}

.active-tab {
  @apply text-blue-600 border-b-2 border-blue-500;
}

.permissions-content {
  @apply mb-4;
}

.category-section {
  @apply mb-6;
}

.category-title {
  @apply font-semibold text-lg mb-2 text-gray-700;
}

.pages-grid {
  @apply grid grid-cols-1 md:grid-cols-2 gap-2;
}

.page-item,
.category-item {
  @apply flex items-center p-2 border rounded hover:bg-gray-50;
}

.page-item input,
.category-item input {
  @apply mr-2;
}

.page-item label,
.category-item label {
  @apply cursor-pointer;
}

.categories-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2;
}

.modal-actions {
  @apply flex justify-end;
}

.close-btn {
  @apply cursor-pointer rounded-lg text-sm text-white bg-blue-600 hover:bg-blue-700 p-2 ml-2;
}
</style>
