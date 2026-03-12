<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { OhVueIcon, addIcons } from 'oh-vue-icons'
import { BiEye, BiEyeSlash } from 'oh-vue-icons/icons/bi'

addIcons(BiEye, BiEyeSlash)

const router = useRouter()
const showPassword = ref(false)

function handleSubmit() {
  router.push('/home')
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

      <form class="flex flex-col gap-5" @submit.prevent="handleSubmit">
        <div class="flex flex-col gap-1.5">
          <label for="email" class="text-sm font-medium text-body">E-mail</label>
          <input
            id="email"
            type="text"
            placeholder="seu@email.com"
            autocomplete="email"
            class="input"
          />
        </div>
        <div class="flex flex-col gap-1.5">
          <div class="flex items-center justify-between">
            <label for="password" class="text-sm font-medium text-body">Senha</label>
            <RouterLink to="/forget-password" class="login-link">Esqueceu a senha?</RouterLink>
          </div>
          <div class="password-input-wrapper">
            <input
              id="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="••••••••"
              autocomplete="current-password"
              class="input input-with-icon"
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
        </div>
        <button type="submit" class="btn-primary mt-1">
          Entrar
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