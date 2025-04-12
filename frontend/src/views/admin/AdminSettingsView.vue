<script lang="ts" setup>
import { ref } from 'vue'

const smtpHost = ref('')
const smtpPort = ref(587)
const smtpUsername = ref('')
const smtpPassword = ref('')

const testEmailStatus = ref('')

const registrationEnabled = ref(false)

const saveSmtpSettings = async () => {
  const payload = {
    smtp_host: smtpHost.value,
    smtp_port: smtpPort.value,
    email_sender: smtpUsername.value,
    email_password: smtpPassword.value,
  }

  try {
    console.log("Payload:", payload)

    const response = await fetch('http://localhost:8000/email/save_smtp', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    const result = await response.json()

    if (response.ok) {
      alert('SMTP nastavenia boli uložené.')
    } else {
      alert('Chyba pri ukladaní: ' + result.message || 'Neznáma chyba')
    }

  } catch (error) {
    alert('Chyba pripojenia k serveru.')
    console.error(error)
  }
}

const sendTestEmail = async () => {
  testEmailStatus.value = '' // очищаем перед новым запросом
  try {
    const response = await fetch('http://localhost:8000/email/send_test_email', {
      method: 'POST',
    })

    const result = await response.json()

    if (response.ok) {
      testEmailStatus.value = '✅ Testovací email bol odoslaný.'
    } else {
      testEmailStatus.value = '❌ Chyba pri odosielaní testovacieho emailu: ' + (result.message || 'Neznáma chyba.')
    }
  } catch (error) {
    testEmailStatus.value = '❌ Nepodarilo sa pripojiť k serveru.'
    console.error(error)
  }
}
</script>

<template>
  <div class="flex flex-col">
    <div class="admin-forms admin-forms-grid">
      <fieldset class="form-container">
        <legend>SMTP</legend>

        <div class="form-group">
          <label for="smtp-host">SMTP Host</label>
          <input v-model="smtpHost" type="text" id="smtp-host" placeholder="smtp.gmail.com" />
        </div>

        <div class="form-group">
          <label for="smtp-port">SMTP Port</label>
          <input v-model.number="smtpPort" type="number" id="smtp-port" placeholder="587" />
        </div>

        <div class="form-group">
          <label for="smtp-username">SMTP Username</label>
          <input v-model="smtpUsername" type="text" id="smtp-username" placeholder="meno@gmail.com" />
        </div>

        <div class="form-group">
          <label for="smtp-password">SMTP Password</label>
          <input v-model="smtpPassword" type="password" id="smtp-password" placeholder="••••••••" />
        </div>
      </fieldset>

      <fieldset class="form-container">
        <legend>Ostatné</legend>

        <div class="form-checkbox">
          <input v-model="registrationEnabled" type="checkbox" id="registration-enabled" />
          <label for="registration-enabled">Povoliť nové registrácie</label>
        </div>
      </fieldset>
    </div>

    <button class="button button-green mt-4 self-end" @click="saveSmtpSettings">
      Uložiť
    </button>

    <button
      class="button mt-2 self-end bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg shadow transition"
      @click="sendTestEmail">
      Odoslať testovací email
    </button>

    <p v-if="testEmailStatus" class="mt-2 text-sm font-medium"
      :class="testEmailStatus.startsWith('✅') ? 'text-green-600' : 'text-red-600'">
      {{ testEmailStatus }}
    </p>
  </div>
</template>
