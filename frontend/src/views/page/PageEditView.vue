<script lang="ts">
import api from "@/services/api";
import PageEditorComponent from "@/components/page/PageEditorComponent.vue";
import { usePagesStore } from "@/store/pageStore";
import { useAuthStore } from "@/store/authStore";

export default {
  name: "PageEditView",
  props: {
    idSlug: {
      type: String,
      required: true,
    },
  },
  components: {
    PageEditorComponent,
  },
  data() {
    return {
      pagesStore: usePagesStore(),
      authStore: useAuthStore(),
      id: null as number | null,
      title: "",
      slug: "",
      htmlContent: ``,
      files: [],
    };
  },
  async created() {
    let [id, slug] = this.idSlug.split("-");

    id = parseInt(id);
    if (isNaN(id)) {
      this.$router.push(`/page/${this.idSlug}`);
      return;
    }

    this.id = id;
    const page = await this.pagesStore.fetchPageById(id);
    this.title = page.title;
    this.slug = slug;
    this.htmlContent = page.html_content;
    await this.loadExistingFiles();
  },
  async beforeRouteEnter(to, from, next) {
    const authStore = useAuthStore();
    if (!authStore.user && authStore.hasToken) {
      await authStore.fetchUserData();
    }

    if (
      !authStore.user ||
      !(authStore.user.role === 1 || authStore.user.role === 2)
    ) {
      next({ name: "login" });
    } else {
      next();
    }
  },
  methods: {
    async loadExistingFiles() {
      try {
        const response = await api.get(`/page/${this.id}/upload`);
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
      this.$router.push(`/page/${this.id}-${this.slug}`);
    },
    async deletePage() {
      const page = await this.pagesStore.fetchPageById(this.id);
      if (!confirm(`Do you really want to delete the page ${page.title}?`)) {
        return;
      }

      await this.pagesStore.deletePage(page);
      this.$router.push(`/`);
    },
    async saveContent() {
      await this.pagesStore.updatePage(this.id, {
        html_content: this.htmlContent,
      });
    },
    async uploadFiles() {
      const newFiles = this.files.filter(
        (file: { alreadyUploaded: boolean }) => !file.alreadyUploaded
      );

      for (const file of newFiles) {
        if (file.size > 1024 * 1024 * 10) {
          alert(
            `The maximum allowed file size is 10 MB  (${file.name} has ${file.size} B)`
          );
          return;
        }

        const formData = new FormData();
        formData.append("uploaded_file", file.fileObj);

        try {
          await api.post(`/page/${this.id}/upload`, formData, {
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
      if (!confirm(`Do you really want to delete the file ${file.name}?`)) {
        return;
      }

      if (file.alreadyUploaded) {
        try {
          await api.delete(`/page/${this.id}/upload/${file.name}`);
          this.files = this.files.filter((f) => f.name !== file.name);
        } catch (error) {
          console.error(`Failed to delete file ${file.name}:`, error);
          alert(`Failed to delete file ${file.name}`);
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
      <span class="title whitespace-nowrap">Editing:</span>
      <span class="nav-label uppercase">{{ title }}</span>
    </h1>
    <div class="nav-inner">
      <button class="button button-red" @click="deletePage">Delete</button>
      <button class="button button-green" @click="savePage">Save</button>
    </div>
  </nav>

  <div class="editor-container">
    <PageEditorComponent v-model="htmlContent" />

    <div class="file-upload-container">
      <h2 class="big mb-2">Attached Files</h2>

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
          Attach File
        </button>

        <div class="file-upload-item" v-for="file in files" :key="file.name">
          <span class="file-upload-item-name"
            >{{ file.name }}, {{ file.size }} B</span
          >
          <button class="button button-red" @click="removeFile(file)">
            Delete
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
