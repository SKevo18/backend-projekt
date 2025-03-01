<script lang="ts">
import "./main.css"
import HeaderComponent from "./components/HeaderComponent.vue"

export default {
  name: "App",
  components: {
    HeaderComponent
  }
}
</script>

<template>
  <HeaderComponent />
  <router-view />
</template>
