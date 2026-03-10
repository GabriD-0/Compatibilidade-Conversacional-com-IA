<script setup lang="ts">
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

      <form class="flex flex-col gap-5" @submit.prevent>
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
            <a href="#" class="login-link">Esqueceu a senha?</a>
          </div>
          <input
            id="password"
            type="password"
            placeholder="••••••••"
            autocomplete="current-password"
            class="input"
          />
        </div>
        <button type="submit" class="btn-primary mt-1">
          Entrar
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-muted">
        Não tem conta?
        <a href="#" class="login-link ml-1">Criar conta</a>
      </p>
    </div>
  </div>
</template>

<style src="../styles/auth.css"></style>