<script setup>
import { onMounted, onBeforeMount } from 'vue'
import { useUserStore } from '@/stores/user'
import { useGlobalStore } from '@/stores/global'
import ListComponent from '@/components/ChatPage/List/ListComponent.vue'
import ChatComponent from '@/components/ChatPage/Chat/ChatComponent.vue'

const userStore = useUserStore()
const { InitStore } = userStore

const globalStore = useGlobalStore()
const { ConnectWebsocket } = globalStore

onBeforeMount(() => {
  InitStore()
})

onMounted(() => {
  ConnectWebsocket()
})
</script>

<template>
  <div class="chat-page">
    <ListComponent />
    <ChatComponent />
  </div>
</template>

<style lang="scss" scoped>
.chat-page {
  display: flex;
  width: 100%;
  height: 100%;
  overflow-y: auto;
}
</style>
