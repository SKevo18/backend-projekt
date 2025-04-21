import { defineStore } from "pinia";
import api from "@/services/api";

interface User {
  id: number;
  first_name: string;
  last_name: string;
  user_email: string;
  role: number;
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as User | null,
    token: localStorage.getItem("token") ?? null,
  }),

  getters: {
    hasToken: (state) => state.token !== null,
    isAuthenticated: (state) => state.user !== null,
    isAdmin: (state) => state.user?.role === 2,
  },

  actions: {
    loadSavedToken() {
      this.token = localStorage.getItem("token") ?? null;
      if (this.token) {
        api.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;
      }
    },

    async register(
      first_name: string,
      last_name: string,
      email: string,
      password: string,
      confirmPassword: string
    ) {
      if (password !== confirmPassword) {
        return {
          success: false,
          msg: "Passwords do not match",
        };
      }

      const response = await api.post(
        "/authentication/register",
        {
          first_name,
          last_name,
          user_email: email,
          user_password: password,
        }
      );
      this.token = response.data.access_token;
      localStorage.setItem("token", this.token);
      api.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;
      await this.fetchUserData();
      return response;
    },

    async login(email: string, password: string) {
      const response = await api.post(
        "/authentication/login",
        {
          user_email: email,
          user_password: password,
        }
      );
      this.token = response.data.access_token;
      localStorage.setItem("token", this.token);
      api.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;
      await this.fetchUserData();
      return response;
    },

    async fetchUserData() {
      if (!this.token) return;
      try {
        const response = await api.get(
          "/authentication/me",
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
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
      api.defaults.headers.common["Authorization"] = "";
      // TODO: also send request to invalidate token on backend
    },
  },
});
