<script lang="ts">
import { defineComponent } from "vue";
import { useAuthStore } from "@/store/authStore";

export default defineComponent({
  name: "RegisterView",
  data() {
    return {
      first_name: "",
      last_name: "",
      email: "@",
      password: "",
      confirmPassword: "",
      registeredSuccessfully: null as boolean | null,
      authStore: useAuthStore(),
    };
  },
  methods: {
    async handleRegister() {
        this.registeredSuccessfully = await this.authStore.register(
        this.first_name,
        this.last_name,
        this.email,
        this.password,
        this.confirmPassword
      );
    },
  },
});
</script>

<template>
  <div class="form-container" v-if="registeredSuccessfully === null">
    <form @submit.prevent="handleRegister" class="auth-form">
      <fieldset>
        <legend>Registrácia</legend>

        <div class="form-group">
          <label for="first_name">Meno</label>
          <input 
          type="text" 
          id="first_name" 
          v-model="first_name" 
          required 
          />
        </div>

        <div class="form-group">
          <label for="last_name">Priezvisko </label>
          <input 
          type="text" 
          id="last_name" 
          v-model="last_name" 
          required 
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input 
          type="email" 
          id="email" 
          v-model="email" 
          required />
        </div>

        <div class="form-group">
          <label for="password">Heslo</label>
          <input 
          type="password" 
          id="password" 
          v-model="password" 
          required 
          />
        </div>

        <div class="form-group">
          <label for="confirmPassword">Potvrdenie hesla</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            required 
            />
        </div>

        <button class="button button-green" type="submit">Registrovať</button>
      </fieldset>
    </form>
  </div>

  <div class="info-container" v-else-if="registeredSuccessfully">
    <div class="success">
      <h1>
        Úspešne ste sa registrovali!<br />
        Skontrolujte si e-mail pre overenie.
      </h1>
    </div>
  </div>

  <div class="info-container" v-else>
    <div class="error">
      <h1>
        Registrácia zlyhala.<br />
        Prosím, skúste to znova neskôr.
      </h1>
    </div>
  </div>
</template>

<style>
@import "./auth_form.css";
</style>
