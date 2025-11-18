<!DOCTYPE html>
<template>
  <div class="sidebar">
    <!-- Existing sidebar content -->

    <!-- Add Usage Dashboard component -->
    <UsageDashboard />
  </div>
</template>

<script>
// Import the UsageDashbord component
import UsageDashboard from './UsageDashboard.vue'

export default {
  name: 'Sidebar',
  components: {
    UsageDashboard
  }
}
</script>
