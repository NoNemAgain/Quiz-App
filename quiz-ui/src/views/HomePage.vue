<template>
  <div class="page">
    <div class="container-fluid home-page-container">
      <div class="row home-page-row">
        <div class="col-sm-12 col-md-7 col-lg-8 welcome-box">
          <div class="welcome-text">
            <h2>Bienvenue</h2>
            <h5>Tester vos conaissance avec ce quiz</h5>
          </div>
          <div class="welcome-btn">
            <button btn class="btn btn-primary" @click="this.$router.push('/start-new-quiz-page')">Commencer</button>
            <button btn class="btn btn-primary leaderboard-btn" @click="showLeaderboardModal">Voir classement</button>
          </div>   
        </div>
        <div class="col-sm-12 col-md-5 col-lg-4 leaderboard-box">
          <h3>Classement</h3>
          <LeaderboardDisplay title="Classement" :registeredScores="registeredScores" />
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
import generalStorageService from "@/services/GeneralStorageService";

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
      generalStorageService.saveNumberOfQuestion(quizInfo.data.size);
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
  align-self: center;
}

.welcome-text {
  font-size: 30px;
}

.leaderboard-btn {
  display: none;
}

.leaderboard-box {
  display: initial;
  text-align: center;
  align-self: center;
}

@media (max-width: 576px) {

  .leaderboard-btn {
    display: inline-block;
  }

  .leaderboard-box {
    display: none;
  }

  .welcome-box {
    height: 100%;
    display: flex;
    flex-flow: column;
    justify-content: space-between;
    padding: 30px 12px;
  }

}

.home-page-container {
  height: 100%;
}

.home-page-row {
  height: 100%;
  display: flex;
}



</style>