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
  WordCount,
} from "ckeditor5";

import translations from "ckeditor5/translations/sk.js";
import "ckeditor5/ckeditor5.css";

export default defineComponent({
  name: "PageEditorComponent",
  components: {
    ckeditor: Ckeditor,
  },
  props: {
    // Allow the parent to set the initial HTML content.
    initialHtml: {
      type: String,
      default: "henlo",
    },
    // (Optional) You can add more props here to customize other config parts.
  },
  data() {
    return {
      initialData: this.initialHtml,
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
          WordCount,
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
        placeholder: "Type or paste your content here!",
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
      const wordCountContainer = this.$refs.editorWordCount as HTMLElement;
      const toolbarContainer = this.$refs.editorToolbar as HTMLElement;
      const menuBarContainer = this.$refs.editorMenuBar as HTMLElement;

      // Clean up any existing child nodes
      [wordCountContainer, toolbarContainer, menuBarContainer].forEach(
        (container) => {
          while (container.firstChild) {
            container.removeChild(container.firstChild);
          }
        }
      );

      const wordCount = editorInstance.plugins.get("WordCount");
      wordCountContainer.appendChild(wordCount.wordCountContainer);
      toolbarContainer.appendChild(editorInstance.ui.view.toolbar.element);
      menuBarContainer.appendChild(editorInstance.ui.view.menuBarView.element);
    },
  },
});
</script>

<template>
  <div class="main-container">
    <div
      class="editor-container editor-container_document-editor editor-container_include-word-count"
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
      <div class="editor_container__word-count" ref="editorWordCount"></div>
    </div>
  </div>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,400;0,700;1,400;1,700&display=swap");

@media print {
  body {
    margin: 0 !important;
  }
}

.main-container {
  --ckeditor5-preview-height: 700px;
  font-family: "Lato";
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
}

.ck-content {
  font-family: "Lato";
  line-height: 1.6;
  word-break: break-word;
}

.editor-container__editor-wrapper {
  display: flex;
  width: fit-content;
}

.editor-container_document-editor {
  border: 1px solid var(--ck-color-base-border);
}

.editor-container_document-editor .editor-container__toolbar {
  display: flex;
  position: relative;
  box-shadow: 0 2px 3px hsla(0, 0%, 0%, 0.078);
}

.editor-container_document-editor .editor-container__toolbar > .ck.ck-toolbar {
  flex-grow: 1;
  width: 0;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
  border-top: 0;
  border-left: 0;
  border-right: 0;
}

.editor-container_document-editor
  .editor-container__menu-bar
  > .ck.ck-menu-bar {
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
  border-top: 0;
  border-left: 0;
  border-right: 0;
}

.editor-container_document-editor .editor-container__editor-wrapper {
  max-height: var(--ckeditor5-preview-height);
  min-height: var(--ckeditor5-preview-height);
  overflow-y: scroll;
  background: var(--ck-color-base-foreground);
}

.editor-container_document-editor .editor-container__editor {
  margin-top: 28px;
  margin-bottom: 28px;
  height: 100%;
}

.editor-container_document-editor
  .editor-container__editor
  .ck.ck-editor__editable {
  box-sizing: border-box;
  min-width: calc(210mm + 2px);
  max-width: calc(210mm + 2px);
  min-height: 297mm;
  height: fit-content;
  padding: 20mm 12mm;
  border: 1px hsl(0, 0%, 82.7%) solid;
  background: hsl(0, 0%, 100%);
  box-shadow: 0 2px 3px hsla(0, 0%, 0%, 0.078);
  flex: 1 1 auto;
  margin-left: 72px;
  margin-right: 72px;
}

.editor_container__word-count .ck-word-count {
  color: var(--ck-color-text);
  display: flex;
  height: 20px;
  gap: var(--ck-spacing-small);
  justify-content: flex-end;
  font-size: var(--ck-font-size-base);
  line-height: var(--ck-line-height-base);
  font-family: var(--ck-font-face);
  padding: var(--ck-spacing-small) var(--ck-spacing-standard);
}

.editor-container_include-word-count.editor-container_document-editor
  .editor_container__word-count {
  border-top: 1px solid var(--ck-color-base-border);
}
</style>
