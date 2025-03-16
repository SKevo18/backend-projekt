<script lang="ts">
export default {
  name: "LoginView",
  data() {
    return {
      email: "@",
      password: "",
    };
  },
  methods: {
    async handleLogin() {
      this.$authStore.login(this.email, this.password);
    },
  },
};
</script>

<template>
  <div class="form-container">
    <form @submit.prevent="handleLogin">
      <fieldset>
        <legend>Prihlásenie</legend>

        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required />
        </div>

        <div class="form-group">
          <label for="password">Heslo</label>
          <input type="password" id="password" v-model="password" required />
        </div>

        <button class="button button-green" type="submit">Prihlásiť sa</button>
      </fieldset>
    </form>
  </div>
</template>

<style scoped>
@import "tailwindcss";

.form-container {
  @apply max-w-md my-20 mx-auto;
}
</style>
