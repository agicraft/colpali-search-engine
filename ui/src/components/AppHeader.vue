<script setup lang="ts">
import { linkFactory } from '@/router';
</script>
<template>
  <div class="d-flex justify-end ga-4 right-0 px-4">
    <RouterLink :to="linkFactory.toHome()" class="text-primary text-decoration-none">
      Главная
    </RouterLink>
    <RouterLink :to="linkFactory.toAdmin()" class="text-primary text-decoration-none">
      Админ. панель
    </RouterLink>
  </div>
</template>
