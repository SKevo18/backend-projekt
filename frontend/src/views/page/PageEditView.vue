<script lang="ts">
import api from "@/services/api";
import PageEditorComponent from "@/components/page/PageEditorComponent.vue";
// TODO: redirect to login if not editor or admin (via guard)

export default {
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
      files: [],
    };
  },
  computed: {
    readableSlug() {
      if (this.slug === "_") {
        return `Hlavná stránka`;
      }
      return this.slug.replace(/[-_]/g, " ");
    },
  },
  methods: {
    savePage() {
      this.saveContent();
      this.uploadFiles();
    },
    saveContent() {
      // TODO: send to backend
      alert(this.htmlContent);
      console.log(this.htmlContent);
    },
    uploadFiles() {
      for (const file of this.files) {
        if (file.size > 1024 * 1024 * 10) {
          alert(
            `Maximálna povolená veľkosť súboru je 10 MB (${file.name} má ${file.size} B)`
          );
          return;
        }

        const formData = new FormData();
        formData.append("uploaded_file", file);

        api.post(`/page/${this.slug}/upload`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
      }
    },
    addFile(event: Event) {
      const files = (event.target as HTMLInputElement).files;
      if (files) {
        this.files = Array.from(files);
      }
    },
    removeFile(file: File) {
      this.files = this.files.filter((f) => f !== file);
    },
  },
};
</script>

<template>
  <nav class="top-nav">
    <h1 class="nav-inner">
      <span class="title whitespace-nowrap">Upravuje sa:</span>
      <span class="nav-label uppercase">{{ year }} / {{ readableSlug }}</span>
    </h1>
    <div class="nav-inner">
      <button class="button button-red">Odstrániť</button>
      <button class="button button-green" @click="savePage">Uložiť</button>
    </div>
  </nav>

  <div class="editor-container">
    <PageEditorComponent v-model="htmlContent" />

    <div class="file-upload-container">
      <h2 class="big mb-2">Priložené súbory</h2>

      <div class="file-upload-list">
        <input
          type="file"
          multiple
          @change="addFile"
          class="file-upload-input"
          ref="fileInput"
        />
        <button
          class="button button-green w-32"
          @click="$refs.fileInput.click()"
        >
          Priložiť súbor
        </button>

        <div class="file-upload-item" v-for="file in files" :key="file.name">
          <span class="file-upload-item-name"
            >{{ file.name }}, {{ file.size }} B</span
          >
          <button class="button button-red" @click="removeFile(file)">
            Odstrániť
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import "tailwindcss";

.top-nav {
  @apply flex flex-col md:flex-row justify-between gap-4 my-6 mx-12;
}

.nav-inner {
  @apply flex flex-row gap-2 items-start;
}

.nav-inner .nav-label {
  @apply text-2xl text-gray-500;
}

.editor-container {
  @apply my-6;
}

.file-upload-input {
  @apply hidden;
}

.file-upload-container {
  @apply my-6 border-1 border-gray-300 rounded-md p-2;
}

.file-upload-list {
  @apply flex flex-col gap-2;
}

.file-upload-list .file-upload-item {
  @apply mx-4 flex flex-row items-center justify-between;
}
</style>
