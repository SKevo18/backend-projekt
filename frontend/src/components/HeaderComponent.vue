<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";
import LogoComponent from "@/components/LogoComponent.vue";
import { usePagesStore } from "@/store/pageStore";
import { useAuthStore } from "@/store/authStore";

export default defineComponent({
  name: "HeaderComponent",
  components: {
    RouterLink,
    LogoComponent,
  },
  setup() {
    const pagesStore = usePagesStore();
    const authStore = useAuthStore();
    const route = useRoute();
    const router = useRouter();

    const showCategories = computed(() => !route.meta.isAdminView);
    const categories = computed(() => pagesStore.categories);
    const sortedCategories = computed(() => {
      return [...categories.value].sort((a, b) =>
        a.title.localeCompare(b.title)
      );
    });

    const maxVisibleCategories = ref(8);
    const visibleCategories = computed(() =>
      sortedCategories.value.slice(0, maxVisibleCategories.value)
    );
    const hiddenCategories = computed(() =>
      sortedCategories.value.slice(maxVisibleCategories.value)
    );

    const logout = () => {
      authStore.logout();
      window.location.href = "/login";
    };

    const navigateToCategoryFromSelect = (event: Event) => {
      const selectElement = event.target as HTMLSelectElement;
      const categoryId = selectElement.value;
      if (categoryId) {
        router.push({ name: "category", params: { category: categoryId } });
        selectElement.value = "";
      }
    };

    onMounted(async () => {
      if (pagesStore.categories.length === 0) {
        await pagesStore.fetchCategories();
      }
    });

    watch(
      () => route.path,
      () => {}
    );

    const isCategoryActive = (categoryId: number) => {
      if (
        route.name === "category" &&
        route.params.category === categoryId.toString()
      ) {
        return true;
      }
      if (pagesStore.activePageCategoryId === categoryId) {
        return true;
      }
      return false;
    };

    return {
      pagesStore,
      authStore,
      logout,
      showCategories,
      visibleCategories,
      hiddenCategories,
      sortedCategories,
      navigateToCategoryFromSelect,
      isCategoryActive,
    };
  },
});
</script>

<template>
  <header class="app-header">
    <div class="header-topnav" v-if="!authStore.isAuthenticated">
      <RouterLink :to="{ name: 'login' }" active-class="nav-link-active"
        >Login</RouterLink
      >
      <span class="mx-2">|</span>
      <RouterLink :to="{ name: 'register' }" active-class="nav-link-active"
        >Register</RouterLink
      >
    </div>

    <div class="header-topnav" v-else>
      <div class="inline-block" v-if="authStore.isAdmin">
        <RouterLink
          :to="{ name: 'admin-settings' }"
          active-class="nav-link-active"
          >Administration</RouterLink
        >
        <span class="mx-2">|</span>
      </div>
      <RouterLink :to="{ name: 'profile' }" active-class="nav-link-active"
        >Profile</RouterLink
      >
      <span class="mx-2">|</span>
      <a class="logout-link" @click="logout">Logout</a>
    </div>

    <div class="header-content">
      <LogoComponent />
      <nav class="category-nav" v-if="showCategories">
        <RouterLink
          v-for="category in visibleCategories"
          :key="category.id"
          :to="{ name: 'category', params: { category: category.id } }"
          class="nav-link"
          :class="{ 'nav-link-active': isCategoryActive(category.id) }"
        >
          {{ category.title }}
        </RouterLink>

        <div v-if="hiddenCategories.length > 0" class="ml-2">
          <select
            @change="navigateToCategoryFromSelect"
            class="nav-link bg-gray-800 border border-gray-700 text-white text-sm rounded-md focus:ring-yellow-500 focus:border-yellow-500 cursor-pointer h-[34px] appearance-none pl-3 pr-8"
            style="
              background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23BBB%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E');
              background-repeat: no-repeat;
              background-position: right 0.5rem center;
              background-size: 0.8em auto;
            "
          >
            <option value="" class="text-gray-500">More...</option>
            <option
              v-for="category in hiddenCategories"
              :key="category.id"
              :value="category.id"
              class="bg-gray-700 text-white"
            >
              {{ category.title }}
            </option>
          </select>
        </div>
      </nav>
    </div>
  </header>
</template>

<style scoped>
@import "tailwindcss";

.header-topnav {
  @apply text-right text-sm text-white bg-green-900 py-1 pr-4;
}

.header-topnav a {
  @apply text-gray-200 hover:text-yellow-400;
}

.header-topnav .nav-link-active {
  @apply text-yellow-500;
}

.header-topnav .logout-link {
  @apply cursor-pointer hover:text-red-400;
}

.header-content {
  @apply bg-green-800 flex flex-col sm:flex-row justify-between items-center px-6 sm:px-10 space-x-0 sm:space-x-4 py-2;
}

.category-nav {
  @apply text-white p-2 sm:p-4 flex flex-wrap items-center justify-center sm:justify-start gap-3 sm:gap-6;
}

.category-nav .nav-link {
  @apply text-white text-center py-1 px-2 rounded-md hover:bg-green-700 whitespace-nowrap h-[34px] flex items-center;
}

.category-nav .nav-link-active {
  @apply text-yellow-500 bg-green-700 font-semibold;
}

select.nav-link {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}
</style>
