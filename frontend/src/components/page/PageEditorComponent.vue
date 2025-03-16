<script lang="ts">
const LICENSE_KEY = "GPL";

import { defineComponent } from "vue";
import { Ckeditor } from "@ckeditor/ckeditor5-vue";
import {
  DecoupledEditor,
  Alignment,
  AutoImage,
  AutoLink,
  Autosave,
  BalloonToolbar,
  Base64UploadAdapter,
  BlockQuote,
  Bold,
  CloudServices,
  Code,
  CodeBlock,
  Essentials,
  FontBackgroundColor,
  FontColor,
  FontFamily,
  FontSize,
  GeneralHtmlSupport,
  Heading,
  Highlight,
  HorizontalLine,
  ImageBlock,
  ImageCaption,
  ImageInline,
  ImageInsert,
  ImageInsertViaUrl,
  ImageResize,
  ImageStyle,
  ImageTextAlternative,
  ImageToolbar,
  ImageUpload,
  Indent,
  IndentBlock,
  Italic,
  Link,
  Paragraph,
  RemoveFormat,
  Strikethrough,
  Subscript,
  Superscript,
  Table,
  TableCaption,
  TableCellProperties,
  TableColumnResize,
  TableProperties,
  TableToolbar,
  Underline,
} from "ckeditor5";

import translations from "ckeditor5/translations/sk.js";
import "ckeditor5/ckeditor5.css";

export default defineComponent({
  name: "PageEditorComponent",
  components: {
    ckeditor: Ckeditor,
  },
  props: {
    modelValue: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      initialData: this.modelValue,
      editor: DecoupledEditor as any,
      isLayoutReady: false,
    };
  },
  computed: {
    config(): any {
      if (!this.isLayoutReady) {
        return null;
      }
      return {
        toolbar: {
          items: [
            "heading",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "|",
            "bold",
            "italic",
            "underline",
            "|",
            "link",
            "insertImage",
            "insertTable",
            "highlight",
            "blockQuote",
            "codeBlock",
            "|",
            "alignment",
            "|",
            "outdent",
            "indent",
          ],
          shouldNotGroupWhenFull: true,
        },
        plugins: [
          Alignment,
          AutoImage,
          AutoLink,
          Autosave,
          BalloonToolbar,
          Base64UploadAdapter,
          BlockQuote,
          Bold,
          CloudServices,
          Code,
          CodeBlock,
          Essentials,
          FontBackgroundColor,
          FontColor,
          FontFamily,
          FontSize,
          GeneralHtmlSupport,
          Heading,
          Highlight,
          HorizontalLine,
          ImageBlock,
          ImageCaption,
          ImageInline,
          ImageInsert,
          ImageInsertViaUrl,
          ImageResize,
          ImageStyle,
          ImageTextAlternative,
          ImageToolbar,
          ImageUpload,
          Indent,
          IndentBlock,
          Italic,
          Link,
          Paragraph,
          RemoveFormat,
          Strikethrough,
          Subscript,
          Superscript,
          Table,
          TableCaption,
          TableCellProperties,
          TableColumnResize,
          TableProperties,
          TableToolbar,
          Underline,
        ],
        balloonToolbar: ["bold", "italic", "|", "link", "insertImage"],
        fontFamily: {
          supportAllValues: true,
        },
        fontSize: {
          options: [10, 12, 14, "default", 18, 20, 22],
          supportAllValues: true,
        },
        heading: {
          options: [
            {
              model: "paragraph",
              title: "Paragraph",
              class: "ck-heading_paragraph",
            },
            {
              model: "heading1",
              view: "h1",
              title: "Heading 1",
              class: "ck-heading_heading1",
            },
            {
              model: "heading2",
              view: "h2",
              title: "Heading 2",
              class: "ck-heading_heading2",
            },
            {
              model: "heading3",
              view: "h3",
              title: "Heading 3",
              class: "ck-heading_heading3",
            },
            {
              model: "heading4",
              view: "h4",
              title: "Heading 4",
              class: "ck-heading_heading4",
            },
            {
              model: "heading5",
              view: "h5",
              title: "Heading 5",
              class: "ck-heading_heading5",
            },
            {
              model: "heading6",
              view: "h6",
              title: "Heading 6",
              class: "ck-heading_heading6",
            },
          ],
        },
        htmlSupport: {
          allow: [
            {
              name: /^.*$/,
              styles: true,
              attributes: true,
              classes: true,
            },
          ],
        },
        image: {
          toolbar: [
            "toggleImageCaption",
            "imageTextAlternative",
            "|",
            "imageStyle:inline",
            "imageStyle:wrapText",
            "imageStyle:breakText",
            "|",
            "resizeImage",
          ],
        },
        language: "sk",
        licenseKey: LICENSE_KEY,
        link: {
          addTargetToExternalLinks: true,
          defaultProtocol: "https://",
          decorators: {
            toggleDownloadable: {
              mode: "manual",
              label: "Downloadable",
              attributes: {
                download: "file",
              },
            },
          },
        },
        menuBar: {
          isVisible: true,
        },
        placeholder: "Začni písať tu...",
        table: {
          contentToolbar: [
            "tableColumn",
            "tableRow",
            "mergeTableCells",
            "tableProperties",
            "tableCellProperties",
          ],
        },
        translations: [translations],
      };
    },
  },
  mounted() {
    this.isLayoutReady = true;
  },
  methods: {
    onReady(editorInstance: any) {
      const toolbarContainer = this.$refs.editorToolbar as HTMLElement;
      const menuBarContainer = this.$refs.editorMenuBar as HTMLElement;

      // Clean up any existing child nodes
      [toolbarContainer, menuBarContainer].forEach((container) => {
        while (container.firstChild) {
          container.removeChild(container.firstChild);
        }
      });

      toolbarContainer.appendChild(editorInstance.ui.view.toolbar.element);
      menuBarContainer.appendChild(editorInstance.ui.view.menuBarView.element);

      // Listen for editor changes and emit update event
      editorInstance.model.document.on("change:data", () => {
        this.$emit("update:modelValue", editorInstance.getData());
      });
    },
  },
});
</script>

<template>
  <div class="main-container">
    <div
      class="editor-container editor-container_document-editor"
      ref="editorContainer"
    >
      <div class="editor-container__menu-bar" ref="editorMenuBar"></div>
      <div class="editor-container__toolbar" ref="editorToolbar"></div>
      <div class="editor-container__editor-wrapper">
        <div class="editor-container__editor">
          <div ref="editorElement">
            <ckeditor
              v-if="editor && config"
              :editor="editor"
              :config="config"
              v-model="initialData"
              @ready="onReady"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,400;0,700;1,400;1,700&display=swap");
@import "tailwindcss";

@media print {
  body {
    margin: 0 !important;
  }
}

.editor-container {
  @apply m-6;
}

.editor-container .ck-toolbar {
  @apply border-b-0;
  border-radius: 0 !important;
}

.editor-container .editor-container__editor .ck-content {
  @apply min-h-[400px] border-1 border-gray-300 border-t-0;
  border-radius: 0 !important;
}
</style>
