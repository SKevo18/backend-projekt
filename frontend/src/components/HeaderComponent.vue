<script lang="ts">
export default {
  name: "HeaderComponent",
  
}
</script>

<template>
  <nav class="nav">
    <div class="nav-container">
      <div class="logo">nConnect</div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Domov</router-link>
        <router-link to="/login" class="nav-link">Login</router-link>
        <router-link to="/register" class="nav-link">Registrácia</router-link>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: #007bff;
  padding: 15px 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 15px;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  padding: 8px 12px;
  border-radius: 5px;
  transition: background 0.3s;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.2);
}

body {
  padding-top: 70px;
}
</style>
