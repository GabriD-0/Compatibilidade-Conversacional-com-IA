<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { OhVueIcon, addIcons } from 'oh-vue-icons'
import { BiHouse, BiChat, BiChevronLeft, BiChevronRight, BiBoxArrowLeft } from 'oh-vue-icons/icons/bi'
import { MdDashboard } from 'oh-vue-icons/icons/md'
import { useAuthStore } from '../stores/auth'

addIcons(BiHouse, BiChat, BiChevronLeft, BiChevronRight, BiBoxArrowLeft, MdDashboard)

const isCollapsed = ref(false)
const router = useRouter()
const authStore = useAuthStore()

function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <aside
    class="sidebar"
    :class="{ 'sidebar--collapsed': isCollapsed }"
    aria-label="Menu de navegação"
  >
    <div class="sidebar__inner">
      <div class="sidebar__header">
      <div class="sidebar__logo">💬</div>
      <div class="sidebar__brand">
        <h2 class="sidebar__title" title="Compatibilidade Conversacional com IA">CompatIA</h2>
      </div>
    </div>

    <nav class="sidebar__nav">
      <span class="sidebar__nav-label">Navegação</span>
      <RouterLink
        to="/home"
        class="sidebar__link"
        active-class="router-link-active"
        end
        title="Início"
      >
        <OhVueIcon name="bi-house" class="sidebar__link-icon" aria-hidden="true" />
        <span class="sidebar__link-text">Início</span>
      </RouterLink>
      <RouterLink
        to="/chat"
        class="sidebar__link"
        active-class="router-link-active"
        title="Chat"
      >
        <OhVueIcon name="bi-chat" class="sidebar__link-icon" aria-hidden="true" />
        <span class="sidebar__link-text">Chat</span>
      </RouterLink>
      <RouterLink
        to="/dashboard"
        class="sidebar__link"
        active-class="router-link-active"
        title="Dashboard"
      >
        <OhVueIcon name="md-dashboard" class="sidebar__link-icon" aria-hidden="true" />
        <span class="sidebar__link-text">Dashboard</span>
      </RouterLink>
    </nav>

      <div class="sidebar__footer">
        <button
          type="button"
          class="sidebar__logout"
          @click="handleLogout"
        >
          <OhVueIcon name="bi-box-arrow-left" class="sidebar__logout-icon" aria-hidden="true" />
          <span class="sidebar__logout-text">Sair</span>
        </button>
      </div>
    </div>

    <button
      type="button"
      class="sidebar__toggle"
      :aria-label="isCollapsed ? 'Expandir menu' : 'Retrair menu'"
      @click="toggleSidebar"
    >
      <OhVueIcon
        :name="isCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"
        class="sidebar__toggle-icon"
      />
    </button>
  </aside>
</template>
