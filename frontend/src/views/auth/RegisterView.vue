<script lang="ts">
import { defineComponent, ref } from "vue";
import { useAuthStore } from "@/store/authStore";
import api from "@/services/api";
import TurnstileComponent from "@/components/TurnstileComponent.vue";

export default defineComponent({
  name: "RegisterView",
  components: {
    TurnstileComponent,
  },
  data() {
    return {
      first_name: "",
      last_name: "",
      email: "@",
      password: "",
      confirmPassword: "",
      registeredSuccessfully: null as boolean | null,
      errorInfo: "Unknown error",
      authStore: useAuthStore(),
    };
  },
  methods: {
    async handleRegister() {
      try {
        const turnstileRef = this.$refs.turnstileRef as any;
        if (!turnstileRef?.hasToken?.value && turnstileRef?.siteKey?.value) {
          this.errorInfo = "Please complete the CAPTCHA verification";
          this.registeredSuccessfully = false;
          return;
        }

        const turnstileToken = turnstileRef?.getToken() || "";

        let response = await this.authStore.register(
          this.first_name,
          this.last_name,
          this.email,
          this.password,
          this.confirmPassword,
          turnstileToken
        );
        this.registeredSuccessfully = response.status === 200;
      } catch (error) {
        if (
          error.response?.data?.detail &&
          Array.isArray(error.response.data.detail)
        ) {
          const errorMessages = error.response.data.detail.map(
            (err) => err.msg
          );
          this.errorInfo = errorMessages.join(", ");
        } else {
          this.errorInfo = error.response?.data?.detail || "Unknown error...";
        }
        this.registeredSuccessfully = false;
      }
    },
  },
});
</script>

<template>
  <div class="form-container my-6" v-if="registeredSuccessfully === null">
    <form @submit.prevent="handleRegister" class="auth-form">
      <fieldset>
        <legend>Register</legend>

        <div class="form-group">
          <label for="first_name">First name</label>
          <input type="text" id="first_name" v-model="first_name" required />
        </div>

        <div class="form-group">
          <label for="last_name">Last name</label>
          <input type="text" id="last_name" v-model="last_name" required />
        </div>

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

        <div class="form-group">
          <label for="confirmPassword">Confirmation password </label>
          <input
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            required
          />
        </div>

        <TurnstileComponent ref="turnstileRef" />

        <button class="button button-green" type="submit">Register</button>
      </fieldset>
    </form>
  </div>

  <div class="info-container" v-else-if="registeredSuccessfully">
    <div class="success">
      <h1>
        You have successfully registered!<br />
        Please check your email for verification.
      </h1>
    </div>
  </div>

  <div class="info-container" v-else>
    <div class="error">
      <h1>
        Registration failed: {{ errorInfo }}<br />
        Please try again later.
      </h1>
    </div>
  </div>
</template>

<style>
@import "./auth_form.css";
</style>
