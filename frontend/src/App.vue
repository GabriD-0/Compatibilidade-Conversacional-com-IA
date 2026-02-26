<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <nav class="nav" aria-label="Navegação principal">
      <div class="nav-inner">
        <RouterLink to="/" class="logo">Compatibilidade com IA</RouterLink>
        <ul class="nav-links">
          <li><RouterLink to="/chat" active-class="active">Chat</RouterLink></li>
          <li><RouterLink to="/dashboard" active-class="active">Dashboard</RouterLink></li>
        </ul>
      </div>
    </nav>
    <main class="main">
      <RouterView />
    </main>
  </div>
</template>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.nav {
  background: #2c3e50;
  color: #fff;
  padding: 0.75rem 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.nav-inner {
  max-width: 960px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.75rem;
}
.logo {
  font-weight: 700;
  font-size: 1.1rem;
  color: #fff;
  text-decoration: none;
}
.logo:hover {
  text-decoration: underline;
}
.nav-links {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: 1rem;
}
.nav-links a {
  color: #ecf0f1;
  text-decoration: none;
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
}
.nav-links a:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}
.nav-links a.active {
  background: #42b883;
  color: #fff;
}
.main {
  flex: 1;
  background: #f5f5f5;
}
</style>

<style scoped>
</style>
