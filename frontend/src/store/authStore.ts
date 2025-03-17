import { defineStore } from "pinia";

interface User {
  id: number;
  name: string;
  email: string;
}

// TODO: connect to backend
export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as User | null,
    token: null as string | null,
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

      // this.user = await this.fetchJsonAuth("/me");
      const response = await fetch(
        "https://jsonplaceholder.typicode.com/users"
      );
      const data = await response.json();
      this.user = data[0];
      //
    },

    async login(email: string, password: string): Promise<boolean> {
      const response = await fetch(
        "https://jsonplaceholder.typicode.com/users"
      );
      const data = await response.json();

      this.user = data[0];
      this.setToken(data[0].email);

      return true;
    },

    async register(
      email: string,
      password: string,
      confirmPassword: string
    ): Promise<boolean> {
      if (password !== confirmPassword) {
        throw new Error("Passwords do not match");
      }

      /*const response = await fetch(
        "https://jsonplaceholder.typicode.com/users"
      );
      return response.ok;*/

      return true;
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

    async fetchJson(url: string, options: RequestInit = {}): Promise<any> {
      const response = await fetch(url, options);
      return response.json();
    },

    async fetchJsonAuth(url: string, options: RequestInit = {}): Promise<any> {
      if (this.token === null) {
        return null;
      }

      return this.fetchJson(url, {
        headers: {
          Authorization: `Bearer ${this.token}`,
        },
        ...options,
      });
    },
  },
});
