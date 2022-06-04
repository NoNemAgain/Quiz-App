export default {
    clear() {
        window.sessionStorage.clear();
    },
    saveNumberOfQuestion(numberOfQuestion) {
        window.sessionStorage.setItem("numberOfQuestion", numberOfQuestion);
    },
    getNumberOfQuestion() {
        return window.sessionStorage.getItem("numberOfQuestion");
    }
  };