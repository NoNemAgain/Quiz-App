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
            <button class="btn btn-primary score-leaderboard-btn" @click="showLeaderboardModal">Voir classement</button>
            <button class="btn btn-primary" @click="this.$router.push('/')">Retour au menu</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal -->
    <div class="modal" ref="classementModal" aria-hidden="false" tabindex="-1">
      <div class="modal-dialog modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Classement</h5>
            <button type="button" class="btn-close" @click="hideLeaderboardModal"></button>
          </div> 
          <div class="modal-body">
            <LeaderboardDisplay :registeredScores="registeredScores" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import participationStorageService from "@/services/ParticipationStorageService";
import LeaderboardDisplay from "@/components/LeaderboardDisplay.vue";
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
    OldScoresDisplay
  },
  methods: {
    showLeaderboardModal(){
      const modalElement = this.$refs.classementModal;
      modalElement.style.display = "block";
    },
    hideLeaderboardModal(){
      const modalElement = this.$refs.classementModal;
      modalElement.style.display = "none";
    },
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