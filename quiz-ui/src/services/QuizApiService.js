import axios from "axios";

const instance = axios.create({
	baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        return {status: error.response.status, data: error.response.data };
      });
  },

  async getQuizInfo() {
    return await this.call("get", "quiz-info");
  },

  async getQuestion(position) {
    return await this.call("get", "/questions/" + position);
  },

  async getQuestions() {
    return await this.call("get", "/questions");
  },

  async addParticipation(playerName, answers) {
    const data = {  
      playerName,
      answers
    };
    return await this.call("post", "/participations", data);
  },

  async login(password) {
    const data = {
      password
    };
    return await this.call("post", "/login", data);
  },

  async deleteQuestion(position, token) {
    return await this.call("delete", "/questions/" + position, null, token);
  },

  async addQuestion(question, token) {
    return await this.call("post", "/questions", question, token);
  },

  async updateQuestion(position, question, token) {
    return await this.call("put", "/questions/" + position, question, token);
  }
};