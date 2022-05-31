<template>
  <form>
    <div>
      <label for="username" class="form-label">Saisissez votre nom :</label>
      <input type="text" class="form-control" id="username" v-model="username" required>
    </div>
    <div>
      <button class="btn btn-outline-danger" @click="launchNewQuiz">GO !</button>
    </div>
  </form>

    

</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";
// import quizApiService from "@/services/quizApiService";

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
  methods:{
    launchNewQuiz(){
      if(this.username) {
        participationStorageService.savePlayerName(this.username);
        this.$router.push('/questions');
      }
    },
  }
};
</script>