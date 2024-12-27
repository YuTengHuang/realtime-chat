<script setup>
import { useGlobalStore } from '@/stores/global'
import { storeToRefs } from 'pinia'
import { computed } from 'vue'

const globalStore = useGlobalStore()
const { GetAllMessage } = globalStore
const { allRooms, openChatRoom, roomMessageCount, totalMessageCount, openList } =
  storeToRefs(globalStore)

const props = defineProps(['filterList'])

const HandleOpenChat = (room) => {
  if (openChatRoom.value.open === false) {
    openChatRoom.value.open = true
  }
  openChatRoom.value.data = room
  GetAllMessage(room.id)
  totalMessageCount.value -= roomMessageCount.value[room.id]
  roomMessageCount.value[room.id] = 0
  openList.value = false
}

const IncludesFilter = (data, filter) => {
  return data && data.toUpperCase().includes(filter)
}

const RoomsData = computed(() => {
  const clearFilter = props.filterList.replace(/\s+/g, ' ').trim().toUpperCase()
  if (clearFilter) {
    return allRooms.value.filter((room) => {
      return (
        IncludesFilter(room.name, clearFilter) ||
        (room.users?.receiver?.username &&
          IncludesFilter(room.users.receiver.username, clearFilter))
      )
    })
  } else {
    return allRooms.value
  }
})
</script>

<template>
  <template v-if="Array.isArray(RoomsData) && RoomsData.length !== 0">
    <div class="item" v-for="room in RoomsData" :key="room.id" @click="HandleOpenChat(room)">
      <template v-if="room.room_type === 'personal'">
        <div class="avatar">
          <img :src="room.users.receiver.avatar" alt="用戶頭像" />
        </div>
        <div class="texts">
          <span>{{ room.users.receiver.username }}</span>
        </div>
        <div class="message-count" v-if="roomMessageCount[room.id] > 0">
          {{ roomMessageCount[room.id] > 99 ? '99+' : roomMessageCount[room.id] }}
        </div>
      </template>
      <template v-else>
        <div class="avatar">
          <img
            class="avatar"
            src="https://vuedjangochats3.s3.ap-northeast-1.amazonaws.com/room_avatar/People.svg"
            alt="群組頭像"
          />
        </div>
        <div class="texts">
          <span>{{ room.name }}</span>
        </div>
        <div class="message-count" v-if="roomMessageCount[room.id] > 0">
          {{ roomMessageCount[room.id] > 99 ? '99+' : roomMessageCount[room.id] }}
        </div>
      </template>
    </div>
  </template>
  <template v-else>
    <h2 class="msg">無聊天列表</h2>
  </template>
</template>

<style lang="scss" scoped>
#app.dark {
  .item {
    color: var(--dark-mod-text-color);
    border-bottom: 1px solid #9b9b9b;
  }
}

.item {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  border-bottom: 1px solid #464646;
  color: black;
  transition:
    color 0.5s,
    border 0.5s,
    background-color 0.2s;
  cursor: pointer;

  &:hover {
    background-color: rgba(255, 255, 255, 0.2);
  }

  .avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
    background-color: white;
    transition: background-color 0.5s;
    display: flex;
    align-items: center;
    justify-content: center;
    img {
      border-radius: 50%;
      width: inherit;
      height: inherit;
    }
  }

  .texts {
    display: flex;
    flex-direction: column;
    gap: 10px;
    span {
      display: inline-block;
      text-overflow: ellipsis;
      overflow: hidden;
      white-space: nowrap;
      max-width: 200px;
      font-weight: bold;
    }
  }

  .message-count {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: auto;
    width: 22px;
    height: 22px;
    font-size: 0.9rem;
    border-radius: 50%;
    background-color: red;
    color: white;
  }
}
.msg {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

@media screen and (max-width: 420px) {
  .item {
    gap: 10px;
    padding: 10px;

    .avatar {
      width: 40px;
      height: 40px;
    }

    .texts {
      span {
        max-width: 130px;
      }
    }
  }
}
</style>
