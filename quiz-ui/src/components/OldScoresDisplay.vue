<template>
  <div class="oldscores-table">
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Date</th>
          <th scope="col">Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="scoreEntry in playerRegisteredScores.slice().sort(this.daySorter).slice(0, 5)" :key="scoreEntry.date">
          <td>{{ getScoreDate(scoreEntry.date) }}</td>
          <td>{{ scoreEntry.score }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "OldScoresDisplay",
  props: {
    playerRegisteredScores : {
      type: Object
    }
  },
  async created() {
  },
  methods: {
    daySorter(a, b) {
      return new Date(b.date) - new Date(a.date);
    },
    getScoreDate(date) {
      const scoreDate = new Date(date);
      return scoreDate.getDate() + "/" + scoreDate.getMonth() + "/" + scoreDate.getFullYear();
    }
  }
};
</script>