import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/login", component: () => import("../views/LoginView.vue") },
  { path: "/register", component: () => import("../views/RegisterView.vue") },
  { path: "/contact", component: () => import("../views/ContactView.vue") },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
