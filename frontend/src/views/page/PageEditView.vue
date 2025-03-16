<script lang="ts">
export default {
  name: "PageEditView",
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      pageHtml: "<p>aaaaaaa</p>",
    };
  },
};
</script>

<template>
  <div class="editor-container">
    <umo-editor />
  </div>
</template>

<style>
@import "tailwindcss";

.editor-container {
  @apply max-w-full max-h-full;
}

.editor-container .umo-page-container {
  @apply mx-auto;
}

.editor-container .umo-footer {
  @apply hidden;
}
</style>
