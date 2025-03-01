<script setup>
import { useUsersStore } from '../store/users';
import { useRouter } from 'vue-router';

const userStore = useUsersStore();
const router = useRouter();

// take first_name and surname
const firstName = userStore.first_name;
const secondName = userStore.second_name;

//logout user
const logout = () => {
  userStore.clearUsersData();
  router.push('/login'); // user catapult login page
};
</script>

<template>
  <div class="home">
    <div class="hero">
      <h1 v-if="firstName && secondName">Добро пожаловать, {{ firstName }} {{ secondName }}!</h1>
      <h1 v-else>Welcome to MyApp!</h1>
      <!-- space Elon Mask-->
      <p v-if="!firstName || !secondName">Для полного доступа войдите или зарегистрируйтесь.</p>
      <p v-else>Super-Duper-2025-Backend-Project-Initial-GitHub-Europe-Herous-Commit.</p>
      <!-- space Elon Mask-->
      <router-link to="/login" v-if="!firstName || !secondName" class="btn">Login</router-link>
      <router-link to="/register" v-if="!firstName || !secondName" class="btn btn-alt">Registration</router-link>
      <!-- space Elon Mask-->
      <button v-if="firstName && secondName" @click="logout" class="btn btn-alt">Logout</button>
    </div>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh);
  text-align: center;
  background: linear-gradient(to right, #007bff, #00c6ff);
  color: white;
}

.hero {
  max-width: 600px;
  padding: 20px;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

p {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.btn {
  display: inline-block;
  margin: 10px;
  padding: 10px 20px;
  font-size: 1.2rem;
  color: white;
  background: #28a745;
  border-radius: 5px;
  text-decoration: none;
  transition: 0.3s;
}

.btn-alt {
  background: #ff9800;
}

.btn:hover {
  opacity: 0.8;
}

button {
  display: inline-block;
  margin: 10px;
  padding: 10px 20px;
  font-size: 1.2rem;
  color: white;
  background: #ff9800;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  opacity: 0.8;
}
</style>


