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
  async created() {
    await this.loadExistingFiles();
  },
  methods: {
    async loadExistingFiles() {
      try {
        const response = await api.get(`/page/${this.slug}/upload`);
        this.files = response.data.map((file: any) => ({
          ...file,
          alreadyUploaded: true,
        }));
      } catch (error) {
        console.error("Failed to load existing files:", error);
      }
    },
    async savePage() {
      await this.saveContent();
      await this.uploadFiles();
    },
    async saveContent() {
      // TODO: send to backend
      console.log(this.htmlContent);
    },
    async uploadFiles() {
      const newFiles = this.files.filter(
        (file: { alreadyUploaded: boolean }) => !file.alreadyUploaded
      );

      for (const file of newFiles) {
        if (file.size > 1024 * 1024 * 10) {
          alert(
            `Maximálna povolená veľkosť súboru je 10 MB (${file.name} má ${file.size} B)`
          );
          return;
        }

        const formData = new FormData();
        formData.append("uploaded_file", file.fileObj);

        try {
          await api.post(`/page/${this.slug}/upload`, formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });
        } catch (error) {
          console.error(`Failed to upload file ${file.name}:`, error);
          alert(`Nepodarilo sa nahrať súbor ${file.name}`);
        }
      }

      await this.loadExistingFiles();
    },
    addFile(event: Event) {
      const fileList = (event.target as HTMLInputElement).files;
      if (fileList) {
        const newFiles = Array.from(fileList).map((file) => {
          return {
            name: file.name,
            size: file.size,
            fileObj: file,
            alreadyUploaded: false,
          };
        });
        this.files = [...this.files, ...newFiles];
      }
    },
    async removeFile(file: any) {
      if (!confirm(`Naozaj chcete odstrániť súbor ${file.name}?`)) {
        return;
      }

      if (file.alreadyUploaded) {
        try {
          await api.delete(`/page/${this.slug}/upload/${file.name}`);
          this.files = this.files.filter((f) => f.name !== file.name);
        } catch (error) {
          console.error(`Failed to delete file ${file.name}:`, error);
          alert(`Nepodarilo sa odstrániť súbor ${file.name}`);
        }
      } else {
        this.files = this.files.filter((f) => f !== file);
      }
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
          @click="() => ($refs.fileInput as HTMLInputElement).click()"
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
