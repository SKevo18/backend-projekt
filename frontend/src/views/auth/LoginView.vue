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
      let success = await this.$authStore.login(this.email, this.password);
      if (success) {
        this.$router.push("/");
      }
    },
  },
};
</script>

<template>
  <div class="auth-form-container">
    <form @submit.prevent="handleLogin" class="auth-form">
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

<style>
@import "./auth_form.css";
</style>
