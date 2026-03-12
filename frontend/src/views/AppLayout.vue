<script setup lang="ts">
import Sidebar from '../components/Sidebar.vue'
</script>

<template>
  <div class="app-layout">
    <Sidebar />
    <main class="app-layout__main">
      <RouterView />
    </main>
  </div>
</template>

<style src="../styles/layout.css"></style>