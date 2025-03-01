<script>
import { useUsersStore } from '../store/users'; 
import { useRouter } from 'vue-router';
import { ref } from 'vue';

export default {
  setup() {
    const userStore = useUsersStore(); //don't ask my why i use const and ref :)
    const router = useRouter();
    const email = ref("");
    const password = ref("");
    const login = () => {
      if (email.value === userStore.user_email && password.value === userStore.user_password) {
        
        userStore.setUsersData({
          first_name: userStore.first_name,
          second_name: userStore.second_name,
          user_email: email.value,
          user_password: password.value,
        });
        router.push('/'); 
      } else {
        alert("wrong Login or Password");
      }
    };

    return { email, password, login };
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








