<script lang="ts">
import { defineComponent } from "vue";
import PageEditorComponent from "@/components/page/PageEditorComponent.vue";

export default defineComponent({
  name: "PageEditView",
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  components: {
    PageEditorComponent,
  },
  data() {
    return {
      htmlContent: "",
    };
  },
  methods: {
    savePage() {
      alert(this.htmlContent);
    },
  },
});
</script>

<template>
  <nav class="flex flex-row justify-end gap-4 m-6">
    <button class="button button-red">Odstrániť</button>
    <button class="button button-green" @click="savePage">Uložiť</button>
  </nav>

  <div class="editor-container">
    <PageEditorComponent v-model="htmlContent" />
  </div>
</template>

<style scoped>
@import "tailwindcss";

.editor-container {
  @apply my-6;
}
</style>
