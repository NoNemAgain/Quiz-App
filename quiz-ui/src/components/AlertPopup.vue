<template>
<div class="alert alert-danger alert-dismissible fade show" ref="alert-danger" role="alert">
  {{ errorMsg }}
  <button type="button" class="btn-close" @click="closeAlert"></button>
</div>
</template>

<script>
export default {
  name: "AlertPopup",
  emits: ['close-alert'],
  props: {
    errorMsg : {
      type: String
    }
  },
  methods: {
    closeAlert() {
      this.$refs['alert-danger'].style.display = 'none';
      this.$emit('close-alert');
    }
  }
};
</script>

<style>

.alert-danger {
  position: absolute;
  left: 0;
  right: 0;
  margin-left: auto;
  margin-right: auto;
  width: 80%;
  margin-top: 20px;
  z-index: 3;
}

</style>