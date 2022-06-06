<template>
  <div class="page">
    <div class="card question-edition-card">
      <h2 v-if="position">Mettre à jour une question</h2>
      <h2 v-else>Créer une question</h2>
      <form action="#" onsubmit="return false">
        <div class="form-group">
          <label for="questionPosition">Position</label>
          <input type="number" class="form-control" id="questionPosition" min="1" :max="totalNumberOfQuestion + 1" placeholder="Position" v-model="question.position" required>
        </div>
        <div class="form-group">
          <label for="questionTitle">Titre</label>
          <input type="text" class="form-control" id="questionTitle" placeholder="Titre" v-model="question.title" required>
        </div>
        <div class="form-group">
          <label for="questionText">Texte</label>
          <input type="text" class="form-control" id="questionText" placeholder="Texte" v-model="question.text" required>
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
              <tr v-for="(possibleAnswer, index) in question.possibleAnswers" :key="index">
                <td><input class="form-check-input" type="radio" name="questionIsCorrect" :value="index" v-model="checkedIndex" required></td>
                <td><input type="text" class="form-control" placeholder="Text" v-model="possibleAnswer.text" required></td>
              </tr>
            </tbody>
          </table>
        </div>
        <button class="btn btn-secondary btn-custom" @click="this.$router.push('/admin')" disableValidation="true">Annuler</button>
        <button class="btn btn-primary btn-custom" @click="saveQuestion">Sauvegarder</button>
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
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
          { text: '', isCorrect: false }
        ]
      },
      token: '',
      totalNumberOfQuestion: 1,
      checkedIndex: null
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

        // Set the index of answer to check
        this.checkedIndex = newQuestion.numCorrect-1;
      }
      
    },
    imageFileChangedHandler(b64String) {
      this.question.image = b64String;
    },
    saveQuestion() {
      // Set the correct answer to true and others to false
      for(let i = 0; i < 4; i++) {
        this.question.possibleAnswers[i].isCorrect = i === this.checkedIndex;
      }

      // Check if update a question or add a new question
      if(this.position) {
        quizApiService.updateQuestion(this.position,this.question, this.token);
      } else {
        quizApiService.addQuestion(this.question, this.token);
      }
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