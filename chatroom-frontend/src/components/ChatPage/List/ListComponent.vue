<script setup>
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useGlobalStore } from '@/stores/global'
import AllList from './AllList/AllList.vue'
import Navbar from './Navbar/Navbar.vue'

const globalStore = useGlobalStore()
const { openList } = storeToRefs(globalStore)

const titleIndex = ref(0)
const ChangeItem = (index) => {
  titleIndex.value = index
}
</script>

<template>
  <div :class="['list', { 'show-list': openList }]">
    <Navbar @ChangeItem="ChangeItem" />
    <AllList :titleIndex="titleIndex" />
  </div>
</template>

<style lang="scss" scoped>
.list {
  display: flex;
}

@media screen and (max-width: 1200px) {
  #app.dark {
    .list {
      background-color: rgb(97, 97, 97);
    }
  }

  .list {
    position: absolute;
    top: 0;
    left: -150%;
    width: 100%;
    height: 100%;
    z-index: 5;
    background-color: rgb(128, 128, 128);
    transition:
      left 0.5s,
      background-color 0.5s;

    &.show-list {
      left: 0;
    }
  }
}
</style>
>
