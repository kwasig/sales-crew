<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        <h2>Sales Crew</h2>
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
      </div>
    </nav>
    
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import { useStore } from './stores/store'

export default {
  name: 'App',
  setup() {
    const store = useStore()
    return { store }
  }
}
</script>

<style>
#app {
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
  background-color: #f8fafc;
}

.navbar {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand h2 {
  margin: 0;
  color: #1f2937;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: #6b7280;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #3b82f6;
  background-color: #eff6ff;
}

.main-content {
  min-height: calc(100vh - 80px);
}
</style>