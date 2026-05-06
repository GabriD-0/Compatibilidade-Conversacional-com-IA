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

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isLoading = ref(false)
const nameError = ref('')
const emailError = ref('')
const passwordError = ref('')
const confirmPasswordError = ref('')
const generalError = ref('')

async function handleSubmit() {
  nameError.value = ''
  emailError.value = ''
  passwordError.value = ''
  confirmPasswordError.value = ''
  generalError.value = ''

  if (password.value !== confirmPassword.value) {
    confirmPasswordError.value = 'As senhas não coincidem.'
    return
  }

  isLoading.value = true

  try {
    await authStore.register(name.value, email.value, password.value)
    router.push('/home')
  } catch (err: unknown) {
    if (isAxiosError(err)) {
      const code = err.response?.data?.error?.code
      const message = err.response?.data?.error?.message ?? 'Erro ao criar conta.'

      if (code === 'missing_name' || code === 'invalid_name') {
        nameError.value = message
      } else if (code === 'missing_email' || code === 'invalid_email' || code === 'email_taken') {
        emailError.value = message
      } else if (code === 'missing_password' || code === 'invalid_password') {
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
        Crie sua conta para continuar
      </h1>
      <p class="mb-6 text-[0.95rem] text-muted text-center"></p>

      <p v-if="generalError" class="mb-4 text-sm text-red-500 text-center">{{ generalError }}</p>

      <form class="flex flex-col gap-5" @submit.prevent="handleSubmit">
        <div class="flex flex-col gap-1.5">
          <label for="name" class="text-sm font-medium text-body">Nome</label>
          <input
            id="name"
            v-model="name"
            type="text"
            placeholder="Seu nome"
            autocomplete="name"
            class="input"
            :class="{ 'input--error': nameError }"
          />
          <p v-if="nameError" class="text-xs text-red-500">{{ nameError }}</p>
        </div>
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
          <label for="password" class="text-sm font-medium text-body">Senha</label>
          <div class="password-input-wrapper">
            <input
              id="password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="••••••••"
              autocomplete="new-password"
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
        <div class="flex flex-col gap-1.5">
          <label for="confirm-password" class="text-sm font-medium text-body">Confirmar senha</label>
          <div class="password-input-wrapper">
            <input
              id="confirm-password"
              v-model="confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              placeholder="••••••••"
              autocomplete="new-password"
              class="input input-with-icon"
              :class="{ 'input--error': confirmPasswordError }"
            />
            <button
              type="button"
              class="password-toggle"
              :aria-label="showConfirmPassword ? 'Ocultar senha' : 'Mostrar senha'"
              @click="showConfirmPassword = !showConfirmPassword"
            >
              <OhVueIcon :name="showConfirmPassword ? 'bi-eye-slash' : 'bi-eye'" />
            </button>
          </div>
          <p v-if="confirmPasswordError" class="text-xs text-red-500">{{ confirmPasswordError }}</p>
        </div>
        <button type="submit" class="btn-primary mt-1" :disabled="isLoading">
          {{ isLoading ? 'Cadastrando...' : 'Cadastrar' }}
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-muted">
        Já tem conta?
        <RouterLink to="/login" class="login-link ml-1">Entrar</RouterLink>
      </p>
    </div>
  </div>
</template>

<style src="../styles/auth.css"></style>