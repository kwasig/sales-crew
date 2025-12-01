<!-- App.vue -->
<template>
  <div class="h-screen bg-white dark:bg-dark-900 transition-colors duration-200">
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
</script>
