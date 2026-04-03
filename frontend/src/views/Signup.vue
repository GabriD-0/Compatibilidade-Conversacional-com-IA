<script setup lang="ts">
import { ref } from 'vue'
import { OhVueIcon, addIcons } from 'oh-vue-icons'
import { BiEye, BiEyeSlash } from 'oh-vue-icons/icons/bi'

addIcons(BiEye, BiEyeSlash)

const showPassword = ref(false)
const showConfirmPassword = ref(false)
</script>

<template>
  <div class="login-page min-h-screen flex items-center justify-center p-4">
    <div class="login-card card w-full max-w-[400px]">
      <div class="login-icon">💬</div>
      <h1 class="mb-2 text-xl font-semibold text-primary text-center">
        Crie sua conta para continuar
      </h1>
      <p class="mb-6 text-[0.95rem] text-muted text-center">
      </p>

      <form class="flex flex-col gap-5" @submit.prevent>
        <div class="flex flex-col gap-1.5">
          <label for="name" class="text-sm font-medium text-body">Nome</label>
          <input
            id="name"
            type="text"
            placeholder="Seu nome"
            autocomplete="name"
            class="input"
          />
        </div>
        <div class="flex flex-col gap-1.5">
          <label for="email" class="text-sm font-medium text-body">E-mail</label>
          <input
            id="email"
            type="email"
            placeholder="seu@email.com"
            autocomplete="email"
            class="input"
          />
        </div>
        <div class="flex flex-col gap-1.5">
          <label for="password" class="text-sm font-medium text-body">Senha</label>
          <div class="password-input-wrapper">
            <input
              id="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="••••••••"
              autocomplete="new-password"
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
        <div class="flex flex-col gap-1.5">
          <label for="confirm-password" class="text-sm font-medium text-body">Confirmar senha</label>
          <div class="password-input-wrapper">
            <input
              id="confirm-password"
              :type="showConfirmPassword ? 'text' : 'password'"
              placeholder="••••••••"
              autocomplete="new-password"
              class="input input-with-icon"
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
        </div>
        <button type="submit" class="btn-primary mt-1">
          Cadastrar
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