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
        <legend>Registrácia</legend>

        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required />
        </div>

        <div class="form-group">
          <label for="password">Heslo</label>
          <input type="password" id="password" v-model="password" required />
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

<style scoped>
@import "tailwindcss";

.form-container {
  @apply max-w-md my-20 mx-auto;
}

.info-container {
  @apply max-w-md my-20 mx-auto;
}
</style>
