<script lang="ts">
export default {
  name: "LoginView",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async handleSubmit() {
      console.log(this.email, this.password);
      this.$authStore.login(this.email, this.password);
    },
  },
};
</script>

<template>
  <div class="form-container">
    <form action="POST" @submit.prevent="handleSubmit">
      <fieldset>
        <legend>Login</legend>

        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" />
        </div>
      </fieldset>

      <button type="submit">Login</button>
    </form>
  </div>
</template>

<style>
@import "tailwindcss";

.form-container {
  @apply flex flex-col items-center justify-center h-full mx-6;
}

.form-container .form-group {
  @apply grid grid-cols-2;
}

.form-container .form-group input {
  @apply border-2 border-gray-500 rounded-md p-2;
}

fieldset {
  @apply space-y-4 items-center justify-center border-2 border-gray-500 rounded-md p-4;
}

legend {
  @apply uppercase text-sm font-bold rounded-lg px-2 border-2 border-gray-500;
}

label {
  @apply text-sm font-bold;
}
</style>
