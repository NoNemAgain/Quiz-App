export default {
    clear() {
        window.sessionStorage.clear();
    },
    saveNumberOfQuestion(numberOfQuestion) {
        window.sessionStorage.setItem("numberOfQuestion", numberOfQuestion);
    },
    getNumberOfQuestion() {
        return window.sessionStorage.getItem("numberOfQuestion");
    },
    saveToken(token) {
        window.sessionStorage.setItem("token", token);
    },
    getToken() {
        return window.sessionStorage.getItem("token");
    }
  };