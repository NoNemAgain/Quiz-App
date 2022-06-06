<template>
  <div class="page">

    <AlertPopup v-show="errorMsg" :errorMsg="errorMsg" />

    <div class="container-fluid home-page-container">
      <div class="row home-page-row">
        <div class="col-sm-12 col-md-7 col-lg-8 welcome-box">
          <img class="welcome-img" src="@/assets/full_logo.png" alt="App_logo"/>
          <div class="welcome-text">
            <h2>Bienvenue</h2>
            <h5>Testez vos connaissances avec ce quiz</h5>
          </div>
          <div class="welcome-btn">
            <button btn class="btn btn-primary" @click="this.$router.push('/start-new-quiz-page')">Commencer</button>
            <button type="button" class="btn btn-primary leaderboard-btn" data-toggle="modal" data-target="#leaderboardModal">
              Voir classement
            </button>
          </div>   
        </div>
        <div class="col-sm-12 col-md-5 col-lg-4 leaderboard-box">
          <h3>Classement</h3>
          <LeaderboardDisplay :registeredScores="registeredScores" />
        </div>
      </div>
    </div>

    <LeaderboardModal :registeredScores="registeredScores" />

  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import LeaderboardDisplay from "@/components/LeaderboardDisplay.vue";
import AlertPopup from "@/components/AlertPopup.vue";
import LeaderboardModal from "@/components/LeaderboardModal.vue";
import generalStorageService from "@/services/GeneralStorageService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: [],
      errorMsg: ''
    };
  },
  async created() {
    let quizInfo = await quizApiService.getQuizInfo();
    if(quizInfo.status === 200) {
      this.registeredScores = quizInfo.data.scores;
      generalStorageService.saveNumberOfQuestion(quizInfo.data.size);
    } else {
      this.errorMsg = "Une erreur est survenue lors de la communication avec le serveur";
    }
    
  },
  components: {
    LeaderboardDisplay,
    AlertPopup,
    LeaderboardModal
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

.welcome-img {
  max-width: 300px;
  width: 80%;
  align-self: center;
}

.leaderboard-btn {
  display: none;
}

.leaderboard-box {
  display: initial;
  text-align: center;
  align-self: center;
  height: 100%;
  padding: 30px 0px;
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
  padding: 20px 20px;
  height: 100%;
}

.home-page-row {
  height: 100%;
  display: flex;
}

</style>