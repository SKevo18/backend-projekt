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
        if (response.success) {
          this.$router.push("/");
        } else {
          this.info = response.data.msg;
        }
      } catch (error) {
        if (
          error.response?.data?.detail &&
          Array.isArray(error.response.data.detail)
        ) {
          const errorMessages = error.response.data.detail.map(
            (err) => err.msg
          );
          this.info = errorMessages.join(", ");
        } else {
          this.info = error.response?.data?.detail || "Prihlásenie zlyhalo...";
        }
      }
    },
  },
});
</script>

<template>
  <div class="auth-form-container my-6">
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

    <div v-if="info" class="text-center text-red-500 my-6">{{ info }}</div>
  </div>
</template>

<style>
@import "./auth_form.css";
</style>
