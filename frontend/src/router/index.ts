import { createRouter, createWebHistory } from "vue-router";
import PageReadView from "@/views/page/PageReadView.vue";
import NotFoundView from "@/views/NotFoundView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: `/${new Date().getFullYear()}`,
      name: "home",
    },
    {
      path: "/:year",
      component: PageReadView,
      props: true,
      name: "year",
    },
    {
      path: "/:year/:slug",
      component: PageReadView,
      props: true,
      name: "page",
    },
    {
      path: "/:year/:slug/edit",
      name: "page-edit",
      // UMO editor has * { margin: 0; padding: 0; } CSS, must be dynamically loaded
      component: () => import("@/views/page/PageEditView.vue"),
      props: true,
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/auth/LoginView.vue"),
    },
    {
      path: "/register",
      name: "register",
      component: () => import("@/views/auth/RegisterView.vue"),
    },
    {
      path: "/admin",
      name: "admin",
      component: () => import("@/views/admin/AdminView.vue"),
      redirect: "/admin/settings",
      children: [
        {
          path: "settings",
          name: "admin-settings",
          component: () => import("@/views/admin/SettingsView.vue"),
        },
        {
          path: "users",
          name: "admin-users",
          component: () => import("@/views/admin/UsersView.vue"),
        },
        {
          path: "sidebar",
          name: "admin-sidebar",
          component: () => import("@/views/admin/SidebarView.vue"),
        },
      ],
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: NotFoundView,
    },
  ],
});

export default router;
