<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <RouterView v-slot="{ Component, route }">
    <Transition name="page-fade" mode="out-in">
      <component :is="Component" :key="route.path" />
    </Transition>
  </RouterView>
</template>

<style scoped>
:deep(.page-fade-enter-active),
:deep(.page-fade-leave-active) {
  transition: opacity 0.5s ease;
}
:deep(.page-fade-enter-from),
:deep(.page-fade-leave-to) {
  opacity: 0;
}
</style>
