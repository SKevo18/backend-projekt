import { defineStore } from "pinia";

// TODO: connect to backend
export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: null,
  }),

  getters: {
    hasToken: (state) => state.token !== null,
    isAuthenticated: (state) => state.user !== null,
  },

  actions: {
    async fetchUserData() {
      if (this.token === null) {
        return;
      }

      const response = await fetch(
        "https://jsonplaceholder.typicode.com/users"
      );
      const data = await response.json();
      this.user = data[0];
    },

    async login(email: string, password: string) {
      const response = await fetch(
        "https://jsonplaceholder.typicode.com/users"
      );
      const data = await response.json();

      this.user = data[0];
      this.setToken(data[0].email);
    },

    async logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem("token");

      // TODO: also invalidate token on backend
    },

    setToken(token: string) {
      this.token = token;
      localStorage.setItem("token", token);
    },
    loadSavedToken() {
      this.token = localStorage.getItem("token");
    },
  },
});
