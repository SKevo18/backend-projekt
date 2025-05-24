<script lang="ts" setup>
import { ref, onMounted, onUnmounted, defineExpose, computed } from "vue";
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
  const container = document.getElementById("turnstile-container");
  if (container) {
    container.innerHTML = "";
  }
  if (window.turnstile && siteKey.value && container) {
    window.turnstile.render(container, {
      sitekey: siteKey.value,
      callback: (token: string) => {
        turnstileToken.value = token;
      },
    });
    console.log("Turnstile ready");
  }
};

const cleanupTurnstile = () => {
  turnstileToken.value = "";
  const container = document.getElementById("turnstile-container");
  if (container) {
    container.innerHTML = "";
  }

  // important to ensure proper cleanup:
  const script = document.getElementById("cloudflare-turnstile");
  if (script) script.remove();
};

onMounted(async () => {
  try {
    const response = await api.get("/settings/turnstile-key");
    siteKey.value = (response.data as { turnstile_site_key: string }).turnstile_site_key;
    if (siteKey.value) {
      loadTurnstile();
    }
  } catch (err) {
    console.error("Failed to load site key:", err);
  }
});

onUnmounted(() => {
  cleanupTurnstile();
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
