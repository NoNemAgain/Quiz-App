<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav class="navbar bg-light quiz-app-navbar">
        <RouterLink class="navbar-brand" to="/">
          <img src="https://getbootstrap.com/docs/5.2/assets/brand/bootstrap-logo.svg" alt="" width="30" height="24"/>
        </RouterLink>
        <div>
          <RouterLink class="nav-link navbar-link navbar-link-home" to="/">Home</RouterLink>
          <span class="vl"></span>
          <RouterLink class="nav-link navbar-link" to="/admin">Administrateur</RouterLink>
        </div>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style>
@import '@/assets/base.css';

.navbar-link {
  display: inline;
}

.vl {
  height: 100%;
  display: inline;
  border-left: 2px solid;
  color: var(--color-border);
}

@media (max-width: 576px) {
  .navbar-link-home {
    display: none;
  }
  .vl {
    display: none;
  }
}

</style>
