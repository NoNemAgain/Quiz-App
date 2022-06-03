<template>
  <div class="d-flex align-items-center justify-content-center">
    <div class="welcome-text">Saisissez votre nom</div>
    <div>
      <input type="text" class="form-control username-input" id="username" v-model="username" required>
      <button class="btn btn-primary username-btn" @click="launchNewQuiz">GO !</button>
    </div>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "NewQuizPage",
  data() {
    return {
      username : '',
    };
  },
  async created() {
    this.username = participationStorageService.getPlayerName();
  },
  methods: {
    launchNewQuiz(){
      if(this.username) {
        participationStorageService.savePlayerName(this.username);
        this.$router.push('/questions');
      }
    },
  }
};
</script>

<style>

.username-input {
  max-width: 300px;
}

.username-btn {
  margin-top: 10px;
  width: 100%;
  max-width: 200px;
}

</style>