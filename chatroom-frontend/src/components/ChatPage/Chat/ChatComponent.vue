<script setup>
import { storeToRefs } from 'pinia'
import { useGlobalStore } from '@/stores/global'

import Top from '@/components/ChatPage/Chat/Top/Top.vue'
import Center from '@/components/ChatPage/Chat/Center/Center.vue'
import Bottom from '@/components/ChatPage/Chat/Bottom/Bottom.vue'
import Standby from '@/components/ChatPage/Chat/Standby/Standby.vue'

const globalStore = useGlobalStore()
const { openChatRoom } = storeToRefs(globalStore)
</script>
<template>
  <div class="chat" v-if="openChatRoom.open">
    <Top />
    <Center />
    <Bottom />
  </div>

  <div class="standby" v-else>
    <Standby />
  </div>
</template>

<style lang="scss" scoped>
#app.dark {
  .chat {
    border-left: 1px solid #9b9b9b;
  }
}

.chat {
  flex: 1;
  height: 100%;
  border-left: 1px solid #464646;
  transition: border 0.5s;
  display: flex;
  flex-direction: column;
}

.standby {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-left: 1px solid #464646;
  transition: border 0.5s;
}
</style>
>
