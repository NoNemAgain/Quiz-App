<template>
  <div>
    <p>Saisissez votre nom :</p>
    <input type="text" class="form-control" v-model="username">
    <button class="btn btn-outline-danger" @click="launchNewQuiz">GO !</button>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";
// import quizApiService from "@/services/quizApiService";

export default {
  name: "NewQuizPage",
  data() {
    const username = participationStorageService.getPlayerName();
    return {
      username : username
    };
  },
  async created() {

  },
  methods:{
    launchNewQuiz(){
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
    },
  }
};
</script>