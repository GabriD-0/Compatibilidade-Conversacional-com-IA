<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="home-page">
    <header class="home-page__hero">
      <h1 class="home-page__title">Bem-vindo</h1>
      <p class="home-page__subtitle">
        Sistema de Compatibilidade Conversacional com IA. Analise diálogos,
        visualize scores e métricas em um só lugar.
      </p>
    </header>

    <section class="home-page__cards">
      <article class="home-card card" @click="router.push('/home/chat')">
        <span class="home-card__icon">💬</span>
        <h2 class="home-card__title">Chat</h2>
        <p class="home-card__text">
          Insira e visualize diálogos para obter análise de compatibilidade.
        </p>
        <span class="home-card__action">Acessar Chat →</span>
      </article>
      <article class="home-card card" @click="router.push('/home/dashboard')">
        <span class="home-card__icon">📊</span>
        <h2 class="home-card__title">Dashboard</h2>
        <p class="home-card__text">
          Métricas agregadas, distribuição de scores e explicabilidade.
        </p>
        <span class="home-card__action">Acessar Dashboard →</span>
      </article>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  max-width: 720px;
}

.home-page__hero {
  margin-bottom: 2.5rem;
}

.home-page__title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--token-text);
  margin: 0 0 0.5rem;
  letter-spacing: -0.02em;
}

.home-page__subtitle {
  font-size: 1rem;
  color: var(--token-text-muted);
  margin: 0;
  line-height: 1.6;
}

.home-page__cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
}

.home-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border-color: rgba(90, 219, 148, 0.25);
}

.home-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2),
              0 0 0 1px rgba(90, 219, 148, 0.2);
}

.home-card__icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 0.75rem;
}

.home-card__title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-primary);
  margin: 0 0 0.5rem;
}

.home-card__text {
  font-size: 0.9rem;
  color: var(--token-text-muted);
  margin: 0 0 1rem;
  line-height: 1.5;
}

.home-card__action {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-secondary);
}

@media (prefers-color-scheme: light) {
  .home-card:hover {
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.1),
                0 0 0 1px rgba(11, 161, 140, 0.2);
  }
}
</style>
