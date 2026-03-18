<script setup lang="ts">
import Button from 'primevue/button'
import Card from 'primevue/card'
import Divider from 'primevue/divider'
import { useRouter } from 'vue-router'
import ChatPreview from '../components/chat/ChatPreview.vue'
import CompatibilityRing from '../components/graphs/CompatibilityRing.vue'
import MetricsBar from '../components/graphs/MetricsBar.vue'
import NetworkGraph from '../components/graphs/NetworkGraph.vue'

const router = useRouter()

const features = [
  {
    title: 'Language Style Matching',
    desc: 'Análise de alinhamento no uso de palavras-função entre participantes, adaptada para PT-BR.',
    tag: 'LSM',
  },
  {
    title: 'Convergência Emocional',
    desc: 'Classificação de polaridade e intensidade dos sentimentos com avaliação de convergência entre pares.',
    tag: 'SENTIMENT',
  },
  {
    title: 'Sinais Comportamentais',
    desc: 'Tempo de resposta, equilíbrio de turnos e comprimento das mensagens como indicadores de engajamento.',
    tag: 'BEHAVIOR',
  },
]

function goToChat() {
  router.push('/chat')
}
</script>

<template>
  <div class="home-page">
    <div class="home-bg">
      <div class="home-bg__glow home-bg__glow--a"></div>
      <div class="home-bg__glow home-bg__glow--b"></div>
      <div class="home-bg__glow home-bg__glow--c"></div>
    </div>

    <div class="home-container">
      <nav class="home-nav">
        <div class="home-brand">
          <span class="home-brand__dot"></span>
          <span class="home-brand__name">ConversaIA</span>
        </div>
        <div class="home-nav__links">
          <a href="#features">Funcionalidades</a>
          <a href="#demo">Demo</a>
          <a href="#metrics">Métricas</a>
        </div>
        <Button label="Começar" class="home-btn home-btn--pill" @click="goToChat" />
      </nav>

      <section class="home-hero">
        <div>
          <p class="home-kicker">COMPATIBILIDADE CONVERSACIONAL</p>
          <h1 class="home-title">
            Descubra a
            <span>sintonia</span>
            por trás do diálogo.
          </h1>
          <p class="home-subtitle">
            IA que analisa conversas textuais e revela o grau de compatibilidade entre pessoas —
            estilo, emoção e dinâmica.
          </p>
          <div class="home-actions">
            <Button
              label="Analisar Conversa"
              icon="pi pi-arrow-right"
              icon-pos="right"
              class="home-btn home-btn--pill"
              @click="goToChat"
            />
            <Button label="Ver Demo" outlined class="home-btn home-btn--ghost" />
          </div>
        </div>

        <Card class="home-score-card">
          <template #content>
            <div class="home-score">
              <CompatibilityRing :score="87" :size="210" />
              <small>compatibilidade.alta</small>
            </div>
          </template>
        </Card>
      </section>

      <section id="demo" class="home__grid">
        <Card class="home__grid-main">
          <template #title>
            <div class="home-card-title">
              <i class="pi pi-comment home-card-title__icon"></i>
              <span>Análise em Tempo Real</span>
            </div>
          </template>
          <template #content>
            <span class="home-card-dot"></span>
            <ChatPreview />
          </template>
        </Card>

        <Card>
          <template #title>
            <div class="home-card-title">
              <i class="pi pi-bolt home-card-title__icon"></i>
              <span>Arquitetura de IA</span>
            </div>
          </template>
          <template #content>
            <NetworkGraph />
            <small class="home__muted">3 dimensões -> 1 score unificado</small>
          </template>
        </Card>

        <Card id="metrics">
          <template #title>
            <div class="home-card-title">
              <i class="pi pi-chart-bar home-card-title__icon"></i>
              <span>Dimensões de Análise</span>
            </div>
          </template>
          <template #content>
            <MetricsBar />
          </template>
        </Card>

        <Card class="home__accent-card">
          <template #content>
            <span class="home-pill">EXPLICABILIDADE</span>
            <h3>Transparência total nos resultados.</h3>
            <p class="home__muted">
              Cada score vem acompanhado de sumários explicáveis, destacando os fatores que mais
              influenciaram a compatibilidade. Conformidade com LGPD.
            </p>
            <small class="home__muted home__lgpd">
              <i class="pi pi-shield"></i>
              <span>lgpd.compliant = true</span>
            </small>
          </template>
        </Card>
      </section>

      <Divider />

      <section id="features">
        <div class="home__section-head">
          <p class="home-kicker">FUNCIONALIDADES</p>
          <h2>Três pilares, um score.</h2>
        </div>
        <div class="home__features">
          <Card v-for="feature in features" :key="feature.tag">
            <template #content>
              <span class="home-feature-tag">{{ feature.tag }}</span>
              <h3>{{ feature.title }}</h3>
              <p class="home__muted">{{ feature.desc }}</p>
            </template>
          </Card>
        </div>
      </section>

      <Card class="home__cta">
        <template #content>
          <h2>Pronto para descobrir a sintonia?</h2>
          <p class="home__muted">
            Envie uma conversa e receba o score de compatibilidade conversacional em segundos.
          </p>
          <Button label="Iniciar Análise" icon="pi pi-send" class="home-btn home-btn--pill" @click="goToChat" />
        </template>
      </Card>

      <footer class="home-footer">
        <span>© 2025 ConversaIA — Gabriel de Oliveira</span>
        <span>Engenharia de Software • Compatibilidade Conversacional com IA</span>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  position: relative;
  overflow: hidden;
  padding-bottom: 2rem;
}

.home-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.home-bg__glow {
  position: absolute;
  border-radius: 999px;
  filter: blur(120px);
}

