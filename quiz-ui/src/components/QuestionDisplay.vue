<template>
  <div>
    <p>{{ question.title }}</p> 
    <img v-if="question.image" :src="question.image" />
    <p>{{ question.text }}</p>
    <div v-if="question" class="container-fluid">
      <div class="row row-cols-2">
        <div class="col-12 col-sm-12 col-md-6" v-for="(answer, index) in question.possibleAnswers" :key="answer.text" >
          <button  class="btn btn-outline-primary  answer-btn" @click="$emit('answer-selected', index+1)">{{ answer.text }}</button>
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
}

.answer-btn:hover, .answer-btn:focus, .answer-btn:active {
  background-color: var(--primary-color) !important;
  border: none;
  color: white;
}

.answer-row {
  padding: 5px 0px 5px 0px;
}

</style>