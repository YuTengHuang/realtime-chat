<script setup>
import { defineAsyncComponent } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  w: {
    type: String,
    default: '24'
  },
  h: {
    type: String,
    default: '24'
  }
})

const icons = import.meta.glob('@/assets/svg/*.svg')
const icon = defineAsyncComponent(() => {
  const iconPath = `/src/assets/svg/${props.name}.svg`
  if (icons[iconPath]) {
    return icons[iconPath]()
  } else {
    return Promise.resolve(null)
  }
})
</script>

<template>
  <component :is="icon" :key="props.name" :width="w" :height="h" />
</template>
