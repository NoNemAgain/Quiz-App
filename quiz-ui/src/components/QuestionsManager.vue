<template>
  <div>
    <QuestionDisplay 
      :question="currentQuestion" 
      :currentQuestionPosition="currentQuestionPosition" 
      :totalNumberOfQuestion="totalNumberOfQuestion"
      @answer-selected="answerClickedHandler"/>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import QuestionDisplay from "@/components/QuestionDisplay.vue";
import participationStorageService from "@/services/ParticipationStorageService";
import generalStorageService from "@/services/GeneralStorageService";

export default {
  name: "QuestionsManager",
  data() {
    return {
      totalNumberOfQuestion: null,
      currentQuestionPosition: 1,
      currentQuestion: {
        title: '',
        image: '',
        text: '',
        possibleAnswers: []
      },
      userAnswers: []
    };
  },
  async created() {
    await this.loadQuestionByPosition()
    this.totalNumberOfQuestion = Number(generalStorageService.getNumberOfQuestion());
  },
  components: {
    QuestionDisplay
  },
  methods: {
    async loadQuestionByPosition() {
      const res = await quizApiService.getQuestion(this.currentQuestionPosition);

      const newQuestion = res.data

      this.currentQuestion = {
        title: newQuestion.title,
        image : newQuestion.image,
        text : newQuestion.text,
        possibleAnswers : newQuestion.possibleAnswers
      }
    },
    async answerClickedHandler(index) {
      this.userAnswers.push(index)
      
      if(this.currentQuestionPosition === this.totalNumberOfQuestion) {
        await this.endQuiz();
      } else {
        this.currentQuestionPosition++;
        await this.loadQuestionByPosition();
      }
    },
    async endQuiz() {
      const username = participationStorageService.getPlayerName();
      const res = await quizApiService.addParticipation(username, this.userAnswers);
      participationStorageService.saveParticipationScore(res.data.score);
      this.$router.push('/score');
    }
  }
  
};
</script>