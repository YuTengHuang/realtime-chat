<script setup>
import { computed, onMounted, ref, watch, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useGlobalStore } from '@/stores/global'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const { user } = storeToRefs(userStore)

const globalStore = useGlobalStore()
const { allMessage, openInfo, imgInfo, openChatRoom } = storeToRefs(globalStore)

const chat = ref(null)
const PreviewImg = (imgUrl) => {
  openInfo.value = true
  imgInfo.value = imgUrl
}

const CheckRoomTypeIsGroup = () => {
  return openChatRoom.value.data.room_type === 'group'
}

const MessageData = computed(() => {
  return allMessage.value.map((data) => {
    return data
  })
})

const scrollToBottom = () => {
  if (chat.value) {
    chat.value.scrollTop = chat.value.scrollHeight
  }
}

onMounted(() => {
  scrollToBottom()
})

watch(MessageData, async () => {
  await nextTick()
  scrollToBottom()
})
</script>

<template>
  <div class="center" ref="chat">
    <div
      :class="['message', { own: data.sender?.id === user.id, 'system-message': data.is_system }]"
      v-for="(data, index) in MessageData"
      :key="data.date + '-' + index"
    >
      <div class="avatar" v-if="data.sender?.id !== user.id && !data.is_system">
        <img :src="data.sender?.avatar" alt="用戶頭像" />
      </div>
      <div class="texts" v-if="!data.is_system">
        <div
          v-if="data.sender?.id !== user.id && !data.is_system && CheckRoomTypeIsGroup()"
          class="sender-name"
        >
          {{ data.sender?.username }}
        </div>
        <div class="img" v-if="data.img" @click="PreviewImg(data.img)">
          <img :src="data.img" alt="訊息圖片" />
        </div>
        <p v-if="data.content">{{ data.content }}</p>
        <span>{{ data.date }}</span>
      </div>
      <div class="texts" v-else>
        <p>{{ data.content }}</p>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#app.dark {
  .center {
    color: var(--dark-mod-text-color);
  }
}

.center {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
  transition: color 0.5s;
  &::-webkit-scrollbar {
    width: 5px;
  }

  &::-webkit-scrollbar-thumb {
    border-radius: 4px;
    background-color: rgba(0, 0, 0, 0.8);
    border: 1px solid slategrey;
  }

  &::-webkit-scrollbar-track {
    border-radius: 4px;
    box-shadow: transparent;
    background-color: #eee;
  }

  .message {
    max-width: 70%;
    display: flex;
    gap: 20px;

    .avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      object-fit: cover;
      background-color: white;
      transition: background-color 0.5s;
      img {
        border-radius: 50%;
        width: inherit;
        height: inherit;
      }
    }

    .texts {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 5px;
      color: var(--dark-mod-text-color);

      .sender-name {
        display: inline-block;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
        width: 100px;
      }

      p {
        align-self: flex-start;
        padding: 10px;
        background-color: rgba(17, 25, 40, 0.3);
        border-radius: 10px;
      }
      .img {
        width: 300px;
        height: 200px;
        border-radius: 10px;
        background-color: rgba(0, 0, 0, 0.3);
        cursor: pointer;
        img {
          width: 100%;
          height: 100%;
          object-fit: contain;
        }
      }
    }

    &.system-message {
      align-self: center;
      word-break: break-all;
      overflow-wrap: break-word;
      width: 200px;
      padding: 10px;
      p {
        border-radius: 30px;
      }
    }

    &.own {
      align-self: flex-end;
      .texts {
        p {
          align-self: flex-end;
          background-color: rgb(81, 130, 255);
        }
        span {
          text-align: end;
        }
        img {
          align-self: flex-end;
        }
      }
    }
  }
}

@media screen and (max-width: 500px) {
  .center {
    .message {
      .texts {
        .img {
          width: 200px;
          height: 200px;
        }
      }
    }
  }
}
</style>
