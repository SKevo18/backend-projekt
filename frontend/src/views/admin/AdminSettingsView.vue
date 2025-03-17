<script lang="ts">
export default {
  name: "AdminSettingsView",
};
</script>

<template>
  <div class="flex flex-col">
    <div class="admin-forms admin-forms-grid">
      <fieldset class="form-container">
        <legend>SMTP</legend>

        <div class="form-group">
          <label for="smtp-host">SMTP Host</label>
          <input type="text" id="smtp-host" placeholder="smtp.gmail.com" />
        </div>

        <div class="form-group">
          <label for="smtp-port">SMTP Port</label>
          <input type="number" id="smtp-port" placeholder="587" />
        </div>

        <div class="form-group">
          <label for="smtp-username">SMTP Username</label>
          <input type="text" id="smtp-username" placeholder="meno@gmail.com" />
        </div>

        <div class="form-group">
          <label for="smtp-password">SMTP Password</label>
          <input type="password" id="smtp-password" placeholder="••••••••" />
        </div>
      </fieldset>

      <fieldset class="form-container">
        <legend>Ostatné</legend>

        <div class="form-checkbox">
          <input type="checkbox" id="registration-enabled" />
          <label for="registration-enabled">Povoliť nové registrácie</label>
        </div>
      </fieldset>
    </div>

    <button class="button button-green mt-4 self-end">Uložiť</button>
  </div>
</template>
