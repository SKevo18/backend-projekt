<script lang="ts" setup>
import { ref } from "vue";
import api from "@/services/api";

const email = ref("");
const message = ref("");
const error = ref("");

const sendEmail = async () => {
  message.value = "";
  error.value = "";

  try {
    const response = await api.post("/email/password_reset", {
      email: email.value,
    });

    if (response.status === 200) {
      message.value = `Na váš e-mail bol odoslaný odkaz na obnovenie hesla.`;
    } else {
      error.value = "Nastala chyba pri odosielaní e-mailu.";
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || "Chyba pri odosielaní e-mailu.";
    console.error(err);
  }
};
</script>

<template>
    <div class="auth-form-container">
        <form class="auth-form" @submit.prevent="sendEmail">
            <fieldset>
                <legend>Obnovenie hesla</legend>

                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" v-model="email" required />
                </div>

                <button type="submit" class="button button-green">
                    Odoslať e-mail
                </button>

                <p v-if="message" class="text-green-600 mt-2">{{ message }}</p>
                <p v-if="error" class="text-red-600 mt-2">{{ error }}</p>
            </fieldset>
        </form>
    </div>
</template>

<style>
@import "./auth_form.css";
</style>
