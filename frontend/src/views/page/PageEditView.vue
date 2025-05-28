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
      files: [] as any[],
      apiUrl: api.defaults.baseURL,
    };
  },
  async created() {
    let [id, slug] = this.idSlug.split("-");

    const parsedId = parseInt(id);
    if (isNaN(parsedId)) {
      this.$router.push(`/page/${this.idSlug}`);
      return;
    }

    this.id = parsedId;
    const page = await this.pagesStore.fetchPageById(this.id);
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
    getFileTypeInfo(file: any) {
      const name = file.name || "";
      const ext = name.split(".").pop()?.toLowerCase() || "";
      const imageExts = ["jpg", "jpeg", "png", "gif", "webp", "svg"];
      if (imageExts.includes(ext)) {
        return { type: "image" };
      }
      if (["pdf"].includes(ext)) return { type: "emoji", emoji: "📄" };
      if (["doc", "docx", "odt", "rtf", "txt"].includes(ext))
        return { type: "emoji", emoji: "📝" };
      if (["zip", "rar", "7z", "tar", "gz"].includes(ext))
        return { type: "emoji", emoji: "📦" };
      if (["xls", "xlsx", "ods", "csv"].includes(ext))
        return { type: "emoji", emoji: "📊" };
      if (["ppt", "pptx", "odp"].includes(ext))
        return { type: "emoji", emoji: "📈" };
      return { type: "emoji", emoji: "📁" };
    },
    async loadExistingFiles() {
      try {
        const response = await api.get(`/page/${this.id}/upload`);
        // @ts-ignore
        this.files = response.data.map((file: any) => ({
          ...file,
          alreadyUploaded: true,
          isUploading: false,
          uploadError: null,
          fileObj: null,
          abortController: null,
        }));
      } catch (error) {
        console.error("Failed to load existing files:", error);
      }
    },
    async savePage() {
      await this.saveContent();
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
    addFile(event: Event) {
      const fileList = (event.target as HTMLInputElement).files;
      if (fileList) {
        const startIndex = this.files.length;
        const newFilesPrepared = Array.from(fileList).map((file) => {
          return {
            name: file.name,
            size: file.size,
            fileObj: file,
            alreadyUploaded: false,
            isUploading: true,
            uploadError: null,
            abortController: null,
          };
        });

        this.files = [...this.files, ...newFilesPrepared];

        for (let i = 0; i < newFilesPrepared.length; i++) {
          const reactiveFileEntry = this.files[startIndex + i];
          if (reactiveFileEntry) {
            this.uploadSingleFile(reactiveFileEntry);
          }
        }

        if (this.$refs.fileInput) {
          (this.$refs.fileInput as HTMLInputElement).value = "";
        }
      }
    },
    async uploadSingleFile(fileEntry: any) {
      fileEntry.abortController = new AbortController();

      if (fileEntry.size > 1024 * 1024 * 10) {
        const errorMsg = `File too large (max 10MB). ${fileEntry.name} is ${
          Math.round((fileEntry.size / (1024 * 1024)) * 100) / 100
        } MB.`;
        fileEntry.isUploading = false;
        fileEntry.uploadError = errorMsg;
        fileEntry.abortController = null;
        alert(errorMsg);
        return;
      }

      const formData = new FormData();
      formData.append("uploaded_file", fileEntry.fileObj);

      try {
        await api.post(`/page/${this.id}/upload`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          signal: fileEntry.abortController.signal,
        });
        fileEntry.isUploading = false;
        fileEntry.alreadyUploaded = true;
        fileEntry.uploadError = null;
        fileEntry.abortController = null;
      } catch (error: any) {
        const isCancellation =
          error.name === "AbortError" || (api.isCancel && api.isCancel(error));

        if (isCancellation) {
          console.log(`Upload of ${fileEntry.name} was cancelled by user.`);
        } else {
          const errorMsg = `Failed to upload ${fileEntry.name}. ${
            error.response?.data?.message || error.message || "Unknown error"
          }`;
          fileEntry.isUploading = false;
          fileEntry.uploadError = errorMsg;
          fileEntry.abortController = null;
          console.error(`Upload error for ${fileEntry.name}:`, errorMsg, error);
          alert(errorMsg);
        }
      }
    },
    async removeFile(file: any) {
      if (!confirm(`Do you really want to delete the file ${file.name}?`)) {
        return;
      }

      if (file.alreadyUploaded && !file.uploadError) {
        try {
          await api.delete(
            `/page/${this.id}/upload/${encodeURIComponent(file.name)}`
          );
          this.files = this.files.filter((f) => f !== file);
        } catch (error) {
          console.error(
            `Failed to delete file ${file.name} from server:`,
            error
          );
          alert(
            `Failed to delete file ${file.name} from server. It will be removed from this list.`
          );
          this.files = this.files.filter((f) => f !== file);
        }
      } else {
        this.files = this.files.filter((f) => f !== file);
      }
    },
    cancelUpload(fileToCancel: any) {
      if (fileToCancel.abortController) {
        fileToCancel.abortController.abort();
      }
      this.files = this.files.filter((f) => f !== fileToCancel);
    },
    getObjectUrl(fileObj: File) {
      return URL.createObjectURL(fileObj);
    },
    handleFileDragStart(file: any, event: DragEvent) {
      if (!file.alreadyUploaded || file.isUploading || file.uploadError) {
        event.preventDefault();
        return;
      }

      const encodedFileName = encodeURIComponent(file.name);
      const fileUrl = `${this.apiUrl}/page/${this.id}/upload/${encodedFileName}`;
      let dragHtml;
      let plainText;

      const fileTypeInfo = this.getFileTypeInfo(file);

      if (fileTypeInfo.type === "image") {
        dragHtml = `<img src="${fileUrl}" alt="${file.name}">`;
        plainText = `Image: ${file.name} (${fileUrl})`;
      } else {
        dragHtml = `<a href="${fileUrl}" target="_blank">${file.name}</a>`;
        plainText = `Link: ${file.name} (${fileUrl})`;
      }

      if (event.dataTransfer) {
        event.dataTransfer.setData("text/html", dragHtml);
        event.dataTransfer.setData("text/plain", plainText);
        event.dataTransfer.effectAllowed = "copy";
      }
    },
    insertLinkIntoEditor(file: any) {
      if (!file.alreadyUploaded) {
        alert("File must be uploaded before it can be linked.");
        return;
      }
      const fileUrl = `${this.apiUrl}/page/${
        this.id
      }/upload/${encodeURIComponent(file.name)}`;
      const linkHtml = `<a href="${fileUrl}" target="_blank">${file.name}</a>`;

      if (this.htmlContent === null || this.htmlContent === undefined) {
        this.htmlContent = "";
      }
      if (
        this.htmlContent.length > 0 &&
        !this.htmlContent.endsWith(" ") &&
        !this.htmlContent.endsWith(">")
      ) {
        this.htmlContent += " ";
      }
      this.htmlContent += linkHtml + " ";
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
        <p class="text-sm text-gray-600 mb-3 px-1">
          Click "Attach File" to select files. They will upload immediately.
          Drag uploaded files (images as images, others as links) from this list
          to the editor.
        </p>
        <input
          type="file"
          multiple
          @change="addFile"
          class="file-upload-input"
          ref="fileInput"
        />
        <button
          class="button button-green w-32 mb-2"
          @click="() => ($refs.fileInput as HTMLInputElement).click()"
        >
          Attach File
        </button>

        <div
          class="file-upload-item"
          :class="{
            'opacity-60': file.isUploading,
            'opacity-70 border-red-500 border':
              file.uploadError && !file.isUploading,
          }"
          v-for="(file, index) in files"
          :key="file.name + '-' + index"
          :draggable="
            file.alreadyUploaded && !file.isUploading && !file.uploadError
          "
          @dragstart="handleFileDragStart(file, $event)"
          :title="
            file.uploadError
              ? typeof file.uploadError === 'string'
                ? file.uploadError
                : 'Upload failed'
              : file.isUploading
              ? 'Uploading...'
              : file.name
          "
        >
          <div class="relative w-7 h-7 mr-2 flex-shrink-0">
            <div v-if="file.isUploading" class="spinner-overlay">
              <div class="spinner"></div>
            </div>
            <div
              v-if="file.uploadError && !file.isUploading"
              class="error-indicator"
              :title="
                typeof file.uploadError === 'string'
                  ? file.uploadError
                  : 'Upload failed'
              "
            >
              <span class="text-red-500 text-xl">⚠️</span>
            </div>

            <span
              v-if="getFileTypeInfo(file).type === 'image'"
              class="file-thumb"
            >
              <img
                v-if="file.alreadyUploaded && !file.isUploading"
                :src="`${apiUrl}/page/${id}/upload/${encodeURIComponent(
                  file.name
                )}`"
                alt="thumb"
                class="thumb-img"
              />
              <img
                v-else-if="file.fileObj"
                :src="getObjectUrl(file.fileObj)"
                alt="preview"
                class="thumb-img"
              />
              <div v-else class="thumb-placeholder">IMG</div>
            </span>
            <span v-else class="file-emoji">
              {{ getFileTypeInfo(file).emoji }}
            </span>
          </div>

          <span
            class="file-upload-item-name flex-grow"
            :class="{ 'text-red-500': file.uploadError && !file.isUploading }"
          >
            {{ file.name }} ({{ (file.size / 1024).toFixed(1) }} KB)
            <span
              v-if="
                file.uploadError &&
                !file.isUploading &&
                typeof file.uploadError === 'string'
              "
              class="text-xs block"
            >
              - Error: {{ file.uploadError }}</span
            >
            <span v-if="file.isUploading" class="text-xs block text-gray-500"
              >Uploading...</span
            >
          </span>
          <div class="flex items-center ml-2 flex-shrink-0">
            <button
              v-if="
                file.alreadyUploaded && !file.isUploading && !file.uploadError
              "
              class="button button-blue mr-2"
              @click="insertLinkIntoEditor(file)"
              title="Insert link into editor (appends to content)"
            >
              Link
            </button>

            <button
              v-if="file.isUploading"
              class="button button-orange"
              @click="cancelUpload(file)"
              title="Cancel upload"
            >
              Cancel
            </button>
            <button
              v-else
              class="button button-red"
              @click="removeFile(file)"
              title="Delete file"
            >
              Delete
            </button>
          </div>
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
  @apply cursor-grab mx-4 flex flex-row items-center justify-between p-1 border-b border-gray-200;
}

.file-thumb {
  display: inline-block;
  width: 100%;
  height: 100%;
  vertical-align: middle;
  position: relative;
}

.thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
  background: #f3f3f3;
}

.thumb-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e0e0e0;
  color: #757575;
  font-size: 0.7rem;
  border-radius: 4px;
}

.file-emoji {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  text-align: center;
  font-size: 1.2rem;
  vertical-align: middle;
  position: relative;
}

.spinner-overlay,
.error-indicator {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.6);
  border-radius: 4px;
  z-index: 10;
}

.spinner {
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-left-color: #3498db;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.button-blue {
  @apply bg-blue-500 hover:bg-blue-700 text-white;
}

.button-orange {
  @apply bg-orange-500 hover:bg-orange-700 text-white;
}
</style>
