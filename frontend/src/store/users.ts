import { defineStore } from "pinia";
import axios from 'axios'

export/* It seems like there is a typo in your code snippet. The line `co` is not a valid TypeScript
syntax or function call. If you provide more context or clarify the specific part of the code
you are referring to, I can help you understand or fix it. */
 const useUsersStore = defineStore("users", {
  state: () => ({
    first_name: localStorage.getItem("first_name") || "",
    last_name: localStorage.getItem("last_name") || "",
    user_email: localStorage.getItem("user_email") || "",
    user_password: sessionStorage.getItem("user_password") || "",
  }),

  actions: {
    setUsersData(data) {
      console.log("Setting user data:", data); // Логирование для отладки
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
      console.log("Clearing user data"); // Логирование для отладки
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
