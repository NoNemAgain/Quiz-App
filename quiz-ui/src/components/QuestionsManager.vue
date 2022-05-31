<template>
  <div>
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
    <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import QuestionDisplay from "@/components/QuestionDisplay.vue";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "QuestionsManager",
  data() {
    return {
      totalNumberOfQuestion: 10,
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
  },
  components: {
    QuestionDisplay
  },
  methods: {
    async loadQuestionByPosition() {
      const newQuestion = await quizApiService.getQuestion(this.currentQuestionPosition);

      this.currentQuestion = {
        title: newQuestion.title,
        image : newQuestion.image,
        text : newQuestion.text,
        possibleAnswers : newQuestion.possibleAnswers
      }
    },
    async answerClickedHandler(index) {
      this.userAnswers.push(index)
      this.currentQuestionPosition++;

      if(this.currentQuestionPosition > this.totalNumberOfQuestion) {
        await this.endQuiz();
      } else {
        await this.loadQuestionByPosition();
      }
    },
    async endQuiz() {
      const username = participationStorageService.getPlayerName();

      await quizApiService.addParticipation(username, this.userAnswers);
    }
  }
  
};
</script>