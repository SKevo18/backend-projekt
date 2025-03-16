<script lang="ts">
export default {
  name: "RegisterView",
  data() {
    return {
      email: "@",
      password: "",
      confirmPassword: "",
      registeredSuccessfully: null as boolean | null,
    };
  },
  methods: {
    async handleRegister() {
      this.registeredSuccessfully = this.$authStore.register(
        this.email,
        this.password,
        this.confirmPassword
      );
    },
  },
};
</script>

<template>
  <div class="form-container" v-if="registeredSuccessfully === null">
    <form @submit.prevent="handleRegister">
      <fieldset>
        <legend>Register</legend>

        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required />
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            required
          />
        </div>

        <button class="button" type="submit">Register</button>
      </fieldset>
    </form>
  </div>

  <div v-else-if="registeredSuccessfully">
    <div class="success">
      <h1>Registered successfully! Check your email for verification.</h1>
      <RouterLink to="/login">Login</RouterLink>
    </div>
  </div>

  <div v-else>
    <div class="error">
      <h1>Registration failed. Please, try again later.</h1>
    </div>
  </div>
</template>

<style scoped>
@import "tailwindcss";

.form-container {
  @apply my-20 mx-auto;
}
</style>
