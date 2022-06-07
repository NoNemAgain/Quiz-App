<template>
  <div>
    <button class="btn btn-primary" @click="modifierQestion()">Modifier</button>
    <button class="btn btn-danger" @click="deleteQuestion()">Supprimer</button>
    <QuestionDisplay 
      :question="currentQuestion" 
      :currentQuestionPosition="position" 
      :totalNumberOfQuestion="totalNumberOfQuestion"
      :adminMode="true"
      @answer-selected="answerClickedHandler"/>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import generalStorageService from "@/services/GeneralStorageService";
import QuestionDisplay from "@/components/QuestionDisplay.vue";

export default {
  name: "AdminLoginPage",
  data() {
    return {
      currentQuestion: {
        title: '',
        image: '',
        text: '',
        possibleAnswers: []
      },
      position: Number(this.$route.params.position),
      totalNumberOfQuestion: 0
    };
  },
  async created() {
    await this.loadQuestionByPosition();
    this.totalNumberOfQuestion = Number(await generalStorageService.getNumberOfQuestion());
    this.token = generalStorageService.getToken();
  },
  components: {
    QuestionDisplay
  },
  methods: {
    async loadQuestionByPosition() {
      const res = await quizApiService.getQuestion(this.position);

      const newQuestion = res.data

      this.currentQuestion = {
        title: newQuestion.title,
        image : newQuestion.image,
        text : newQuestion.text,
        possibleAnswers : newQuestion.possibleAnswers
      }
    },
    modifierQestion() {
      this.$router.push(`/questionEdition/${ this.position }`)
    },
    deleteQuestion() {
      quizApiService.deleteQuestion(this.position, this.token);
      this.$router.push('/admin')
    },
    async answerClickedHandler() {

    }
  }
};
</script>
