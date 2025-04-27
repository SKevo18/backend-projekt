<script lang="ts" setup>
import { ref, onMounted } from "vue";
import api from "@/services/api";

interface Settings {
  smtp_host: string;
  smtp_port: number;
  email_sender: string | null;
  email_password: string | null;
  turnstile_site_key: string | null;
  turnstile_secret_key: string | null;
}

const smtpHost = ref("");
const smtpPort = ref(587);
const smtpUsername = ref("");
const smtpPassword = ref("");
const turnstileSiteKey = ref("");
const turnstileSecretKey = ref("");

const infoText = ref("");

const registrationEnabled = ref(false);

const saveSettings = async () => {
  infoText.value = "";
  const payload = {
    smtp_host: smtpHost.value,
    smtp_port: smtpPort.value,
    email_sender: smtpUsername.value,
    email_password: smtpPassword.value,
    turnstile_site_key: turnstileSiteKey.value,
    turnstile_secret_key: turnstileSecretKey.value,
  };

  try {
    const response = await api.post("/settings/save", payload);

    if (response.status === 200) {
      infoText.value = "Nastavenia boli úspešne uložené.";
    } else {
      infoText.value = "Chyba pri ukladaní nastavení.";
    }
  } catch (error: any) {
    if (error.response) {
      console.error("Server error:", error.response.data);
      infoText.value =
        "Chyba pri ukladaní nastavení: " + error.response.data.detail;
    } else {
      console.error("Network error:", error);
      infoText.value = "Chyba pripojenia k serveru.";
    }
  }
};

const sendTestEmail = async () => {
  infoText.value = "";
  try {
    const response = await api.post("/email/send_test_email");

    if (response.status == 200) {
      infoText.value = response.data.message;
    } else {
      infoText.value = `Error sending test email: ${
        response?.data?.detail || "Unknown error"
      }`;
    }
  } catch (error: any) {
    infoText.value = `Error sending test email: ${
      error.response?.data?.detail || "Unknown error"
    }`;
    console.error(error);
  }
};

onMounted(async () => {
  try {
    const response = await api.get("/settings");
    const data = response.data as Settings | null;

    smtpHost.value = data?.smtp_host ?? "";
    smtpPort.value =
      data?.smtp_port && data.smtp_port !== 0 ? data.smtp_port : 587;
    smtpUsername.value = data?.email_sender ?? "";
    smtpPassword.value = data?.email_password ?? "";
    turnstileSiteKey.value = data?.turnstile_site_key ?? "";
    turnstileSecretKey.value = data?.turnstile_secret_key ?? "";
  } catch (error) {
    console.error("Error loading settings:", error);
  }
});
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
        <legend>Cloudflare Turnstile</legend>

        <div class="form-group">
          <label for="turnstile-site-key">Site Key</label>
          <input
            v-model="turnstileSiteKey"
            type="text"
            id="turnstile-site-key"
            placeholder="1x00000000000000000000AA"
          />
        </div>

        <div class="form-group">
          <label for="turnstile-secret-key">Secret Key</label>
          <input
            v-model="turnstileSecretKey"
            type="password"
            id="turnstile-secret-key"
            placeholder="1x00000000000000000000AA"
          />
        </div>
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
      <button class="button button-green" @click="saveSettings">Uložiť</button>
    </div>

    <p
      v-if="infoText"
      class="mt-2 text-sm font-medium"
      :class="
        infoText.startsWith('T') || infoText.startsWith('Nastavenia boli')
          ? 'text-green-600'
          : 'text-red-600'
      "
    >
      {{ infoText }}
    </p>
  </div>
</template>
