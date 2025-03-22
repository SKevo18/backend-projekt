<script lang="ts">
import { defineComponent } from 'vue';
import { usePagesStore } from '@/store/pageStore';

export default defineComponent({
  name: 'AdminPagesView',
  data() {
    return {
      pagesStore: usePagesStore(),
      year: '',
      description: '',
      showAddPageForm: false,
    };
  },
  computed: {
    sortedPages() {
      return [...this.pagesStore.pages].sort((a, b) => a.year - b.year);
    }
  },
  methods: {
    addPage() {
      const yearValue = Number(this.year);

      if (!this.year || isNaN(yearValue) || yearValue < 2000 || yearValue > 2100) {
        alert('Please enter the correct year in the format 2000-2100.');
        return;
      }

      if (this.description.trim() === '') {
        alert('Please enter a description of the page.');
        return;
      }

      this.pagesStore.addPage(yearValue, this.description);

      this.year = '';
      this.description = '';
      this.showAddPageForm = false;
    },
    deletePage(year: number) {
      if (confirm(`Are you sure you want to delete the page for the year ${year}?`)) {
        this.pagesStore.deletePage(year);
      }
    }
  },
  mounted() {
    this.pagesStore.getPages();
  }
});
</script>

<template>
  <div class="container">
    <div v-if="sortedPages.length === 0" class="empty-message">
      No pages added.
    </div>

    <div v-for="page in sortedPages" :key="page.year" class="page-item">
      <div class="page-content">
        <h3>{{ page.year }}</h3>
        <p>{{ page.description }}</p>
        <button @click="deletePage(page.year)" class="delete-button">
          Delete
        </button>
      </div>
    </div>

    <div class="add-page-button">
      <button @click="showAddPageForm = !showAddPageForm">
        {{ showAddPageForm ? 'Hide Form' : 'Add New Page' }}
      </button>
    </div>

    <div v-if="showAddPageForm" class="form-section">
      <div class="form-group">
        <input
          v-model="year"
          placeholder="Year (e.g. 2025)"
          type="number"
        />
        <input
          v-model="description"
          placeholder="Description"
          type="text"
        />
        <button @click="addPage">Add Page</button>
      </div>
    </div>
  </div>
</template>

<style>
.container {
  padding: 24px;
  background-color: #fafafa;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  gap: 20px;
  font-family: 'Arial', sans-serif;
}

.empty-message {
  text-align: center;
  color: #aaa;
  font-weight: 500;
  font-size: 18px;
}

.page-item {
  background-color: #ffffff;
  border: 1px solid #eaeaea;
  border-radius: 12px;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
}

.page-item:hover {
  transform: translateY(-2px);
}

.page-content {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.page-content h3 {
  font-weight: 600;
  color: #222;
  margin: 0;
}

.page-content p {
  flex-grow: 1;
  color: #555;
  margin: 0;
  font-size: 15px;
}

.delete-button {
  background: none;
  border: none;
  color: #f44336;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: color 0.3s ease, text-decoration 0.2s ease;
}

.delete-button:hover {
  color: #d32f2f; 
  text-decoration: underline; 
}

.form-section {
  background-color: #fff;
  border: 1px solid #eaeaea;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.form-group {
  display: flex;
  gap: 12px;
}

.form-group input {
  flex: 1;
  padding: 12px;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  outline: none;
  transition: border 0.3s ease;
  background-color: #f0f0f0;
}

.form-group input:focus {
  border-color: #4CAF50;
}

.form-group button,
.add-page-button button {
  background-color: #4CAF50;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.add-page-button {
  text-align: center;
}

.add-page-button button {
  width: 100%;
  background: black;
  color: #ffffff;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;
}
</style>