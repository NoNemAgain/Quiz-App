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
        window.localStorage.setItem("token", token);
    },
    getToken() {
        return window.localStorage.getItem("token");
    },
    removeToken() {
        return window.localStorage.removeItem("token");
    }
  };