<template>
  <div>
    <p>Bonjour</p>
    <div v-for="scoreEntry in registeredScores" :key="scoreEntry.playerName">
      {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: [],
    };
  },
  async created() {
    let quizInfo = await quizApiService.getQuizInfo();
    this.registeredScores = quizInfo.scores;
  }
};
</script>