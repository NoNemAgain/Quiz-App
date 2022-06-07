<template>
  <header>
    <div class="wrapper">
      <nav class="navbar bg-light quiz-app-navbar">
        <RouterLink class="navbar-brand" to="/">
          <img src="@/assets/full_logo.png" alt="App_logo" height="24"/>
        </RouterLink>
        <div>
          <div class="nav_links">
            <RouterLink class="nav-link navbar-link navbar-link-home" to="/">Accueil</RouterLink>
          </div>
          <div class="nav_links">
            <span class="vl"></span>
            <RouterLink class="nav-link navbar-link" to="/admin">Administrateur</RouterLink>
          </div>
          <div class="nav_links" v-if="adminMode">
            <span class="vl"></span>
            <a class="nav-link navbar-link logout-btn" @click="logoutHandler">Déconnexion</a>
          </div>
        </div>
      </nav>
    </div>
  </header>
  <AlertPopup v-show="errorMsg" :errorMsg="errorMsg" @close-alert="closeAlertPopup" />

  <RouterView @show-alert="showAlertPopup" @set-logout-btn="setLogoutBtn"/>
</template>

<script>
import AlertPopup from "@/components/AlertPopup.vue";
import generalStorageService from "@/services/GeneralStorageService";

export default {
  data() {
    return {
      errorMsg: '',
      adminMode: ''
    };
  },
  async created() {
    this.adminMode = generalStorageService.getToken();
    console.log(this.adminMode)
  },
  components: {
    AlertPopup,
  },
  methods: {
    async showAlertPopup(message) {
      this.errorMsg = message;
    },
    async closeAlertPopup() {
      this.errorMsg = '';
    },
    logoutHandler() {
      generalStorageService.removeToken();
      this.adminMode=''

      // 
      if(this.$route.name === 'Admin') {
        window.location.reload();
      } else {
        this.$router.push('/admin');
      } 
    },
    setLogoutBtn(adminMode) {
      this.adminMode=adminMode;
    }
  }
};
</script>


<style>
@import '@/assets/base.css';

.navbar-brand {
  padding: 0;
  padding-left: 10px;
}

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

.nav_links {
  display: inline;
}

.logout-btn {
  color: var(--red-color);
}

</style>
