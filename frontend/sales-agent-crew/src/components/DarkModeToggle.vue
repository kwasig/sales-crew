<template>
  <button
    @click="toggleDarkMode"
    class="p-2 rounded-lg transition-colors duration-200 hover:bg-gray-100 dark:hover:bg-gray-700"
    :title="isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'"
  >
    <!-- Sun Icon (visible in dark mode) -->
    <svg
      v-if="isDarkMode"
      class="w-5 h-5 text-yellow-400"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
      />
    </svg>
    
    <!-- Moon Icon (visible in light mode) -->
    <svg
      v-else
      class="w-5 h-5 text-gray-600"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
      />
    </svg>
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isDarkMode = ref(false)

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('darkMode', 'enabled')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('darkMode', 'disabled')
  }
}

const initializeDarkMode = () => {
  const savedPreference = localStorage.getItem('darkMode')
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  
  if (savedPreference === 'enabled') {
    isDarkMode.value = true
    document.documentElement.classList.add('dark')
  } else if (savedPreference === 'disabled') {
    isDarkMode.value = false
    document.documentElement.classList.remove('dark')
  } else if (systemPrefersDark) {
    isDarkMode.value = true
    document.documentElement.classList.add('dark')
    localStorage.setItem('darkMode', 'enabled')
  }
}

onMounted(() => {
  initializeDarkMode()
})
</script>