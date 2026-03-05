<script setup lang="ts">
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-4 bg-page">
    <div class="card w-full max-w-[380px]">
      <h1 class="m-0 mb-1 text-xl font-semibold text-primary">
        Compatibilidade Conversacional com IA
      </h1>
      <p class="m-0 mb-6 text-[0.95rem] text-muted">
        Entre na sua conta
      </p>

      <form class="flex flex-col gap-5" @submit.prevent>
        <div class="flex flex-col gap-1">
          <label for="email" class="text-sm font-medium text-body">E-mail</label>
          <input
            id="email"
            type="text"
            placeholder="seu@email.com"
            autocomplete="email"
            class="input"
          />
        </div>
        <div class="flex flex-col gap-1">
          <label for="password" class="text-sm font-medium text-body">Senha</label>
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
    </div>
  </div>
</template>
