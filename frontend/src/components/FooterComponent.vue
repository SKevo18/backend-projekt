<script lang="ts">
import LogoComponent from "@/components/LogoComponent.vue";

export default {
  name: "FooterComponent",
  components: {
    LogoComponent,
  },
};
</script>

<template>
  <footer>
    <div class="info">
      <div>
        <LogoComponent />
        <div class="flex-row">
          <p class="big">Animal Science Days</p>
          <a tabindex="-1" href="mailto:info@uniag.sk">info@uniag.sk</a>
        </div>
      </div>
      <div>
        <p>
          Slovenská Poľnohospodárska Univerzita<br />
          Tr. A. Hlinku 38<br />
          949 76 Nitra
        </p>
      </div>
    </div>

    <p class="copyright">
      &copy; {{ new Date().getFullYear() }} Animal Science Days
    </p>
  </footer>
</template>

<style scoped>
@import "tailwindcss";

footer {
  @apply text-white bg-gray-800 pt-6;
}

footer > .info {
  @apply flex flex-col sm:flex-row gap-4 justify-evenly;
}

footer > .info > div {
  @apply flex flex-col sm:flex-row gap-4 justify-center sm:justify-between items-center sm:items-start;
}

footer .copyright {
  @apply text-center py-4;
}
</style>
