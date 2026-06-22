<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { isAxiosError } from 'axios'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const name = ref(authStore.user?.name ?? '')
const email = ref(authStore.user?.email ?? '')
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const deletePassword = ref('')
const saving = ref(false)
const deleting = ref(false)
const success = ref('')
const error = ref('')

watch(
  () => authStore.user,
  (user) => {
    name.value = user?.name ?? ''
    email.value = user?.email ?? ''
  },
)

function messageFor(err: unknown, fallback: string): string {
  if (isAxiosError(err)) {
    return err.response?.data?.error?.message ?? fallback
  }
  return fallback
}

async function saveProfile() {
  success.value = ''
  error.value = ''

  if (newPassword.value && newPassword.value !== confirmPassword.value) {
    error.value = 'A nova senha e a confirmação precisam ser iguais.'
    return
  }

  saving.value = true
  try {
    const payload: {
      name: string
      email: string
      current_password?: string
      new_password?: string
    } = { name: name.value, email: email.value }

    if (newPassword.value) {
      payload.current_password = currentPassword.value
      payload.new_password = newPassword.value
    }

    await authStore.updateProfile(payload)
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
    success.value = 'Configurações atualizadas com sucesso.'
  } catch (err) {
    error.value = messageFor(err, 'Não foi possível atualizar as configurações.')
  } finally {
    saving.value = false
  }
}

async function removeAccount() {
  success.value = ''
  error.value = ''
  if (!deletePassword.value) {
    error.value = 'Informe sua senha atual para excluir a conta.'
    return
  }

  if (!window.confirm('Excluir permanentemente sua conta e todas as conversas? Esta ação não pode ser desfeita.')) {
    return
  }

  deleting.value = true
  try {
    await authStore.deleteAccount(deletePassword.value)
    router.replace('/login')
  } catch (err) {
    error.value = messageFor(err, 'Não foi possível excluir a conta.')
  } finally {
    deleting.value = false
  }
}
</script>

<template>
  <main class="settings-page">
    <section class="settings-card">
      <header>
        <p class="settings-kicker">CONTA</p>
        <h1>Configurações</h1>
        <p>Atualize seus dados de acesso ou exclua definitivamente sua conta.</p>
      </header>

      <p v-if="error" class="settings-message settings-message--error">{{ error }}</p>
      <p v-if="success" class="settings-message settings-message--success">{{ success }}</p>

      <form class="settings-form" @submit.prevent="saveProfile">
        <label>
          Nome
          <input v-model="name" type="text" autocomplete="name" required />
        </label>
        <label>
          E-mail
          <input v-model="email" type="email" autocomplete="email" required />
        </label>

        <div class="settings-divider">Alterar senha (opcional)</div>
        <label>
          Senha atual
          <input v-model="currentPassword" type="password" autocomplete="current-password" />
        </label>
        <label>
          Nova senha
          <input v-model="newPassword" type="password" autocomplete="new-password" minlength="8" />
        </label>
        <label>
          Confirmar nova senha
          <input v-model="confirmPassword" type="password" autocomplete="new-password" minlength="8" />
        </label>
        <button class="settings-save" type="submit" :disabled="saving">
          {{ saving ? 'Salvando...' : 'Salvar alterações' }}
        </button>
      </form>

      <section class="settings-danger">
        <h2>Excluir conta</h2>
        <p>A exclusão remove a conta e as conversas associadas. Informe sua senha atual para confirmar.</p>
        <label>
          Senha atual
          <input v-model="deletePassword" type="password" autocomplete="current-password" />
        </label>
        <button class="settings-delete" type="button" :disabled="deleting" @click="removeAccount">
          {{ deleting ? 'Excluindo...' : 'Excluir minha conta' }}
        </button>
      </section>
    </section>
  </main>
</template>

<style scoped>
.settings-page {
  min-height: 100%;
  padding: 2rem;
  color: #f0ebff;
}

.settings-card {
  width: min(100%, 44rem);
  margin: 0 auto;
  padding: 2rem;
  border: 1px solid rgba(90, 219, 148, 0.18);
  border-radius: 1.25rem;
  background: rgba(18, 4, 32, 0.92);
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.38);
}

.settings-kicker { margin: 0; color: #5adb94; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.14em; }
.settings-card h1 { margin: 0.4rem 0; font-size: 1.9rem; }
.settings-card header > p:last-child, .settings-danger p { color: rgba(240, 235, 255, 0.65); line-height: 1.5; }
.settings-form, .settings-danger { display: grid; gap: 1rem; margin-top: 1.5rem; }
.settings-form label, .settings-danger label { display: grid; gap: 0.45rem; color: rgba(240, 235, 255, 0.8); font-size: 0.9rem; }
.settings-form input, .settings-danger input { padding: 0.72rem 0.8rem; border: 1px solid rgba(90, 219, 148, 0.22); border-radius: 0.55rem; background: rgba(255, 255, 255, 0.05); color: #f0ebff; }
.settings-divider { margin-top: 0.5rem; padding-top: 1.25rem; border-top: 1px solid rgba(255, 255, 255, 0.1); color: rgba(240, 235, 255, 0.58); font-size: 0.82rem; }
.settings-save, .settings-delete { padding: 0.75rem 1rem; border: 0; border-radius: 0.6rem; font-weight: 700; cursor: pointer; }
.settings-save { background: #5adb94; color: #06140e; }
.settings-danger { margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid rgba(248, 113, 113, 0.3); }
.settings-danger h2 { margin: 0; color: #f87171; font-size: 1.1rem; }
.settings-delete { justify-self: start; background: rgba(248, 113, 113, 0.14); border: 1px solid rgba(248, 113, 113, 0.45); color: #fecaca; }
.settings-message { margin: 1.25rem 0 0; padding: 0.75rem; border-radius: 0.6rem; }
.settings-message--error { background: rgba(248, 113, 113, 0.12); color: #fecaca; }
.settings-message--success { background: rgba(90, 219, 148, 0.12); color: #b5f5d0; }
button:disabled { cursor: wait; opacity: 0.65; }
@media (max-width: 640px) { .settings-page { padding: 1rem; } .settings-card { padding: 1.25rem; } }
</style>