.home-bg__glow--a {
  width: 34rem;
  height: 34rem;
  top: -18rem;
  left: -14rem;
  background: color-mix(in srgb, var(--color-secondary) 24%, transparent);
}

.home-bg__glow--b {
  width: 24rem;
  height: 24rem;
  top: 28%;
  right: -8rem;
  background: color-mix(in srgb, var(--color-accent) 18%, transparent);
}

.home-bg__glow--c {
  width: 20rem;
  height: 20rem;
  bottom: 6%;
  left: 30%;
  background: color-mix(in srgb, var(--color-primary) 20%, transparent);
}

.home-container {
  position: relative;
  z-index: 2;
  max-width: 1300px;
  margin: 0 auto;
  display: grid;
  gap: 2.2rem;
  padding: 2rem;
}

.home-container :deep(.p-card) {
  border: 1px solid color-mix(in srgb, var(--token-border) 45%, transparent);
  background: color-mix(in srgb, var(--token-bg-surface) 80%, transparent);
  backdrop-filter: blur(8px);
  box-shadow: inset 0 1px 0 color-mix(in srgb, #ffffff 5%, transparent);
}

.home-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.home-brand {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.home-brand__dot {
  width: 1.1rem;
  height: 1.1rem;
  border-radius: 999px;
  background: var(--color-primary);
  box-shadow: 0 0 0 0.35rem color-mix(in srgb, var(--color-primary) 25%, transparent);
}

.home-brand__name {
  font-weight: 700;
  font-size: 1.35rem;
}

.home-nav__links {
  display: flex;
  gap: 1.8rem;
}

.home-nav__links a {
  color: var(--token-text-muted);
  text-decoration: none;
}

.home-nav__links a:hover {
  color: var(--color-primary);
}

.home-btn {
  border-radius: 999px;
}

.home-btn--pill :deep(.p-button) {
  border-radius: 999px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  border: none;
  color: #102015;
  font-weight: 700;
  box-shadow: 0 0 30px color-mix(in srgb, var(--color-primary) 30%, transparent);
}

.home-btn--ghost :deep(.p-button) {
  border-radius: 999px;
}

.home-hero {
  display: grid;
  grid-template-columns: 1.25fr 0.9fr;
  align-items: center;
  gap: 2.2rem;
  min-height: 67vh;
}

.home-kicker {
  color: color-mix(in srgb, var(--color-primary) 88%, #c4fff2);
  letter-spacing: 0.42em;
  font-size: 0.8rem;
  margin: 0 0 1.1rem;
}

.home-title {
  font-size: clamp(2.8rem, 6.4vw, 5.2rem);
  line-height: 0.96;
  margin: 0;
  letter-spacing: -0.02em;
}

.home-title span {
  color: var(--color-primary);
}

.home-subtitle {
  margin-top: 1.35rem;
  max-width: 38rem;
  color: var(--token-text-muted);
  font-size: clamp(1rem, 1.6vw, 1.2rem);
}

.home-actions {
  margin-top: 1.8rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.9rem;
}

.home-score-card {
  border-radius: 1.45rem;
}

.home-score {
  min-height: 22rem;
  display: grid;
  place-items: center;
  text-align: center;
}

.home-score small,
.home__muted {
  color: var(--token-text-muted);
}

.home__grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.home__grid-main {
  grid-column: span 2;
  position: relative;
}

.home-card-dot {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  width: 0.86rem;
  height: 0.86rem;
  border-radius: 999px;
  background: var(--color-primary);
}

.home-card-title {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 1.08rem;
}

.home-card-title__icon {
  color: var(--color-primary);
}

.home__accent-card h3 {
  margin: 1rem 0;
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 1.05;
}

.home-pill {
  display: inline-flex;
  align-items: center;
  border: 1px solid color-mix(in srgb, var(--color-accent) 60%, transparent);
  color: color-mix(in srgb, var(--color-accent) 45%, var(--token-text));
  border-radius: 999px;
  padding: 0.34rem 0.78rem;
  font-size: 0.78rem;
  letter-spacing: 0.12em;
  font-weight: 700;
}

.home__lgpd {
  margin-top: 1rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace;
}

.home__section-head {
  margin-bottom: 1rem;
}

.home__section-head h2 {
  margin: 0.6rem 0 0;
  font-size: clamp(2.3rem, 5vw, 4rem);
  line-height: 1.05;
  letter-spacing: -0.02em;
}

.home__features {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.home__features h3 {
  margin: 0.85rem 0;
  font-size: 2rem;
  line-height: 1.08;
}

.home-feature-tag {
  display: inline-block;
  color: color-mix(in srgb, var(--color-primary) 70%, var(--token-text));
  font-size: 0.85rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
}

.home__cta {
  text-align: center;
  padding: 2.4rem 0;
}

.home__cta p {
  margin: 0.85rem auto 1.3rem;
  max-width: 42rem;
}

.home__cta h2 {
  font-size: clamp(2.15rem, 4vw, 3.3rem);
  letter-spacing: -0.02em;
}

.home-footer {
  border-top: 1px solid color-mix(in srgb, var(--token-border) 25%, transparent);
  padding-top: 1.5rem;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
  color: color-mix(in srgb, var(--token-text) 64%, transparent);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace;
  font-size: 0.84rem;
}

@media (max-width: 1100px) {
  .home-nav__links {
    display: none;
  }

  .home-hero {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .home__grid {
    grid-template-columns: 1fr;
  }

  .home__grid-main {
    grid-column: auto;
  }

  .home__features {
    grid-template-columns: 1fr;
  }

  .home__features h3 {
    font-size: 1.55rem;
  }
}
</style>
