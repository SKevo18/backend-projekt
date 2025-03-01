<script lang="ts">
import { useUsersStore } from '../store/users';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      first_name: '',
      second_name: '',
      user_email: '',
      user_password: '',
      confirm_password: '',
    };
  },
  setup() {
    const userStore = useUsersStore();
    const router = useRouter(); 
    return { userStore, router };
  },
  computed: {
    isPasswordValid(): boolean {
      return this.user_password === this.confirm_password
    }
  },
  methods: {
    register() {
      if (!this.isPasswordValid) {
        alert("Password not match!");
        return;
      }

      this.userStore.setUsersData({
        first_name: this.first_name,
        second_name: this.second_name,
        user_email: this.user_email,
        user_password: this.user_password,
      });

      this.router.push('/'); // redirect user to main page
    },
  },
};
</script>

<template>
    <div class="auth-container">
      <div class="auth-box">
        <h2>Registration</h2>
        <form @submit.prevent="register">
          <input type="text" placeholder="Kevin" v-model="first_name" required />
          <input type="text" placeholder="Svitač" v-model="second_name" required />
          <input type="email" placeholder="kichatyisebastian@gmail.com" v-model="user_email"  autocomplete="email" required />
          <input type="password" placeholder="Password" v-model="user_password" autocomplete="current-password" required />
          <input type="password" placeholder="Confirm password" v-model="confirm_password" required />
          <button type="submit">Registration</button>
        </form>
        <p>Already have an account? <router-link to="/login">Sign In</router-link></p>
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
