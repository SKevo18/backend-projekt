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
      path: "/page/:id",
      component: PageReadView,
      props: true,
      name: "page",
    },
    {
      path: "/:year/:id/edit",
      name: "page-edit",
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
          component: () => import("@/views/admin/AdminSettingsView.vue"),
        },
        {
          path: "users",
          name: "admin-users",
          component: () => import("@/views/admin/AdminUsersView.vue"),
        },
        {
          path: "pages",
          name: "admin-pages",
          component: () => import("@/views/admin/AdminPagesView.vue"),
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
