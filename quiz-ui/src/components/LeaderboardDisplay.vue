<template>
  <div class="leaderboard">
    <div v-for="(scoreEntry, index) in registeredScores" :key="scoreEntry.playerName" class="card leaderboard-card">
      <div class="card-body leaderboard-card-body">
        <div class="leaderboard-num">{{ index + 1 }}</div>
        <div class="leaderboard-user-name">{{ scoreEntry.playerName }}</div>
        <div class="leaderboard-user-score">Score : {{ scoreEntry.score }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LeaderboardDisplay",
  props: {
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
  height: calc(100% - 40px);
  overflow: auto;
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
  padding: 3px 10px;
}

.leaderboard-num {
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