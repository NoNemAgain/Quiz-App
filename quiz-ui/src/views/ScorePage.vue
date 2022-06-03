<template>
  <div>
    <p>Score</p>
    <div>
      <p>Votre score</p>
      <div>
        {{ newScore }}
      </div>
    </div>

    <div>
      <p>Classement de l'utilisateur</p>
      <div v-for="scoreEntry in registeredScores.filter(rScore => rScore.playerName === username)" :key="scoreEntry.playerName">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </div>
    </div>

    <div>
      <p>Classement global</p>
      <div v-for="scoreEntry in registeredScores" :key="scoreEntry.playerName">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </div>
    </div>
    <button class="btn btn-outline-danger" @click="this.$router.push('/')">RETOUR AU MENU</button>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "ScorePage",
  data() {
    return {
      registeredScores: [],

    };
  },
  async created() {
    this.username = participationStorageService.getPlayerName();
    this.newScore = participationStorageService.getParticipationScore();

    let quizInfo = await quizApiService.getQuizInfo();
    if(quizInfo.status === 200) {
      this.registeredScores = quizInfo.data.scores;
    } else {
      // gérer erreur
    }
    
  }
};
</script>