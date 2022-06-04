<template>
  <div class="page">
    <div class="question-display">
      <div class="question-display-head">
        <h6 class="question-title">Question : {{ currentQuestionPosition }}/{{ totalNumberOfQuestion }} - {{ question.title }}</h6>
      </div>
      <img class="question-display-image" v-if="question.image" :src="question.image"/>
      <div class="question-display-body">
        <div class="question-text">{{ question.text }}</div>
        <div v-if="question" class="container-fluid">
          <div class="row row-cols-2">
            <div class="col-12 col-sm-12 col-md-6" v-for="(answer, index) in question.possibleAnswers" :key="answer.text" >
              <button  class="btn btn-outline-primary answer-btn" @click="$emit('answer-selected', index+1)">{{ answer.text }}</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionDisplay",
  emits: ['answer-selected'],
  data() {
    return {
    };
  },
  async created() {
  },
  props: {
    currentQuestionPosition: {
      type: Number
    },
    totalNumberOfQuestion: {
      type: Number
    },
    question: {
      type: Object
    }
  }
};
</script>

<style>
@import '@/assets/base.css';


.answer-btn {
  background-color: var(--color-background-soft) !important;
  border: 2px solid var(--color-border);
  min-width: 200px;
  height: 80px;
  width: 100%;
  font-weight: 500;
  color: var(--color-text);
  margin: 5px 0px 5px 0px;
}

.answer-btn:hover, .answer-btn:focus, .answer-btn:active {
  background-color: var(--primary-color) !important;
  border: none;
  color: white;
}

.answer-row {
  padding: 5px 0px 5px 0px;
}

.question-display {
  height: 100%;
  display: flex;
  flex-flow: column;
  justify-content: space-between;
  align-items: center;
  align-content: stretch;
  text-align: center;
  padding: 20px 0px;
}

.question-display-head {
  width: 100%;
}

.question-title {
  display: inline-block;
}

.question-display-body {
  width: 100%;
}

.question-display-image {
    max-width: 90%;
    max-height: calc(100% - 240px);
  }

.question-text {
  font-size: 30px;
}

@media (max-width: 576px) {
  .question-display-image {
    max-height: 270px;
  }

  .question-title {
    font-size: 14px;
  }

  .answer-btn {
    height: 50px;
    font-size: 12px;
  }

  .question-text {
    font-size: 16px;
  }
}



</style>