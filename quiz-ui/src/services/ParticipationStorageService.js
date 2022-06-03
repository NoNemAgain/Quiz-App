export default {
    clear() {
        window.localStorage.clear();
        window.sessionStorage.clear();
    },
    savePlayerName(playerName) {
        window.localStorage.setItem("playerName", playerName);
    },
    getPlayerName() {		
        return window.localStorage.getItem("playerName");
    },
    removePlayerName() {
        window.localStorage.removeItem("playerName");
    },
    saveParticipationScore(participationScore) {
        window.sessionStorage.setItem("participationScore", participationScore);
    },
    getParticipationScore() {
        return window.sessionStorage.getItem("participationScore");
    }
  };