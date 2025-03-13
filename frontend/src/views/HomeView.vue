<script setup>
import { useUsersStore } from "../store/users";
import { useRouter } from "vue-router";
import FooterComponent from "../components/FooterComponent.vue";
import SideBar from "../components/SideBar.vue";

const userStore = useUsersStore();
const router = useRouter();

// take first_name and surname
const firstName = userStore.first_name;
const secondName = userStore.second_name;

//logout user
const logout = () => {
  userStore.clearUsersData();
  router.push("/login"); // user catapult login page
};
</script>

<template>
  <div class="home-container">
    <SideBar />
    <div class="home">
      <div class="hero">
        <h1 v-if="firstName && secondName">
          Welcome, {{ firstName }} {{ secondName }}!
        </h1>
        <h1 v-else>Welcome to MyApp!</h1>
        <p v-if="!firstName || !secondName">
          For full access, please log in or register.
        </p>
        <router-link to="/login" v-if="!firstName || !secondName" class="btn">Login</router-link>
        <router-link to="/register" v-if="!firstName || !secondName" class="btn btn-alt">Registration</router-link>
        <button v-if="firstName && secondName" @click="logout" class="btn btn-alt">
          Logout
        </button>
      </div>
    </div>
  </div>
  <FooterComponent />
</template>

<style scoped>
.home-container {
  display: flex;
  min-height: 100vh;
}

.home {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: linear-gradient(to right, #007bff, #00c6ff);
  color: white;
}

.hero {
  max-width: 600px;
  padding: 20px;
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