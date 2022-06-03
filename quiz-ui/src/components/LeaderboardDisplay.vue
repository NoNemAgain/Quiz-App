<template>
  <div class="leaderboard">
    <div v-for="scoreEntry in registeredScores" :key="scoreEntry.playerName" class="card leaderboard-card">
      <div class="card-body leaderboard-card-body">
        <img src="@/assets/user.png" class="leaderboard-user-img">
        <div class="leaderboard-user-name">{{ scoreEntry.playerName }}</div>
        <div class="leaderboard-user-score">{{ scoreEntry.score }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LeaderboardDisplay",
  props: {
    title: {
      type: String
    },
    registeredScores : {
      type: Object
    }
  }
};
</script>

<style>
.leaderboard {
  padding: 20px;
  text-align: center;
}

.leaderboard .title {
  padding-bottom: 20px;
}

.leaderboard-card {
  margin: 10px 0px 10px 0px;
  /* box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px; */
}

.leaderboard-card-body {
  padding: 3px;
  padding-right: 10px;
}

.leaderboard-user-img {
  height: 30px;
  width: 30px;
  display: inline;
  float: left;
}

.leaderboard-user-name {
  display: inline;
  margin-top: 2px;
}

.leaderboard-user-score {
  display: inline;
  float: right;
  margin-top: 2px;
}

</style>