<template>
  <div class="oldscores-table">
    <button class="btn btn-primary" @click="this.$router.push('/questionEdition')">Crée une nouvelle question</button>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Position</th>
          <th scope="col">Question</th>
          <th scope="col">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="question in questions" :key="question.position">
          <td>{{ question.position }}</td>
          <td>{{ question.title }}</td>
          <td>
            <div class="btn-group" role="group" aria-label="Basic outlined example">
              <button type="button" class="btn btn-outline-primary" @click="displayQestion(question.position)">Voir</button>
              <button type="button" class="btn btn-outline-primary" @click="modifierQestion(question.position)">Modifier</button>
              <button type="button" class="btn btn-outline-primary" @click="deleteQuestion(question.position)">Supprimer</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import generalStorageService from "@/services/GeneralStorageService";

export default {
  name: "QuestionsList",
  emits: ['show-alert'],
  data() {
    return {
      questions: []
    };
  },
  async created() {
    this.token = generalStorageService.getToken();

    // get list of questions
    const res = await quizApiService.getQuestions();
    if(res.status === 200) {
      this.questions = res.data.questions;
    } else {
      this.$emit('show-alert', "Une erreur est survenue lors de la communication avec le serveur");
    }
    // add save the number of questions
    generalStorageService.saveNumberOfQuestion(this.questions.length)
  },
  methods: {
    displayQestion(index) {
      this.$router.push(`/adminQuestion/${index}`);
    },
    async modifierQestion(index) {
      this.$router.push(`/questionEdition/${index}`);
    },
    async deleteQuestion(position) {
      await quizApiService.deleteQuestion(position, this.token);
      window.location.reload();
    }
  }
};
</script>

<style>


</style>