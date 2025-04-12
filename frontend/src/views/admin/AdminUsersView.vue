<script lang="ts">
import { useAuthStore } from "@/store/authStore";
import axios from "axios";

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
        const response = await axios.get<User[]>("http://localhost:8000/user/", {
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
        await axios.delete(`http://localhost:8000/user/${id}`, {
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
    //fix
    async confirmRoleChange(userId: number) {
      const authStore = useAuthStore();
      const newRole = this.editedRoles[userId];
      if (!authStore.isAuthenticated) {
        alert("Please log in to access this page.");
        return;
      }

      try {
        await axios.patch(
          `http://localhost:8000/user/${userId}/role`, 
          { role: newRole }, 
          {
        headers: {
          Authorization: `Bearer ${authStore.token}`,
        },
    }
  );

        alert("Role updated successfully!");
        delete this.editedRoles[userId]; 
        this.getUsers(); 
      } catch (error) {
        console.error("Error updating role:", error);
        alert("Failed to update role.");
      }
    },
  },
  mounted() {
    const authStore = useAuthStore();
    if (!authStore.isAuthenticated || authStore.user?.role !== 2) {
      alert("Admin access required");
      this.$router.push("/");
      return;
    }
    this.getUsers();
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
          <td>{{ user.edited_at ? user.edited_at : 'Not Edited' }}</td>
          <td>
            <button class="cursor-pointer rounded-lg text-sm text-white button-red px-2 py-1"
              @click="deleteUser(user.id)">
              Odstrániť
            </button>
            <button v-if="editedRoles[user.id]"
              class="cursor-pointer rounded-lg text-sm text-white button-green px-2 py-1"
              @click="confirmRoleChange(user.id)">
              Confirm
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
        <span>{{ user.edited_at ? user.edited_at : 'Not Edited' }}</span>
      </div>
      <div class="user-field">
        <span class="field-label">Actions:</span>
        <button class="cursor-pointer rounded-lg text-sm text-white button-red px-2 py-1" @click="deleteUser(user.id)">
          Odstrániť
        </button>
        <button v-if="editedRoles[user.id]" class="cursor-pointer rounded-lg text-sm text-white button-green px-2 py-1"
          @click="confirmRoleChange(user.id)">
          Confirm
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
</style>
