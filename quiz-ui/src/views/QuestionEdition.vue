<template>
  <div class="page">
    <div class="card question-edition-card">
      <h2>Question édition</h2>
      <form>
        <div class="form-group">
          <label for="questionPosition">Position</label>
          <input type="number" class="form-control" id="questionPosition" name="position" min="1" :max="totalNumberOfQuestion + 1" placeholder="Position" :value="question.position" required>
        </div>
        <div class="form-group">
          <label for="questionTitle">Titre</label>
          <input type="text" class="form-control" id="questionTitle" name="title" placeholder="Titre" :value="question.title" required>
        </div>
        <div class="form-group">
          <label for="questionText">Text</label>
          <input type="text" class="form-control" id="questionText" name="text" placeholder="Text" :value="question.text" required>
        </div>
        <div class="form-group">
          <label for="questionText">Image</label>
          <ImageUpload @file-change="imageFileChangedHandler" />
        </div>
        <div class="form-group">
          <label for="questionText">Les réponses</label>
          <table class="table table-secondary">
            <thead>
              <tr>
                <th>Bonne réponse</th>
                <th>Réponses</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="possibleAnswer in question.possibleAnswers" :key="possibleAnswer.text">
                <td><input class="form-check-input" type="radio" name="questionIsCorrect" :checked="possibleAnswer.isCorrect" required></td>
                <td><input type="text" class="form-control" placeholder="Text" :value="possibleAnswer.text" required></td>
              </tr>
            </tbody>
          </table>
        </div>
        <button class="btn btn-primary btn-secondary-custom" @click="this.$router.push('/admin')" disableValidation="true">Annuler</button>
        <button class="btn btn-secondary btn-primary-custom">Sauvegarder</button>
      </form>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/quizApiService";
import generalStorageService from "@/services/GeneralStorageService";
import ImageUpload from "@/components/ImageUpload.vue";

export default {
  name: "QuestionEdition",
  data() {
    return {
      position: Number(this.$route.params.position),
      question: {
        position: 1,
        title: '',
        image: '',
        text: '',
        possibleAnswers: [
          { text: '', isCorrect: true },
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
          { text: '', isCorrect: false }
        ]
      },
      token: '',
      totalNumberOfQuestion: 1
    };
  },
  components: {
    ImageUpload
  },
  async created() {
    // Récuprer le token
    this.token = generalStorageService.getToken();

    await this.loadQuestionByPosition();
    this.totalNumberOfQuestion = Number(await generalStorageService.getNumberOfQuestion());
    
  },
  methods: {
    async loadQuestionByPosition() {
      if(this.position) {
        const res = await quizApiService.getQuestion(this.position);

        const newQuestion = res.data

        this.question = {
          position: newQuestion.position,
          title: newQuestion.title,
          image : newQuestion.image,
          text : newQuestion.text,
          possibleAnswers : newQuestion.possibleAnswers
        }
      }
      
    },
    imageFileChangedHandler(b64String) {
      this.question.image = b64String;
    }
  }
};
</script>

<style scoped>

.page {
  padding: 20px;
}

.question-edition-card {
  padding: 30px;
}

.question-edition-card label {
  font-size: 15px;
  font-weight: 500;
}

.form-group {
  margin-top: 15px;
}

</style>