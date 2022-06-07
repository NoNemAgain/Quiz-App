<template>
  <div class="page">
    <div v-if="!adminMode" class="login-container">
      <div class="card">
        <div class="card-body">
          <div class="login-box-header">
            <h5 class="card-title">Connexion administrateur</h5>
          </div>
          <div class="login-box-body">
            <label for="password">Mot de passe</label>
            <input type="password" class="form-control form-control-custom password-input" id="password" v-model="password" placeholder="Mot de passe">
            <p class="input-error-msg" v-if="errorMsg !== ''">{{ errorMsg }}</p>
          </div>
          <div class="login-box-footer">
            <button class="btn btn-primary btn-custom" @click="launchLogin">Connexion</button>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <QuestionsList />
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import generalStorageService from "@/services/GeneralStorageService";
import QuestionsList from "@/components/QuestionsList.vue";

export default {
  name: "AdminLoginPage",
  emits: ['show-alert', 'set-logout-btn'],
  data() {
    return {
      password: '',
      adminMode: '',
      errorMsg: ''
    };
  },
  async created() {
    this.adminMode = generalStorageService.getToken();
  },
  components: {
    QuestionsList
  },
  methods: {
    async launchLogin() {
      if(this.password) {
        const res = await quizApiService.login(this.password);

        // Password correct
        if(res.status === 200) {
          // Save token
          generalStorageService.saveToken(res.data.token);
          this.adminMode = res.data.token;
          this.$emit('set-logout-btn', this.adminMode);
        }
        // Wrong password
        else if(res.status === 401) {
          this.errorMsg = "Mauvais mot de passe";
        }
        else {
          this.$emit('show-alert', "Une erreur est survenue lors de la communication avec le serveur");
        }
      } else {
        this.errorMsg = "Veuillez entrer votre mot de passe"
      }
    }
  }
};
</script>

<style>

.login-container {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  align-content: center;
}

.login-box-body {
  padding: 15px 0px;
}

.login-box-footer {
  text-align: center;
}

</style>