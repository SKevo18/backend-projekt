<script lang="ts" setup>
import { ref } from "vue";
import api from "@/services/api";

const smtpHost = ref("");
const smtpPort = ref(587);
const smtpUsername = ref("");
const smtpPassword = ref("");

const testEmailStatus = ref("");

const registrationEnabled = ref(false);

const saveSmtpSettings = async () => {
  const payload = {
    smtp_host: smtpHost.value,
    smtp_port: smtpPort.value,
    email_sender: smtpUsername.value,
    email_password: smtpPassword.value,
  };

  try {
    console.log("Payload:", payload);

    const response = await api.post("/email/save_smtp", payload);

    if (response.status == 200) {
      alert("SMTP nastavenia boli uložené.");
    } else {
      alert("Chyba pri ukladaní.");
    }
  } catch (error: any) {
    if (error.response) {
      console.error("Server error:", error.response.data);
      alert("Chyba pri ukladaní: " + error.response.data.detail);
    } else {
      console.error("Network error:", error);
      alert("Chyba pripojenia k serveru.");
    }
  }
};

const sendTestEmail = async () => {
  testEmailStatus.value = "";
  try {
    const response = await api.post("/email/send_test_email");

    if (response.status == 200) {
      testEmailStatus.value = "Testovací email bol odoslaný.";
    } else {
      testEmailStatus.value = "Chyba pri odosielaní testovacieho emailu:.";
    }
  } catch (error: any) {
    testEmailStatus.value = error.response?.data?.detail;
    console.error(error);
  }
};
</script>

<template>
  <div class="flex flex-col">
    <div class="admin-forms admin-forms-grid">
      <fieldset class="form-container">
        <legend>SMTP</legend>

        <div class="form-group">
          <label for="smtp-host">SMTP Host</label>
          <input
            v-model="smtpHost"
            type="text"
            id="smtp-host"
            placeholder="smtp.gmail.com"
          />
        </div>

        <div class="form-group">
          <label for="smtp-port">SMTP Port</label>
          <input
            v-model.number="smtpPort"
            type="number"
            id="smtp-port"
            placeholder="587"
          />
        </div>

        <div class="form-group">
          <label for="smtp-username">SMTP Username</label>
          <input
            v-model="smtpUsername"
            type="text"
            id="smtp-username"
            placeholder="meno@gmail.com"
          />
        </div>

        <div class="form-group">
          <label for="smtp-password">SMTP Password</label>
          <input
            v-model="smtpPassword"
            type="password"
            id="smtp-password"
            placeholder="••••••••"
          />
        </div>

        <button
          class="py-1 px-3 bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm rounded-lg shadow transition"
          @click="sendTestEmail"
        >
          Odoslať test email
        </button>
      </fieldset>

      <fieldset class="form-container">
        <legend>Ostatné</legend>

        <div class="form-checkbox">
          <input
            v-model="registrationEnabled"
            type="checkbox"
            id="registration-enabled"
          />
          <label for="registration-enabled">Povoliť nové registrácie</label>
        </div>
      </fieldset>
    </div>

    <div class="flex justify-between items-end mt-4">
      <button class="button button-green" @click="saveSmtpSettings">
        Uložiť
      </button>
    </div>

    <p
      v-if="testEmailStatus"
      class="mt-2 text-sm font-medium"
      :class="
        testEmailStatus.startsWith('T') ? 'text-green-600' : 'text-red-600'
      "
    >
      {{ testEmailStatus }}
    </p>
  </div>
</template>
