<template>
  <header class="shadow-md bg-white dark:bg-dark-800">
    <div class="h-16 mx-auto px-4 sm:px-6 flex items-center justify-between">
      <!-- Left: Logo & Brand -->
      <div class="flex items-center space-x-2 sm:space-x-4">
        <div class="flex-shrink-0">
          <img 
            src="https://sambanova.ai/hubfs/sambanova-logo-black.png" 
            alt="Samba Sales Co-Pilot Logo" 
            class="h-6 sm:h-8 dark:invert"
          />
        </div>
        <h1 class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
          Samba Sales Co-Pilot
        </h1>
      </div>

      <!-- Right: User Button and DateTime -->
      <div class="flex items-center space-x-4">
        <div class="hidden sm:block text-sm text-gray-600 dark:text-gray-400">
          {{ currentDateTime }}
        </div>
        
        <!-- Dark Mode Toggle -->
        <button
          @click="toggleDarkMode"
          class="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
          :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
        >
          <svg v-if="isDark" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd" />
          </svg>
          <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
          </svg>
        </button>
        
        <button
          @click="openSettings"
          class="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </button>
        <SignedIn>
          <UserButton 
            afterSignOutUrl="/login" 
            :appearance="{ elements: { avatarBox: 'h-8 w-8 sm:h-10 sm:w-10' } }"
          />
        </SignedIn>
      </div>
    </div>
    
    <SettingsModal ref="settingsModalRef" @keysUpdated="onKeysUpdated" />
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { SignedIn, UserButton } from '@clerk/vue'
import SettingsModal from './SettingsModal.vue'
import { useDarkMode } from '../composables/useDarkMode'

const settingsModalRef = ref(null)
const { isDark, toggleDarkMode } = useDarkMode()

const emit = defineEmits(['keysUpdated'])

const currentDateTime = computed(() => {
  const now = new Date()
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'full',
    timeStyle: 'medium'
  }).format(now)
})

const openSettings = () => {
  settingsModalRef.value.isOpen = true
}

const onKeysUpdated = () => {
  emit('keysUpdated')
}

// **Line 70**: Expose the openSettings method
defineExpose({
  openSettings
})
</script>