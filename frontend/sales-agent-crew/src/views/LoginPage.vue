<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-blue-50 dark:from-dark-800 dark:to-dark-900 flex items-center justify-center p-4 transition-colors duration-200">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <img 
          src="https://sambanova.ai/hubfs/sambanova-logo-black.png" 
          alt="SambaNova Logo" 
          class="h-12 mx-auto mb-6 dark:invert"
        />
        <h1 class="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-2">Sales Co-Pilot</h1>
        <p class="text-lg text-gray-600 dark:text-gray-400">AI-Powered Sales Intelligence</p>
      </div>
      
      <div class="bg-white dark:bg-dark-800 rounded-xl shadow-lg p-8">
        <SignIn 
          :appearance="{ 
            elements: {
              headerTitle: 'hidden',
              headerSubtitle: 'hidden',
              footerAction: 'hidden'
            }
          }"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { SignIn } from '@clerk/vue'
</script>