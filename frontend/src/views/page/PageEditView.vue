<script lang="ts">
import { defineComponent } from "vue";
import PageEditorComponent from "@/components/page/PageEditorComponent.vue";

export default defineComponent({
  name: "PageEditView",
  props: {
    slug: {
      type: String,
      required: true,
      default: "_",
    },
    year: {
      type: String,
      required: true,
    },
  },
  components: {
    PageEditorComponent,
  },
  data() {
    return {
      htmlContent: ``,
    };
  },
  computed: {
    readableSlug() {
      if (this.slug === "_") {
        return `Ročník ${this.year}`;
      }
      return this.slug.replace(/[-_]/g, " ");
    },
  },
  methods: {
    savePage() {
      // TODO: send to backend
      alert(this.htmlContent);
      console.log(this.htmlContent);
    },
  },
});
</script>

<template>
  <nav class="top-nav">
    <h1 class="nav-inner">
      <span class="title">Upravuje sa:</span>
      <span class="nav-label uppercase">{{ year }} / {{ readableSlug }}</span>
    </h1>
    <div class="nav-inner">
      <button class="button button-red">Odstrániť</button>
      <button class="button button-green" @click="savePage">Uložiť</button>
    </div>
  </nav>

  <div class="editor-container">
    <PageEditorComponent v-model="htmlContent" />
  </div>
</template>

<style scoped>
@import "tailwindcss";

.top-nav {
  @apply flex flex-row justify-between gap-4 my-6 mx-12;
}

.nav-inner {
  @apply flex flex-row gap-2 items-center;
}

.nav-inner .nav-label {
  @apply text-2xl text-gray-500;
}

.editor-container {
  @apply my-6;
}
</style>
