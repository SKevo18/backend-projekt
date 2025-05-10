<script lang="ts">
import { useAuthStore } from "@/store/authStore";
import api from "@/services/api";

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
      allPages: [] as { id: number; title: string; category_id: number }[],
      userPermissions: {
        pages: {} as Record<number, number[]>,
        categories: {} as Record<number, number[]>,
      },
      selectedUser: null as { id: number | null; first_name: string; last_name: string } | null,
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
      const authStore = useAuthStore();
      try {
        await api.delete(`/user/${id}`, {
          headers: { Authorization: `Bearer ${authStore.token}` },
        });
        this.users = this.users.filter((user) => user.id !== id);
      } catch (error) {
        console.error("Error deleting user:", error);
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
        const response = await api.get("/page/all", {
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

    async togglePermission(userId: number, pageId: number) {
      const authStore = useAuthStore();
      const hasPermission = this.userPermissions.pages[userId]?.includes(pageId);

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
      const hasPermission = this.userPermissions.categories[userId]?.includes(categoryId);

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
      }
    },

    closePermissionsModal() {
      this.selectedUser = null;
      this.showPermissionsModal = false;
    },

    getPagesByCategory(categoryId: number) {
      return this.allPages.filter((page) => page.category_id === categoryId);
    },

    switchTab(tab: "pages" | "categories") {
      this.activeTab = tab;
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
      await Promise.all([this.getUsers(), this.getAllPages(), this.getCategories()]);
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
              <select class="role-select" @change="changeUserRole(user.id, $event)" :value="user.role">
                <option :value="2">Admin</option>
                <option :value="1">Editor</option>
                <option :value="0">User</option>
              </select>
            </td>
            <td>{{ user.registered_at }}</td>
            <td>{{ user.edited_at ? user.edited_at : 'Not Edited' }}</td>
            <td>
              <button class="delete-btn" @click="deleteUser(user.id)">Delete</button>
              <button v-if="editedRoles[user.id]" class="confirm-btn" @click="confirmRoleChange(user.id)">
                Confirm
              </button>
              <button v-if="user.role === 1" class="permissions-btn" @click="openPermissionsModal(user.id)">
                Manage Permissions
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
          <select class="role-select" @change="changeUserRole(user.id, $event)" :value="user.role">
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
          <span>{{ user.edited_at ? user.edited_at : 'Not Edited' }}</span>
        </div>
        <div class="user-field">
          <span class="field-label">Actions:</span>
          <button class="delete-btn" @click="deleteUser(user.id)">Delete</button>
          <button v-if="editedRoles[user.id]" class="confirm-btn" @click="confirmRoleChange(user.id)">
            Confirm
          </button>
          <button v-if="user.role === 1" class="permissions-btn" @click="openPermissionsModal(user.id)">
            Permissions
          </button>
        </div>
      </div>
    </div>

    <div v-if="showPermissionsModal" class="permissions-modal-overlay" @click.self="closePermissionsModal">
      <div class="permissions-modal">
        <h3 class="modal-title">
          Manage Permissions for: {{ selectedUser?.first_name }} {{ selectedUser?.last_name }}
        </h3>

        <div class="tabs">
          <button class="tab-btn" :class="{ 'active-tab': activeTab === 'pages' }" @click="switchTab('pages')">
            Page Permissions
          </button>
          <button class="tab-btn" :class="{ 'active-tab': activeTab === 'categories' }"
            @click="switchTab('categories')">
            Category Permissions
          </button>
        </div>

        <div class="permissions-content">
          <div v-if="activeTab === 'pages'" class="page-permissions">
            <div v-for="category in categories" :key="category.id" class="category-section">
              <h4 class="category-title">{{ category.title }}</h4>
              <div class="pages-grid">
                <div v-for="page in getPagesByCategory(category.id)" :key="page.id" class="page-item">
                  <input type="checkbox" :id="`page-${page.id}`"
                    :checked="selectedUser && userPermissions.pages[selectedUser.id]?.includes(page.id)"
                    @change="togglePermission(selectedUser?.id || 0, page.id)" />
                  <label :for="`page-${page.id}`">
                    {{ page.title }}
                  </label>
                </div>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'categories'" class="category-permissions">
            <div class="categories-grid">
              <div v-for="category in categories" :key="category.id" class="category-item">
                <input type="checkbox" :id="`category-${category.id}`"
                  :checked="selectedUser && userPermissions.categories[selectedUser.id]?.includes(category.id)"
                  @change="toggleCategoryPermission(selectedUser?.id || 0, category.id)" />
                <label :for="`category-${category.id}`">
                  {{ category.title }}
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button @click="closePermissionsModal" class="close-btn">Close</button>
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
  @apply fixed inset-0 bg-black flex items-center justify-center z-50;
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
  @apply cursor-pointer rounded-lg text-sm text-white bg-red-600 hover:bg-red-700 px-2 py-1;
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
  @apply fixed inset-0 bg-black flex items-center justify-center z-50;
}

.permissions-modal {
  @apply bg-white rounded-lg p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto;
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
  @apply px-4 py-2 bg-gray-300 rounded hover:bg-gray-400;
}
</style>