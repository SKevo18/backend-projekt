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
          id: 1,
          name: "John Doe",
          email: "john.doe@example.com",
          role: "admin",
          createdAt: "2025-03-02",
          updatedAt: "2025-03-17",
        },
        {
          id: 2,
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
        <td>{{ user.email }}</td>
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
            <option :selected="user.role === 'user'" value="user">User</option>
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
</style>
