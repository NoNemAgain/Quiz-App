<template>
  <div class="page">
    <div class="new-quiz-container">
      <h3>Saisissez votre nom</h3>
      <div class="input-box">
        <form>
          <input type="text" class="form-control form-control-custom username-input" id="username" v-model="username" required>
          <button class="btn btn-primary btn-custom username-btn" @click="launchNewQuiz">GO !</button>
        </form>
      </div>
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

.new-quiz-container {
  height: 100%;
  display: flex;
  flex-flow: column;
  justify-content: center;
  align-items: center;
}

.input-box {
  margin-top: 30px;
 text-align: center;
}

</style>