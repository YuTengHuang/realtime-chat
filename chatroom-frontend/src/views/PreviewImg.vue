<script setup>
import { storeToRefs } from 'pinia'
import { useGlobalStore } from '@/stores/global'

const globalStore = useGlobalStore()
const { openInfo, imgInfo } = storeToRefs(globalStore)

const emit = defineEmits(['closeImg'])
const CloseImg = () => {
  emit('closeImg')
}
</script>

<template>
  <div :class="['preview-img', { show: openInfo }]">
    <div class="preview-close-img" @click="CloseImg">
      <c-svg name="XCircle" />
    </div>
    <img :src="imgInfo" alt="預覽圖片" />
  </div>
</template>

<style lang="scss" scoped>
.preview-img {
  position: absolute;
  visibility: hidden;
  opacity: 0;
  z-index: 3;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  border-radius: 10px;
  width: auto;
  height: auto;
  background-color: black;

  .preview-close-img {
    display: flex;
    align-self: flex-end;
    justify-content: center;
    padding: 5px;
    width: auto;
    color: var(--dark-mod-text-color);
    cursor: pointer;
  }

  img {
    max-width: 1200px;
    max-height: 720px;
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  &.show {
    visibility: visible;
    opacity: 1;
  }
}

@media screen and (max-width: 1200px) {
  .preview-img {
    width: 90%;
  }
}
</style>
