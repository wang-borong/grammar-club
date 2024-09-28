<template>
  <span class="note_main">
    <u v-if="note"><slot /></u>
    <i v-else><slot /></i>

    <span v-if="note">
      <span>{{ note }}</span>
    </span>
  </span>
</template>

<script>
export default {
  props: {
    note: String
  }
};
</script>

<style lang="scss">
.note_main {
  display: inline-grid;
  text-align: center;
  text-indent: 0;
  line-height: 1.2;
}
</style>
