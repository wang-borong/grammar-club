<template>
  <div v-if="wrong" class="quote_wrong">
    <slot />
  </div>
  <div v-else class="quote_right">
    <slot />
  </div>
</template>

<script>
export default {
  props: {
    wrong: Boolean
  }
};
</script>

<style lang="scss">
.quote_right {
  background: #d0f0e0;
}
.quote_wrong {
  background: #eedada;
}
</style>
