<script lang="ts">
import { defineComponent, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/services/api';

export default defineComponent({
  name: 'PageSidebarComponent',
  setup() {
    const links = ref<{ id: number; title: string; category: any }[]>([]);
    const route = useRoute();

    const fetchLinks = async () => {
      try {
        const response = await api.get('/page/');
        links.value = response.data.filter((page: any) => {
          return page.category?.slug === route.params.slug;
        });
      } catch (error) {
        console.error('Nepodarilo sa načítať stránky pre sidebar.', error);
      }
    };

    onMounted(fetchLinks);
    watch(
      () => route.params.slug,
      () => {
        fetchLinks();
      }
    );

    return {
      links,
      year: route.params.year,
      slug: route.params.slug
    };
  }
});

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
          :to="{ name: 'page', params: { year, slug: link.title } }"
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
