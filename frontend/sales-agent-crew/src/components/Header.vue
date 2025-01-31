<template>
  <header class="shadow-md bg-white">
    <div class="h-16 mx-auto px-4 sm:px-6 flex items-center justify-between">
      <!-- Left: Logo & Brand -->
      <div class="flex items-center space-x-2 sm:space-x-4">
        <div class="flex-shrink-0">
          <img 
            src="https://sambanova.ai/hubfs/sambanova-logo-black.png" 
            alt="Samba Sales Co-Pilot Logo" 
            class="h-6 sm:h-8"
          />
        </div>
        <h1 class="text-lg sm:text-2xl font-bold text-gray-900 tracking-tight">
          Samba Sales Co-Pilot
        </h1>
      </div>

      <!-- Right: User Button and DateTime -->
      <div class="flex items-center space-x-4">
        <div class="hidden sm:block text-sm text-gray-600">
          {{ currentDateTime }}
        </div>
        <button
          @click="openSettings"
          class="p-2 text-gray-600 hover:text-gray-900 transition-colors"
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

const settingsModalRef = ref(null)

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