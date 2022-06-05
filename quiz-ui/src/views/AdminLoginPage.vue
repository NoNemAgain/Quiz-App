<template>
  <div class="page">
    <div class="login-container">
      <div class="card">
        <div class="card-body">
          <div class="login-box-header">
            <h5 class="card-title">Connexion administrateur</h5>
          </div>
            <div class="login-box-body">
              <label for="password">Psassword</label>
              <input type="password" class="form-control password-input" id="password" v-model="password" required>
              <p v-if="showWrongPwdMsg">Mauvais mot de passe</p>
            </div>
            <div class="login-box-footer">
              <button class="btn btn-primary" @click="launchLogin">Connexion</button>
            </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import generalStorageService from "@/services/GeneralStorageService";

export default {
  name: "AdminLoginPage",
  data() {
    return {
      password: ''
    };
  },
  async created() {
    this.showWrongPwdMsg = false;
  },
  methods: {
    async launchLogin() {
      if(this.password) {
        const res = await quizApiService.login(this.password);

        // Password correct
        if(res.status === 200) {
          // Save token
          generalStorageService.saveToken(res.data.token);

          
        }
        // Wrong password
        else if(res.status === 401) {
          this.showWrongPwdMsg = true;
        }
        else {
          throw 'Server error';
        }
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