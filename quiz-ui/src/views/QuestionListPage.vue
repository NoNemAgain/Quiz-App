<template>
  <div class="page">
    
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