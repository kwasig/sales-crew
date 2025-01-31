<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex min-h-screen items-center justify-center p-4">
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-black opacity-30" @click="close"></div>

      <!-- Modal -->
      <div class="relative w-full max-w-lg bg-white rounded-xl shadow-lg p-6">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-gray-900">API Settings</h2>
          <button @click="close" class="text-gray-500 hover:text-gray-700">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 text-red-700 rounded">
          {{ errorMessage }}
        </div>

        <!-- Success Message -->
        <div v-if="successMessage" class="mb-4 p-3 bg-green-100 text-green-700 rounded">
          {{ successMessage }}
        </div>

        <div class="space-y-6">
          <!-- SambaNova API Key -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              SambaNova API Key
              <a 
                href="https://cloud.sambanova.ai/"
                target="_blank"
                class="text-primary-600 hover:text-primary-700 ml-2 text-sm"
              >
                Get Key →
              </a>
            </label>
            <div class="relative">
              <input
                v-model="sambanovaKey"
                :type="sambanovaKeyVisible ? 'text' : 'password'"
                placeholder="Enter your SambaNova API Key"
                class="block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500 pr-10"
              />
              <button 
                @click="toggleSambanovaKeyVisibility"
                class="absolute inset-y-0 right-0 px-3 flex items-center text-gray-500 hover:text-gray-700"
              >
                <svg v-if="sambanovaKeyVisible" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor">
                  <!-- Eye Open Icon -->
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M2.458 12C3.732 7.943 7.519 5 12 5c4.481 0 8.268 2.943 9.542 7" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M2.458 12c1.508 4.057 5.294 7 9.542 7s8.034-2.943 9.542-7" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor">
                  <!-- Eye Closed Icon -->
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M13.875 18.825A9.952 9.952 0 0112 19.5c-5.247 0-9.645-4.028-9.985-9.227M9.642 9.642a3 3 0 104.715 4.715" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M3 3l18 18" />
                </svg>
              </button>
            </div>
            <!-- Save and Clear Buttons -->
            <div class="flex justify-end space-x-2 mt-2">
              <button 
                @click="clearSambanovaKey"
                class="px-3 py-1 text-sm bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none"
              >
                Clear Key
              </button>
              <button 
                @click="saveSambanovaKey"
                class="px-3 py-1 text-sm bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none"
              >
                Save Key
              </button>
            </div>
          </div>

          <!-- Exa API Key -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Exa API Key
              <a 
                href="https://exa.example.com/get-key"
                target="_blank"
                class="text-primary-600 hover:text-primary-700 ml-2 text-sm"
              >
                Get Key →
              </a>
            </label>
            <div class="relative">
              <input
                v-model="exaKey"
                :type="exaKeyVisible ? 'text' : 'password'"
                placeholder="Enter your Exa API Key"
                class="block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-primary-500 focus:border-primary-500 pr-10"
              />
              <button 
                @click="toggleExaKeyVisibility"
                class="absolute inset-y-0 right-0 px-3 flex items-center text-gray-500 hover:text-gray-700"
              >
                <svg v-if="exaKeyVisible" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor">
                  <!-- Eye Open Icon -->
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M2.458 12C3.732 7.943 7.519 5 12 5c4.481 0 8.268 2.943 9.542 7" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M2.458 12c1.508 4.057 5.294 7 9.542 7s8.034-2.943 9.542-7" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                     viewBox="0 0 24 24" stroke="currentColor">
                  <!-- Eye Closed Icon -->
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M13.875 18.825A9.952 9.952 0 0112 19.5c-5.247 0-9.645-4.028-9.985-9.227M9.642 9.642a3 3 0 104.715 4.715" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M3 3l18 18" />
                </svg>
              </button>
            </div>
            <!-- Save and Clear Buttons -->
            <div class="flex justify-end space-x-2 mt-2">
              <button 
                @click="clearExaKey"
                class="px-3 py-1 text-sm bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none"
              >
                Clear Key
              </button>
              <button 
                @click="saveExaKey"
                class="px-3 py-1 text-sm bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none"
              >
                Save Key
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuth } from '@clerk/vue'
import { encryptKey, decryptKey } from '../utils/encryption'

const isOpen = ref(false)
const sambanovaKey = ref('')
const exaKey = ref('')
const errorMessage = ref('')
const successMessage = ref('')

// Key visibility controls
const sambanovaKeyVisible = ref(false)
const exaKeyVisible = ref(false)

const { userId } = useAuth()

// Define the emit function
const emit = defineEmits(['keysUpdated'])

// Load keys on mount
onMounted(async () => {
  await loadKeys()
})

const loadKeys = async () => {
  try {
    const savedSambanovaKey = localStorage.getItem(`sambanova_key_${userId}`)
    const savedExaKey = localStorage.getItem(`exa_key_${userId}`)

    sambanovaKey.value = savedSambanovaKey
      ? await decryptKey(savedSambanovaKey)
      : ''
    exaKey.value = savedExaKey
      ? await decryptKey(savedExaKey)
      : ''
  } catch (error) {
    console.error('Failed to load keys:', error)
    errorMessage.value = 'Failed to load saved keys'
  }
}

// Save functions for individual keys
const saveSambanovaKey = async () => {
  try {
    if (!sambanovaKey.value) {
      errorMessage.value = 'SambaNova API key cannot be empty!'
      return
    }
    const encryptedKey = await encryptKey(sambanovaKey.value)
    localStorage.setItem(`sambanova_key_${userId}`, encryptedKey)
    successMessage.value = 'SambaNova API key saved successfully!'
    emit('keysUpdated')
  } catch (error) {
    console.error('Failed to save SambaNova key:', error)
    errorMessage.value = 'Failed to save SambaNova API key'
  } finally {
    clearMessagesAfterDelay()
  }
}

const clearSambanovaKey = () => {
  localStorage.removeItem(`sambanova_key_${userId}`)
  sambanovaKey.value = ''
  successMessage.value = 'SambaNova API key cleared successfully!'
  emit('keysUpdated')
  clearMessagesAfterDelay()
}

const saveExaKey = async () => {
  try {
    if (!exaKey.value) {
      errorMessage.value = 'Exa API key cannot be empty!'
      return
    }
    const encryptedKey = await encryptKey(exaKey.value)
    localStorage.setItem(`exa_key_${userId}`, encryptedKey)
    successMessage.value = 'Exa API key saved successfully!'
    emit('keysUpdated')
  } catch (error) {
    console.error('Failed to save Exa key:', error)
    errorMessage.value = 'Failed to save Exa API key'
  } finally {
    clearMessagesAfterDelay()
  }
}

const clearExaKey = () => {
  localStorage.removeItem(`exa_key_${userId}`)
  exaKey.value = ''
  successMessage.value = 'Exa API key cleared successfully!'
  emit('keysUpdated')
  clearMessagesAfterDelay()
}

// Toggle key visibility
const toggleSambanovaKeyVisibility = () => {
  sambanovaKeyVisible.value = !sambanovaKeyVisible.value
}

const toggleExaKeyVisibility = () => {
  exaKeyVisible.value = !exaKeyVisible.value
}

const close = () => {
  isOpen.value = false
  errorMessage.value = ''
  successMessage.value = ''
}

// Function to clear messages after a delay
const clearMessagesAfterDelay = () => {
  setTimeout(() => {
    errorMessage.value = ''
    successMessage.value = ''
  }, 3000)
}

// Expose methods and state
defineExpose({
  isOpen,
  getKeys: () => ({
    sambanovaKey: sambanovaKey.value,
    exaKey: exaKey.value,
  }),
})
</script> 