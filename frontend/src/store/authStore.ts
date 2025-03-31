import { defineStore } from "pinia";
import axios from "axios";

interface User {
  id: number;
  first_name: string;  
  last_name: string; 
  email: string;
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as User | null,
    token: localStorage.getItem("token") ?? null,
  }),

  getters: {
    hasToken: (state) => state.token !== null,
    isAuthenticated: (state) => state.user !== null,
  },

  actions: {
    loadSavedToken() {
      this.token = localStorage.getItem("token") ?? null;
      if (this.token) {
        axios.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;
      }
    },

    async login(email: string, password: string): Promise<boolean> {
      try {
        const response = await axios.post("http://localhost:8000/authentication/login", {
          user_email: email,
          user_password: password,
        });
        this.token = response.data.access_token;
        localStorage.setItem("token", this.token);
        axios.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;
        await this.fetchUserData();
        return true;
      } catch (error) {
        console.error("Login Error:", error);
        return false;
      }
    },

    async register(firstName: string, lastName: string, email: string, password: string, confirmPassword: string): Promise<boolean> {
      if (password !== confirmPassword) {
        console.error("Passwords don't match");
        return false;
      }
      try {
        const response = await axios.post("http://localhost:8000/api/authentication/register", {
          first_name: firstName,    
          last_name: lastName,
          user_email: email,
          user_password: password,
          role: 0,
        });
        this.token = response.data.access_token;
        localStorage.setItem("token", this.token);
        axios.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;
        await this.fetchUserData();
        return true;
      } catch (error) {
        console.error("Registration Error:", error);
        return false;
      }
    },

    async fetchUserData() {
      if (!this.token) return;
      try {
        const response = await axios.get("http://localhost:8000/authentication/me", {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        });
        this.user = response.data;
      } catch (error) {
        console.error("Error while retrieving user data:", error);
        this.logout();
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem("token");
      axios.defaults.headers.common["Authorization"] = "";
    },
  },
});