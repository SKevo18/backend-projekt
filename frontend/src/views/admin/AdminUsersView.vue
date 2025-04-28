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
      userPermissions: {} as Record<number, number[]>,
      selectedUser: null as number | null,
      showPermissionsModal: false,
      categories: [] as { id: number; title: string }[],
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
        const response = await api.get("http://localhost:8000/user/", {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
        this.users = response.data;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    async deleteUser(id: number) {
      const authStore = useAuthStore();
      if (!authStore.isAuthenticated) {
        alert("Please log in to access this page.");
        return;
      }

      try {
        await api.delete(`http://localhost:8000/user/${id}`, {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
        this.users = this.users.filter((user) => user.id !== id);
      } catch (error) {
        console.error("Error deleting user:", error);
      }
    },
    async changeUserRole(id: number, event: Event) {
      const role = (event.target as HTMLSelectElement).value;
      if (this.users.find(user => user.id === id)?.role !== parseInt(role)) {
        this.editedRoles[id] = role;
      } else {
        delete this.editedRoles[id];
      }
    },
    async confirmRoleChange(userId: number) {
      const authStore = useAuthStore();
      const newRole = this.editedRoles[userId];
      if (!authStore.isAuthenticated) {
        alert("Please log in to access this page.");
        return;
      }

      try {
        await api.patch(
          `http://localhost:8000/user/${userId}/role`,
          { role: newRole },
          {
            headers: {
              Authorization: `Bearer ${authStore.token}`,
            },
          }
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
        const response = await api.get("http://localhost:8000/page/", {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
        this.allPages = response.data;
      } catch (error) {
        console.error("Error fetching pages:", error);
      }
    },
    async getCategories() {
      const authStore = useAuthStore();
      try {
        const response = await api.get("http://localhost:8000/category/", {
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
        this.categories = response.data;
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    },
    async getUserPermissions(userId: number) {
      const authStore = useAuthStore();
      try {
        const response = await api.get(
          `http://localhost:8000/permissions/${userId}/pages`,
          {
            headers: {
              Authorization: `Bearer ${authStore.token}`,
            },
          }
        );
        this.userPermissions[userId] = response.data;
      } catch (error) {
        console.error("Error fetching permissions:", error);
      }
    },
    async togglePermission(userId: number, pageId: number) {
      const authStore = useAuthStore();
      const hasPermission = this.userPermissions[userId]?.includes(pageId);

      try {
        if (hasPermission) {
          await api.delete("http://localhost:8000/permissions/", {
            params: { user_id: userId, page_id: pageId },
            headers: {
              Authorization: `Bearer ${authStore.token}`,
            },
          });
        } else {
          await api.post("http://localhost:8000/permissions/", null, {
            params: { user_id: userId, page_id: pageId },
            headers: {
              Authorization: `Bearer ${authStore.token}`,
            },
          });
        }
        await this.getUserPermissions(userId);
      } catch (error) {
        console.error("Error updating permission:", error);
        alert("Failed to update permission.");
      }
    },
    openPermissionsModal(userId: number) {
      this.selectedUser = userId;
      this.showPermissionsModal = true;
      this.getUserPermissions(userId);
    },
    closePermissionsModal() {
      this.selectedUser = null;
      this.showPermissionsModal = false;
    },
    getPagesByCategory(categoryId: number) {
      return this.allPages.filter(page => page.category_id === categoryId);
    },
  },
  async mounted() {
    const authStore = useAuthStore();
    if (!authStore.isAuthenticated || authStore.user?.role !== 2) {
      alert("Admin access required");
      this.$router.push("/");
      return;
    }
    await this.getUsers();
    await this.getAllPages();
    await this.getCategories();
  },
};
</script>

<template>
  <!-- desktop -->
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
            <select class="cursor-pointer rounded-lg text-sm text-white button-green px-2 py-1"
              @change="changeUserRole(user.id, $event)" :value="user.role">
              <option :value="2">Admin</option>
              <option :value="1">Editor</option>
              <option :value="0">User</option>
            </select>
          </td>
          <td>{{ user.registered_at }}</td>
          <td>{{ user.edited_at ? user.edited_at : "Not Edited" }}</td>
          <td>
            <button class="cursor-pointer rounded-lg text-sm text-white button-red px-2 py-1"
              @click="deleteUser(user.id)">
              Delete
            </button>
            <button v-if="editedRoles[user.id]"
              class="cursor-pointer rounded-lg text-sm text-white button-green px-2 py-1"
              @click="confirmRoleChange(user.id)">
              Confirm
            </button>
            <button v-if="user.role === 1"
              class="cursor-pointer rounded-lg text-sm text-white button-blue px-2 py-1 ml-2"
              @click="openPermissionsModal(user.id)">
              Manage Pages
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- mobile -->
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
        <select class="cursor-pointer rounded-lg text-sm text-white button-green px-2 py-1"
          @change="changeUserRole(user.id, $event)" :value="user.role">
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
        <button class="cursor-pointer rounded-lg text-sm text-white button-red px-2 py-1" @click="deleteUser(user.id)">
          Delete
        </button>
        <button v-if="editedRoles[user.id]"
          class="cursor-pointer rounded-lg text-sm text-white button-green px-2 py-1 ml-2"
          @click="confirmRoleChange(user.id)">
          Confirm
        </button>
        <button v-if="user.role === 1" class="cursor-pointer rounded-lg text-sm text-white button-blue px-2 py-1 ml-2"
          @click="openPermissionsModal(user.id)">
          Manage Pages
        </button>
      </div>
    </div>
  </div>

  <!-- Permissions Modal -->
  <div v-if="showPermissionsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    @click.self="closePermissionsModal">
    <div class="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
      <h3 class="text-xl font-bold mb-4">
        Manage Page Permissions for User #{{
          selectedUser
        }}
      </h3>

      <div v-for="category in categories" :key="category.id" class="mb-6">
        <h4 class="font-semibold text-lg mb-2">{{ category.title }}</h4>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
          <div v-for="page in getPagesByCategory(category.id)" :key="page.id"
            class="flex items-center p-2 border rounded">
            <input type="checkbox" :id="`page-${page.id}`" :checked="userPermissions[selectedUser!]?.includes(page.id) || false
              " @change="togglePermission(selectedUser!, page.id)" class="mr-2" />
            <label :for="`page-${page.id}`" class="cursor-pointer">
              {{ page.title }}
            </label>
          </div>
        </div>
      </div>

      <div class="flex justify-end mt-4">
        <button @click="closePermissionsModal" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<style>
@import "tailwindcss";

.users-table {
  @apply w-full;
}

.users-table thead {
  @apply bg-green-700 text-white;
}

.users-table tbody tr:nth-child(even) {
  @apply bg-green-200;
}

.users-table tbody tr:nth-child(odd) {
  @apply bg-green-100;
}

.users-table th {
  @apply text-left p-3;
}

.users-table td {
  @apply text-left p-3;
}

.mobile-user-card {
  @apply bg-green-100 p-4 mb-4 rounded-lg;
}

.mobile-user-card:nth-child(even) {
  @apply bg-green-200;
}

.user-field {
  @apply flex justify-between items-center mb-2;
}

.field-label {
  @apply font-semibold text-green-700;
}

.button-blue {
  @apply bg-blue-600 hover:bg-blue-700;
}

.button-green {
  @apply bg-green-600 hover:bg-green-700;
}

.button-red {
  @apply bg-red-600 hover:bg-red-700;
}
</style>