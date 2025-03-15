<script lang="ts">
import SidebarComponent from "@/components/SidebarComponent.vue";

export default {
  name: "HomeView",
  components: {
    SidebarComponent,
  },
};
</script>

<template>
  <div class="content">
    <SidebarComponent />
    <h1>Home</h1>
  </div>
</template>
