<template>
  <div class="alert alert-danger fade show">
    <strong>Error!</strong> {{ errorMsg }}
  </div>
</template>

<script>
export default {
  name: "AlertPopup",
  props: {
    errorMsg : {
      type: String
    }
  }
};
</script>

<style>

.alert-danger {
  position: absolute;
}

</style>