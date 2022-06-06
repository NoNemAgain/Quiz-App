<template>
  <!-- Modal -->
  <div class="modal fade" id="leaderboardModal" tabindex="-1" role="dialog" aria-labelledby="modalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modalLabel">Classement</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <LeaderboardDisplay :registeredScores="registeredScores" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LeaderboardDisplay from "@/components/LeaderboardDisplay.vue";

export default {
  name: "LeaderboardModal",
  props: {
    registeredScores : {
      type: Object
    }
  },
  components: {
    LeaderboardDisplay
  }
};
</script>