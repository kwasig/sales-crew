import { ref, watch, onMounted } from 'vue'

export function useDarkMode() {
  const isDark = ref(false)

  // Load dark mode preference from localStorage
  const loadDarkModePreference = () => {
    const saved = localStorage.getItem('darkMode')
    if (saved !== null) {
      isDark.value = JSON.parse(saved)
    } else {
      // Check system preference
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    applyDarkMode()
  }

  // Apply dark mode to document
  const applyDarkMode = () => {
    if (isDark.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // Toggle dark mode
  const toggleDarkMode = () => {
    isDark.value = !isDark.value
    localStorage.setItem('darkMode', JSON.stringify(isDark.value))
    applyDarkMode()
  }

  // Set dark mode explicitly
  const setDarkMode = (value) => {
    isDark.value = value
    localStorage.setItem('darkMode', JSON.stringify(isDark.value))
    applyDarkMode()
  }

  // Watch for system preference changes
  const setupSystemPreferenceWatcher = () => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    const handleChange = (e) => {
      // Only follow system preference if no explicit preference is set
      if (localStorage.getItem('darkMode') === null) {
        isDark.value = e.matches
        applyDarkMode()
      }
    }
    
    mediaQuery.addEventListener('change', handleChange)
    
    // Cleanup function
    return () => {
      mediaQuery.removeEventListener('change', handleChange)
    }
  }

  // Initialize
  onMounted(() => {
    loadDarkModePreference()
    setupSystemPreferenceWatcher()
  })

  return {
    isDark,
    toggleDarkMode,
    setDarkMode
  }
}