<script lang="ts">
import { RouterLink } from "vue-router";

export default {
  name: "PageSidebarComponent",
  components: {
    RouterLink,
  },
  props: {
    slug: {
      type: String,
      required: true,
    },
    year: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      links: [
        // TODO: fetch links from backend
        { id: 1, title: "Osoby" },
        { id: 2, title: "Koláče" },
        { id: 3, title: "Kontakt" },
      ],
    };
  },
};
</script>

<template>
  <aside class="sidebar">
    <ul>
      <li>
        <RouterLink
          :to="{ name: 'year', params: { year } }"
          class="sidebar-link sidebar-year-link"
          active-class="sidebar-link-active"
        >
          Ročník {{ year }}
        </RouterLink>
      </li>
      <li v-for="link in links" :key="link.id">
        <RouterLink
          :to="{ name: 'page', params: { year: year, slug: link.title } }"
          class="sidebar-link"
          active-class="sidebar-link-active"
        >
          {{ link.title }}
        </RouterLink>
      </li>
    </ul>

    <!-- TODO: iba ak je editor pre daný ročník alebo admin -->
    <RouterLink class="text-center my-4" :to="{ name: 'admin-pages' }">
      Upraviť
    </RouterLink>
  </aside>
</template>

<style scoped>
@import "tailwindcss";

.sidebar {
  @apply bg-gray-800 text-white sm:w-[240px] text-center sm:text-left sm:h-[80vh] flex flex-col justify-between;
}

.sidebar a.sidebar-year-link {
  @apply text-yellow-100 font-bold;
}

.sidebar .sidebar-link {
  @apply text-white block py-4 px-6;
}

.sidebar .sidebar-link-active {
  @apply bg-gray-900 text-yellow-500;
}

.sidebar .sidebar-link:hover {
  @apply bg-gray-900;
}
</style>
