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
      </nav>

      <section class="home-hero">
        <div>
          <p class="home-kicker">COMPATIBILIDADE CONVERSACIONAL</p>
          <h1 class="home-title">
            Descubra a <span>sintonia</span> por trás do diálogo.
          </h1>
          <p class="home-subtitle">
            IA que analisa conversas textuais e revela o grau de compatibilidade entre pessoas — estilo, emoção e dinâmica.
          </p>

          <div class="home-actions">
            <Button
              label="Analisar Conversa"
              class="btn-primary"
              @click="goToChat"
            />
          </div>
        </div>

        <Card class="home-score-card">
          <template #content>
            <div class="home-score">
              <CompatibilityRing :score="87" :size="220" />
              <small class="home-score__tag">compatibilidade.alta</small>
            </div>
          </template>
        </Card>
      </section>

      <Divider />

      <section id="demo" class="home__grid">
        <div class="home__section-head">
          <p class="home-kicker">DEMO</p>
          <h2>Análise de compatibilidade em tempo real.</h2>
        </div>

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
      </section>

      <Divider />

      <section id="metrics" class="home__grid">
        <div class="home__section-head">
          <p class="home-kicker">MÉTRICAS</p>
          <h2>Dimensões de análise e explicabilidade.</h2>
        </div>

        <Card>
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
          <Button label="Iniciar Análise" icon="pi pi-send" class="btn-primary" @click="goToChat" />
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
  padding-bottom: 0rem;
  background: radial-gradient(ellipse 125% 95% at 50% 22%, #2a1034 0%, #280830 48%, #120618 100%);
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
  margin: 0 auto;
  display: grid;
  padding: 2rem;
}

.home-container :deep(.p-card) {
  border: 1px solid color-mix(in srgb, var(--token-border) 45%, transparent);
  background: color-mix(in srgb, var(--token-bg-surface) 30%, #25143177) !important;
  backdrop-filter: blur(8px);
  box-shadow: inset 0 1px 0 color-mix(in srgb, #ffffff 5%, transparent);
}

.home-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.home-nav__links {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: clamp(1.25rem, 3vw, 2.35rem);
}

.home-nav__links a {
  font-size: 0.88rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  color: color-mix(in srgb, var(--token-text) 78%, transparent);
  text-decoration: none;
  transition: color 0.2s ease;
}

.home-nav__links a:hover {
  color: color-mix(in srgb, var(--color-primary) 55%, var(--token-text));
}

.home-brand {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.home-brand__mark {
  width: 2.35rem;
  height: 2.35rem;
  border-radius: 0.55rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: color-mix(in srgb, var(--token-bg-surface) 72%, #0a050c);
  border: 1px solid color-mix(in srgb, var(--token-border) 32%, transparent);
  box-shadow:
    inset 0 1px 0 color-mix(in srgb, #ffffff 7%, transparent),
    0 4px 18px rgba(0, 0, 0, 0.35);
}

.home-brand__dot {
  width: 0.78rem;
  height: 0.78rem;
  border-radius: 999px;
  background: linear-gradient(160deg, #5df2a5, var(--color-primary));
  box-shadow: 0 0 14px color-mix(in srgb, var(--color-primary) 42%, transparent);
}

.home-brand__name {
  font-weight: 700;
  font-size: 1.35rem;
}

.home-hero {
  display: grid;
  grid-template-columns: 1.25fr 0.9fr;
  align-items: center;
  gap: 2.2rem;
  min-height: 55vh;
}

.home-kicker {
  color: color-mix(in srgb, var(--color-primary) 88%, #c4fff2);
  letter-spacing: 0.42em;
  font-size: 0.8rem;
  margin: 0 0 1.1rem;
}

.home-title {
  font-size: clamp(2.8rem, 6.4vw, 4rem);
  line-height: 0.96;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.02em;
}

.home-title span {
  color: var(--color-primary);
}

.home-subtitle {
  margin-top: 1.35rem;
  max-width: 38rem;
  color: color-mix(in srgb, var(--token-text) 94%, #ffffff);
  line-height: 1.65;
  font-size: clamp(1rem, 1.6vw, 1.2rem);
}

.home-actions {
  margin-top: 1.8rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.9rem;
}

.home-page :deep(.p-button.btn-primary) {
  border-radius: 999px;
  padding-block: 0.85rem;
  padding-inline: clamp(1.35rem, 4vw, 2rem);
  box-shadow: 0 4px 14px rgba(90, 219, 148, 0.25);
  transform-origin: center;
  transition:
    transform 0.22s ease,
    box-shadow 0.22s ease,
    background-color 0.2s ease,
    color 0.2s ease,
    border-color 0.2s ease;
}

.home-page :deep(.p-button.btn-primary:not(:disabled):hover) {
  transform: scale(1.1);
  box-shadow: 0 10px 28px rgba(11, 161, 140, 0.42);
}

@media (prefers-reduced-motion: reduce) {
  .home-page :deep(.p-button.btn-primary),
  .home-page :deep(.p-button.btn-primary:not(:disabled):hover) {
    transition-duration: 0.01ms;
  }

  .home-page :deep(.p-button.btn-primary:not(:disabled):hover) {
    transform: none;
  }
}

.home-score-card {
  border-radius: 1.45rem;
}

.home-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.35rem;
  padding: 1.5rem 1rem 1.65rem;
  text-align: center;
}

.home-score__tag {
  margin: 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace;
  font-size: 0.82rem;
  color: color-mix(in srgb, var(--token-text) 88%, transparent);
  letter-spacing: 0.02em;
}

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

  .home-nav {
    justify-content: space-between;
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
