import { usePagesStore } from "@/store/pageStore";
import NotFoundView from "@/views/NotFoundView.vue";
import PageReadView from "@/views/page/PageReadView.vue";
import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/store/authStore";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/views/page/CategoryRedirectView.vue"),
      beforeEnter: async (_, __, next) => {
        const pagesStore = usePagesStore();

        if (pagesStore.categories.length === 0) {
          await pagesStore.fetchCategories();
        }

        if (pagesStore.categories.length > 0) {
          // redirect to first category
          next({
            name: "category",
            params: { category: pagesStore.categories[0].id },
          });
        } else {
          next(); // show page with empty sidebar
        }
      },
    },
    {
      path: "/:category",
      component: () => import("@/views/page/CategoryRedirectView.vue"),
      props: true,
      name: "category",
    },
    {
      path: "/page/:idSlug",
      component: PageReadView,
      props: true,
      name: "page",
    },
    {
      path: "/page/:idSlug/edit",
      name: "page-edit",
      component: () => import("@/views/page/PageEditView.vue"),
      props: true,
      meta: { requiresEditorOrAdmin: true},
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
      path: "/forgot-password",
      name: "forgot-password",
      component: () => import("@/views/auth/ForgotPasswordView.vue"),
    },
    {
      path: "/reset-password",
      name: "reset-password",
      component: () => import("@/views/auth/ResetPasswordView.vue"),
    },
    {
      path: "/profile",
      name: "profile",
      component: () => import("@/views/user/ProfileView.vue"),
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


router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresEditorOrAdmin) {
    if (!authStore.user && authStore.hasToken) {
      await authStore.fetchUserData();
    }

    if (!authStore.user || !(authStore.user.role === 1 || authStore.user.role === 2)) {
      return next({ name: "login" });
    }
  }

  next();
});


export default router;
