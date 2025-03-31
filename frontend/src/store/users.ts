import { defineStore } from "pinia";

export const useUsersStore = defineStore("users", {
  state: () => ({
    first_name: localStorage.getItem("first_name") || "",
    last_name: localStorage.getItem("last_name") || "",
    user_email: localStorage.getItem("user_email") || "",
    user_password: sessionStorage.getItem("user_password") || "",
  }),

  actions: {
    setUsersData(data: Record<string, string>) {
      console.log("Setting user data:", data);
      Object.keys(data).forEach((key) => {
        if (key in this) {
          this[key] = data[key];
          if (key === "user_password") {
            sessionStorage.setItem(key, data[key]);
          } else {
            localStorage.setItem(key, data[key]);
          }
        }
      });
    },

    clearUsersData() {
      console.log("Clearing user data");
      Object.assign(this, {
        first_name: "",
        last_name: "",
        user_email: "",
        user_password: "",
      });

      ["first_name", "last_name", "user_email"].forEach((key) =>
        localStorage.removeItem(key)
      );
      sessionStorage.removeItem("user_password");
    },
  },
});
