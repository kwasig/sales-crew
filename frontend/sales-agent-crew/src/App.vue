<!-- App.vue -->
<template>
  <div class="h-screen bg-white dark:bg-gray-900 transition-colors duration-200">
    <!-- Main content -->
    <main>
      <SignedIn>
        <router-view />
      </SignedIn>
      <SignedOut>
        <LoginPage />
      </SignedOut>
    </main>
  </div>
</template>

<script setup>
import { SignedIn, SignedOut } from '@clerk/vue'
import LoginPage from './views/LoginPage.vue'
import { onMounted } from 'vue'

onMounted(() => {
  // Initialize dark mode based on saved preference or system preference
  const savedMode = localStorage.getItem('darkMode')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  
  if (savedMode === 'true' || (!savedMode && prefersDark)) {
    document.documentElement.classList.add('dark')
  }
})
</script>
