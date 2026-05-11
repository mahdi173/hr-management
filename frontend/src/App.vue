<template>
  <div id="app">
    <header>
      <h1>📝 MVP Todo Application</h1>
      <p class="subtitle">FastAPI + Vue.js + Docker</p>
    </header>

    <main class="container">
      <!-- Status Section -->
      <div class="status-section">
        <div v-if="loading" class="loading">Loading...</div>
        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="apiStatus" class="success">✓ Connected to API</div>
      </div>

      <!-- Add Item Form -->
      <div class="add-item">
        <h2>Add New Item</h2>
        <form @submit.prevent="addItem">
          <input
            v-model="newItem.title"
            type="text"
            placeholder="Item title"
            required
            class="input"
          />
          <textarea
            v-model="newItem.description"
            placeholder="Description (optional)"
            class="textarea"
          ></textarea>
          <button type="submit" class="btn btn-primary">Add Item</button>
        </form>
      </div>

      <!-- Items List -->
      <div class="items-section">
        <h2>Items ({{ items.length }})</h2>
        <div v-if="items.length === 0" class="empty-state">
          No items yet. Create your first item above!
        </div>
        <div v-else class="items-list">
          <div
            v-for="item in items"
            :key="item.id"
            class="item-card"
            :class="{ completed: item.completed }"
          >
            <div class="item-content">
              <h3>{{ item.title }}</h3>
              <p v-if="item.description">{{ item.description }}</p>
              <small>Created: {{ formatDate(item.created_at) }}</small>
            </div>
            <div class="item-actions">
              <button
                @click="toggleComplete(item)"
                class="btn btn-small"
                :class="item.completed ? 'btn-warning' : 'btn-success'"
              >
                {{ item.completed ? 'Undo' : 'Complete' }}
              </button>
              <button
                @click="deleteItem(item.id)"
                class="btn btn-small btn-danger"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      items: [],
      newItem: {
        title: '',
        description: '',
        completed: false
      },
      loading: false,
      error: null,
      apiStatus: false
    }
  },
  mounted() {
    this.checkAPI()
    this.fetchItems()
  },
  methods: {
    async checkAPI() {
      try {
        const response = await axios.get('/api/health')
        this.apiStatus = response.data.status === 'healthy'
      } catch (err) {
        console.error('API health check failed:', err)
        this.error = 'Cannot connect to API'
      }
    },
    async fetchItems() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get('/api/items/')
        this.items = response.data
      } catch (err) {
        this.error = 'Failed to fetch items'
        console.error('Error fetching items:', err)
      } finally {
        this.loading = false
      }
    },
    async addItem() {
      if (!this.newItem.title.trim()) return

      this.loading = true
      this.error = null
      try {
        await axios.post('/api/items/', this.newItem)
        this.newItem = { title: '', description: '', completed: false }
        await this.fetchItems()
      } catch (err) {
        this.error = 'Failed to add item'
        console.error('Error adding item:', err)
      } finally {
        this.loading = false
      }
    },
    async toggleComplete(item) {
      try {
        await axios.put(`/api/items/${item.id}`, {
          ...item,
          completed: !item.completed
        })
        await this.fetchItems()
      } catch (err) {
        this.error = 'Failed to update item'
        console.error('Error updating item:', err)
      }
    },
    async deleteItem(id) {
      if (!confirm('Are you sure you want to delete this item?')) return

      try {
        await axios.delete(`/api/items/${id}`)
        await this.fetchItems()
      } catch (err) {
        this.error = 'Failed to delete item'
        console.error('Error deleting item:', err)
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString()
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 20px;
}

#app {
  max-width: 1200px;
  margin: 0 auto;
}

header {
  text-align: center;
  color: white;
  margin-bottom: 40px;
  padding: 20px;
}

header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
}

.container {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.status-section {
  margin-bottom: 20px;
}

.loading,
.error,
.success {
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 10px;
}

.loading {
  background: #e3f2fd;
  color: #1976d2;
}

.error {
  background: #ffebee;
  color: #c62828;
}

.success {
  background: #e8f5e9;
  color: #2e7d32;
}

.add-item {
  margin-bottom: 40px;
  padding-bottom: 30px;
  border-bottom: 2px solid #f0f0f0;
}

.add-item h2,
.items-section h2 {
  margin-bottom: 20px;
  color: #333;
}

.input,
.textarea {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.3s;
}

.input:focus,
.textarea:focus {
  outline: none;
  border-color: #667eea;
}

.textarea {
  min-height: 80px;
  resize: vertical;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-small {
  padding: 8px 16px;
  font-size: 0.9rem;
}

.btn-success {
  background: #4caf50;
  color: white;
}

.btn-success:hover {
  background: #45a049;
}

.btn-warning {
  background: #ff9800;
  color: white;
}

.btn-warning:hover {
  background: #fb8c00;
}

.btn-danger {
  background: #f44336;
  color: white;
}

.btn-danger:hover {
  background: #e53935;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 1.1rem;
}

.items-list {
  display: grid;
  gap: 15px;
}

.item-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  transition: all 0.3s;
}

.item-card:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.item-card.completed {
  opacity: 0.6;
  border-left-color: #4caf50;
}

.item-card.completed h3 {
  text-decoration: line-through;
}

.item-content {
  flex: 1;
}

.item-content h3 {
  margin-bottom: 8px;
  color: #333;
}

.item-content p {
  color: #666;
  margin-bottom: 8px;
}

.item-content small {
  color: #999;
  font-size: 0.85rem;
}

.item-actions {
  display: flex;
  gap: 10px;
}

@media (max-width: 768px) {
  .item-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .item-actions {
    margin-top: 15px;
    width: 100%;
  }

  .item-actions button {
    flex: 1;
  }
}
</style>
