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
  },
  data() {
    return {
      links: [
        // TODO: fetch links from backend
        { id: 1, title: "Home" },
        { id: 2, title: "Chicken Genetics" },
        { id: 3, title: "Poultry Science" },
        { id: 4, title: "Contact" },
      ],
    };
  },
};
</script>

<template>
  <aside class="sidebar">
    <ul>
      <li v-for="link in links" :key="link.id">
        <!-- TODO: link to dynamic route -->
        <RouterLink to="#" class="sidebar-link">
          {{ link.title }}
        </RouterLink>
      </li>
    </ul>
  </aside>
</template>

<style>
@import "tailwindcss";

.sidebar {
  @apply bg-gray-800 text-white sm:w-[240px] text-center sm:text-left h-[80vh];
}

.sidebar-link {
  @apply text-white block py-4 px-6;
}

.sidebar-link:hover {
  @apply bg-gray-900;
}
</style>
