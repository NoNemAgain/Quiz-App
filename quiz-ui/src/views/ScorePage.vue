<template>
  <div class="page">
    <div class="socre-page">
      <div class="container-fluid  score-container">
        <div class="row home-page-row">
          <div class="col-sm-12 col-md-6 player-score">
            <div class="new-score">
              <h3>Votre score</h3>
              <p class="score-value">{{ newScore }}</p>
            </div>
            <div>
              <h3>Vos scores précédents</h3>
              <OldScoresDisplay class="score-table" :playerRegisteredScores="registeredScores.filter(rScore => rScore.playerName === username)" />
              <!-- Leaderboard of player -->
            </div>
          </div>
          <div class="col-sm-12 col-md-6 general-leaderboard-box">
            <h3>Classement général</h3>
            <LeaderboardDisplay :registeredScores="registeredScores" />
          </div>
          <div>
            <button type="button" class="btn btn-primary btn-primary-custom leaderboard-btn" data-toggle="modal" data-target="#leaderboardModal">
              Voir classement
            </button>
            <button class="btn btn-primary btn-primary-custom" @click="this.$router.push('/')">Retour au menu</button>
          </div>
        </div>
      </div>
    </div>

    <LeaderboardModal :registeredScores="registeredScores" />
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";
import LeaderboardDisplay from "@/components/LeaderboardDisplay.vue";
import LeaderboardModal from "@/components/LeaderboardModal.vue";
import OldScoresDisplay from "@/components/OldScoresDisplay.vue";

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
  },
  components: {
    LeaderboardDisplay,
    OldScoresDisplay,
    LeaderboardModal
  }
};
</script>

<style>

.socre-page {
  height: 100%;
  padding-top: 20px;
  text-align: center;
}

.score-container {
  height: calc(100% - 90px);
}

.general-leaderboard-box {
  height: 100%;
}

.score-leaderboard-btn {
  display: none;
}

.general-leaderboard-box {
  padding-bottom: 20px;
}

@media (max-width: 768px) {

  .score-leaderboard-btn {
    display: inline-block;
  }

  .general-leaderboard-box {
    display: none;
  }

}

.score-value {
  font-size: 50px;
  font-weight: 500;
}

.score-table {
  margin-top: 20px;
}

</style>