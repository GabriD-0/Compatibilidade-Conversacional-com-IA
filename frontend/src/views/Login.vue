<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { isAxiosError } from 'axios'
import { OhVueIcon, addIcons } from 'oh-vue-icons'
import { BiEye, BiEyeSlash } from 'oh-vue-icons/icons/bi'
import { useAuthStore } from '../stores/auth'

addIcons(BiEye, BiEyeSlash)

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const emailError = ref('')
const passwordError = ref('')
const generalError = ref('')

async function handleSubmit() {
  emailError.value = ''
  passwordError.value = ''
  generalError.value = ''
  isLoading.value = true

  try {
    await authStore.login(email.value, password.value)
    router.push('/home')
  } catch (err: unknown) {
    if (isAxiosError(err)) {
      const code = err.response?.data?.error?.code
      const message = err.response?.data?.error?.message ?? 'Erro ao fazer login.'

      if (code === 'missing_identifier' || code === 'invalid_email') {
        emailError.value = message
      } else if (code === 'missing_password') {
        passwordError.value = message
      } else {
        generalError.value = message
      }
    } else {
      generalError.value = 'Erro inesperado. Tente novamente.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-page min-h-screen flex items-center justify-center p-4">
    <div class="login-card card w-full max-w-[400px]">
      <div class="login-icon">💬</div>
      <h1 class="mb-2 text-xl font-semibold text-primary text-center">
        Compatibilidade Conversacional com IA
      </h1>
      <p class="mb-6 text-[0.95rem] text-muted text-center">
        Entre na sua conta para continuar
      </p>

      <p v-if="generalError" class="mb-4 text-sm text-red-500 text-center">{{ generalError }}</p>

      <form class="flex flex-col gap-5" @submit.prevent="handleSubmit">
        <div class="flex flex-col gap-1.5">
          <label for="email" class="text-sm font-medium text-body">E-mail</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="seu@email.com"
            autocomplete="email"
            class="input"
            :class="{ 'input--error': emailError }"
          />
          <p v-if="emailError" class="text-xs text-red-500">{{ emailError }}</p>
        </div>
        <div class="flex flex-col gap-1.5">
          <div class="flex items-center justify-between">
            <label for="password" class="text-sm font-medium text-body">Senha</label>
            <!-- <RouterLink to="/forget-password" class="login-link">Esqueceu a senha?</RouterLink> -->
          </div>
          <div class="password-input-wrapper">
            <input
              id="password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="••••••••"
              autocomplete="current-password"
              class="input input-with-icon"
              :class="{ 'input--error': passwordError }"
            />
            <button
              type="button"
              class="password-toggle"
              :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'"
              @click="showPassword = !showPassword"
            >
              <OhVueIcon :name="showPassword ? 'bi-eye-slash' : 'bi-eye'" />
            </button>
          </div>
          <p v-if="passwordError" class="text-xs text-red-500">{{ passwordError }}</p>
        </div>
        <button type="submit" class="btn-primary mt-1" :disabled="isLoading">
          {{ isLoading ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-muted">
        Não tem conta?
        <RouterLink to="/signup" class="login-link ml-1">Criar conta</RouterLink>
      </p>
    </div>
  </div>
</template>

<style src="../styles/auth.css"></style>