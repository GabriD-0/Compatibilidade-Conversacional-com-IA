<script setup lang="ts">
// TODO: Implementar a lógica de recuperação de senha
</script>

<template>
  <div class="login-page min-h-screen flex items-center justify-center p-4">
    <div class="login-card card w-full max-w-[400px]">
      <div class="login-icon">💬</div>
      <h1 class="mb-2 text-xl font-semibold text-primary text-center">
        Informe sua conta para recuperar a senha
      </h1>

      <form class="flex flex-col gap-5" @submit.prevent>
        <div class="flex flex-col gap-1.5">
          <label for="account" class="text-sm font-medium text-body">Conta</label>
          <input
            id="account"
            type="text"
            placeholder="Digite a sua conta"
            autocomplete="account"
            class="input"
          />
        </div>
        <button type="submit" class="btn-primary mt-1">
          Enviar link de recuperação
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-muted">
        <RouterLink to="/login" class="login-link">Voltar ao login</RouterLink>
      </p>
    </div>
  </div>
</template>

<style src="../styles/auth.css"></style>