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
        console.error(error);
      });
  },
  async getQuizInfo() {
    return await this.call("get", "quiz-info");
  },
  async getQuestion(position) {
    return await this.call("get", "/questions/" + position);
  },
  async addParticipation(username, answer) {
    const data = {  
      username,
      answer
    };
    return await this.call("post", "/participations", data);
  }
};