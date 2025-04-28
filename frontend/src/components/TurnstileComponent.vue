<script lang="ts" setup>
import { ref, onMounted, defineExpose, computed } from "vue";
import api from "@/services/api";

declare global {
  interface Window {
    turnstile: any;
  }
}

const turnstileToken = ref<string>("");
const siteKey = ref<string>("");

const getToken = (): string => {
  return turnstileToken.value;
};

const hasToken = computed(() => {
  return !!turnstileToken.value;
});

const loadTurnstile = () => {
  if (!document.getElementById("cloudflare-turnstile")) {
    const script = document.createElement("script");
    script.id = "cloudflare-turnstile";
    script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js";
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);

    script.onload = () => {
      renderTurnstile();
    };
  } else {
    renderTurnstile();
  }
};

const renderTurnstile = () => {
  if (window.turnstile && siteKey.value) {
    window.turnstile.render("#turnstile-container", {
      sitekey: siteKey.value,
      callback: (token: string) => {
        turnstileToken.value = token;
      },
    });
    console.log("Turnstile ready");
  }
};

onMounted(async () => {
  try {
    const response = await api.get("/settings/turnstile-key");
    siteKey.value = response.data.turnstile_site_key;
    if (siteKey.value) {
      loadTurnstile();
    }
  } catch (err) {
    console.error("Failed to load site key:", err);
  }
});

defineExpose({
  getToken,
  hasToken,
  siteKey,
});
</script>

<template>
  <div class="form-group" v-if="siteKey">
    <div id="turnstile-container"></div>
  </div>
</template>
