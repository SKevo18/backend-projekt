<script lang="ts">
import { useUsersStore } from '../store/users'; 
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      email: "",
      password: ""
    }
  },
  methods: {
    login() {
      if (this.email === this.userStore.user_email && this.password === this.userStore.user_password) {
        
        this.userStore.setUsersData({
          first_name: this.userStore.first_name,
          second_name: this.userStore.second_name,
          user_email: this.email,
          user_password: this.password,
        });
        this.router.push('/'); 
      } else {
        alert("wrong Login or Password");
      }
    }
  },
  setup() {
    const userStore = useUsersStore();
    const router = useRouter();
    return { userStore, router };
  },
};
</script>

<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>Sign in</h2>
      <form @submit.prevent="login">
        <input type="email" placeholder="Email" v-model="email" required autocomplete="email" />
        <input type="password" placeholder="password" v-model="password" required autocomplete="current-password" />
        <button type="submit">Sign in</button>
      </form>
      <p>Don’t have an account? <router-link to="/register">Sign Up</router-link></p>
    </div>
  </div>
</template>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.auth-box {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 300px;
  text-align: center;
}

.auth-box input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.auth-box button {
  width: 100%;
  padding: 10px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.auth-box button:hover {
  background: #0056b3;
}
</style>








