<script lang="ts">
export default {
  name: "AdminUsersView",
  data() {
    return {
      users: [],
    };
  },
  methods: {
    async getUsers() {
      // this.users = await this.$authStore.fetchJsonAuth("/api/admin/users");
      this.users = [
        {
          id: 2,
          name: "John Doe",
          email: "john.doe@example.com",
          role: "admin",
          createdAt: "2025-03-02",
          updatedAt: "2025-03-17",
        },
        {
          id: 1,
          name: "Jane Doe",
          email: "jane.doe@example.com",
          role: "editor",
          createdAt: "2025-03-06",
          updatedAt: null,
        },
      ];
    },
    async deleteUser(id: number) {
      // await this.$authStore.fetchJsonAuth(`/api/admin/users/${id}`, {
      //   method: "DELETE",
      // });
      this.users = this.users.filter((user) => user.id !== id);
    },
    async changeUserRole(id: number, event: Event) {
      const role = (event.target as HTMLSelectElement).value;
      console.log(id, role);
    },
  },
  mounted() {
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
          <th>Meno</th>
          <th>Email</th>
          <th>Rola</th>
          <th>Vytvorený</th>
          <th>Upravený</th>
          <th>Akcie</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.name }}</td>
          <td class="break-words">{{ user.email }}</td>
          <td>
            <select
              class="cursor-pointer rounded-lg text-sm text-white button-green px-2 py-1"
              @change="changeUserRole(user.id, $event)"
            >
              <option :selected="user.role === 'admin'" value="admin">
                Admin
              </option>
              <option :selected="user.role === 'editor'" value="editor">
                Editor
              </option>
              <option :selected="user.role === 'user'" value="user">
                Používateľ
              </option>
            </select>
          </td>
          <td>{{ user.createdAt }}</td>
          <td>{{ user.updatedAt || "–" }}</td>
          <td>
            <button
              class="cursor-pointer rounded-lg text-sm text-white button-red px-2 py-1"
              @click="deleteUser(user.id)"
            >
              Odstrániť
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
        <span class="field-label">Meno:</span>
        <span>{{ user.name }}</span>
      </div>
      <div class="user-field">
        <span class="field-label">Email:</span>
        <span>{{ user.email }}</span>
      </div>
      <div class="user-field">
        <span class="field-label">Rola:</span>
        <select
          class="cursor-pointer rounded-lg text-sm text-white button-green px-2 py-1"
          @change="changeUserRole(user.id, $event)"
        >
          <option :selected="user.role === 'admin'" value="admin">Admin</option>
          <option :selected="user.role === 'editor'" value="editor">
            Editor
          </option>
          <option :selected="user.role === 'user'" value="user">User</option>
        </select>
      </div>
      <div class="user-field">
        <span class="field-label">Vytvorený:</span>
        <span>{{ user.createdAt }}</span>
      </div>
      <div class="user-field">
        <span class="field-label">Upravený:</span>
        <span>{{ user.updatedAt || "–" }}</span>
      </div>
      <div class="user-field">
        <span class="field-label">Akcie:</span>
        <button
          class="cursor-pointer rounded-lg text-sm text-white button-red px-2 py-1"
          @click="deleteUser(user.id)"
        >
          Odstrániť
        </button>
      </div>
    </div>
  </div>
</template>

<style>
@import "tailwindcss";

/* desktop */
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

/* mobile */
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
