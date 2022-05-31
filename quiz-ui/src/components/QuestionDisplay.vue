<template>
  <div>
    <p>{{ question.title }}</p> 
    <img v-if="question.image" :src="question.image" />
    <p>{{ question.text }}</p>
    <button v-for="(answer, index) in question.possibleAnswers" :key="answer.text" @click="$emit('answer-selected', index)">{{ answer.text }}</button>
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
    console.log(this.question);
  },
  props: {
    question: {
      type: Object
    }
  }
};
</script>