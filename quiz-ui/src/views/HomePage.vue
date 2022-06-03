<template>
  <div>
    <div class="container-fluid">
      <div class="row d-flex justify-content-center align-items-center">
        <div class="col-sm-12 col-md-7 col-lg-8 welcome-box">
          <div class="welcome-text">Bienvenue sur Quiz</div>
          <div class="welcome-text">Tester vos conaissance avec ce quiz !</div>
          <button btn class="btn btn-primary" @click="this.$router.push('/start-new-quiz-page')">Commencer</button>
          <button btn class="btn btn-primary leaderboard-btn" @click="showLeaderboardModal">Voir classement</button>
        </div>
        <div class="col-sm-12 col-md-5 col-lg-4">
          <LeaderboardDisplay class="leaderboard-main" title="Classement" :registeredScores="registeredScores" />
        </div>
      </div>
    </div>
    
    <!-- Modal -->
    <div class="modal" ref="classementModal" aria-hidden="false" tabindex="-1">
      <div class="modal-dialog modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
            <button type="button" class="btn-close" @click="hideLeaderboardModal"></button>
          </div> 
          <div class="modal-body">
            <LeaderboardDisplay title="Classement" :registeredScores="registeredScores" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import LeaderboardDisplay from "@/components/LeaderboardDisplay.vue";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: [],
    };
  },
  async created() {
    let quizInfo = await quizApiService.getQuizInfo();
    if(quizInfo.status === 200) {
      this.registeredScores = quizInfo.data.scores;
    } else {
      // gérer erreur
    }
    
  },
  components: {
    LeaderboardDisplay
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

.welcome-box {
  text-align: center;
}

.welcome-text {
  font-size: 30px;
}

.leaderboard-btn {
  display: none;
}

.leaderboard-main {
  display: block;
}

@media (max-width: 576px) {
  .leaderboard-btn {
    display: inline-block;
  }
  .leaderboard-main {
    display: none;
  }
}

</style>