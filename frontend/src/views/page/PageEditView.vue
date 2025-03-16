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
      initialHtmlContent: "<p>Začni písať tu...</p>",
    };
  },
});
</script>

<template>
  <div class="editor-container">
    <PageEditorComponent :initialHtml="initialHtmlContent" />
  </div>
</template>

<style scoped>
@import "tailwindcss";

.editor-container {
  @apply my-6;
}
</style>
