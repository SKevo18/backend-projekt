<script lang="ts">
import { defineComponent } from "vue";
import { useAuthStore } from "@/store/authStore";

export default defineComponent({
  name: "LoginView",
  data() {
    return {
      email: "",
      password: "",
      authStore: useAuthStore(),
      info: "",
    };
  },
  methods: {
    async handleLogin() {
      try {
        let response = await this.authStore.login(this.email, this.password);
        if (response.status === 200) {
          this.$router.push("/");
        } else {
          this.info = response.data.msg;
        }
      } catch (error) {
        console.log(error);
        if (
          error.response?.data?.detail &&
          Array.isArray(error.response.data.detail)
        ) {
          const errorMessages = error.response.data.detail.map(
            (err) => err.msg
          );
          this.info = errorMessages.join(", ");
        } else {
          this.info = error.response?.data?.detail || "Login failed...";
        }
      }
    },
    goToForgotPassword() {
      this.$router.push({ name: "forgot-password" });
    },
  },
});
</script>

<template>
  <div class="auth-form-container my-6">
    <form @submit.prevent="handleLogin" class="auth-form">
      <fieldset>
        <legend>Login</legend>

        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            minlength="8"
            required
          />
        </div>

        <div class="flex justify-between items-center w-full">
          <button
            type="button"
            @click="goToForgotPassword"
            class="text-blue-600 hover:underline text-sm font-medium"
          >
            Forgot your password?
          </button>

          <button type="submit" class="button button-green">Login</button>
        </div>
      </fieldset>
    </form>

    <div v-if="info" class="text-center text-red-500 my-6">{{ info }}</div>
  </div>
</template>

<style>
@import "./auth_form.css";
</style>
