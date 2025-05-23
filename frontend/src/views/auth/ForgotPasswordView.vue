<script lang="ts" setup>
import { ref } from "vue";
import api from "@/services/api";
import TurnstileComponent from "@/components/TurnstileComponent.vue";

const email = ref("");
const message = ref("");
const error = ref("");
const turnstileRef = ref(null);

const sendEmail = async () => {
  message.value = "";
  error.value = "";

  if (
    !turnstileRef.value?.hasToken?.value &&
    turnstileRef.value?.siteKey?.value
  ) {
    error.value = "Please complete the CAPTCHA verification.";
    return;
  }

  try {
    const response = await api.post("/email/password_reset", {
      email: email.value,
      turnstile_token: turnstileRef.value?.getToken() || "",
    });

    message.value = `A password reset link has been sent to your email.`;
  } catch (err: any) {
    if (err.response.status === 404) {
      error.value = "User with this email does not exist.";
    } else {
      error.value = "There was an error when sending the email.";
    }
    console.error(err);
  }
};
</script>

<template>
  <div class="auth-form-container">
    <form class="auth-form" @submit.prevent="sendEmail">
      <fieldset>
        <legend>Reset password</legend>

        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required />
        </div>

        <TurnstileComponent ref="turnstileRef" />

        <button type="submit" class="button button-green">Send e-mail</button>

        <p v-if="message" class="text-green-600 mt-2">{{ message }}</p>
        <p v-if="error" class="text-red-600 mt-2">{{ error }}</p>
      </fieldset>
    </form>
  </div>
</template>

<style>
@import "./auth_form.css";
</style>
