<script setup lang="ts">
import { OhVueIcon, addIcons } from 'oh-vue-icons'
import { BiHouse, BiChat } from 'oh-vue-icons/icons/bi'
import { MdDashboard } from 'oh-vue-icons/icons/md'

addIcons(BiHouse, BiChat, MdDashboard)
</script>

<template>
  <aside class="app-layout__sidebar">
    <div class="sidebar__header">
      <div class="sidebar__logo">💬</div>
      <h2 class="sidebar__title">Compatibilidade Conversacional</h2>
      <p class="sidebar__subtitle">com IA</p>
    </div>
    <nav class="sidebar__nav">
      <span class="sidebar__nav-label">Navegação</span>
      <RouterLink to="/home" class="sidebar__link" active-class="router-link-active" end>
        <OhVueIcon name="bi-house" class="sidebar__link-icon" />
        Início
      </RouterLink>
      <RouterLink to="/home/chat" class="sidebar__link" active-class="router-link-active">
        <OhVueIcon name="bi-chat" class="sidebar__link-icon" />
        Chat
      </RouterLink>
      <RouterLink to="/home/dashboard" class="sidebar__link" active-class="router-link-active">
        <OhVueIcon name="md-dashboard" class="sidebar__link-icon" />
        Dashboard
      </RouterLink>
    </nav>
  </aside>
</template>
