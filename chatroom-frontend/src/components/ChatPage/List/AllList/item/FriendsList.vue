<script setup>
import { useGlobalStore } from '@/stores/global'
import { storeToRefs } from 'pinia'
import { computed } from 'vue'

const globalStore = useGlobalStore()
const { friendsList, openChatRoom, openInfo, userInfo, openList } = storeToRefs(globalStore)
const { GetOrCreatePersonalRoom } = globalStore

const props = defineProps(['filterList'])

const HandleOpenChat = async (userId) => {
  const room = await GetOrCreatePersonalRoom(userId)

  if (openChatRoom.value.open === false) {
    openChatRoom.value.open = true
  }
  openChatRoom.value.data = room
  openList.value = false
}

const OpenInfo = (user) => {
  userInfo.value = user
  openInfo.value = true
}

const FriendsListData = computed(() => {
  const clearFilter = props.filterList.replace(/\s+/g, ' ').trim().toUpperCase()
  if (clearFilter) {
    return friendsList.value.filter((friend) => {
      return friend.username.toUpperCase().includes(clearFilter)
    })
  } else {
    return friendsList.value
  }
})
</script>

<template>
  <template v-if="Array.isArray(FriendsListData) && FriendsListData.length !== 0">
    <div class="item" v-for="user in FriendsListData" :key="user.id">
      <div class="avatar" @click="OpenInfo(user)">
        <img :src="user.avatar" alt="用戶頭像" />
      </div>
      <div class="texts" @click="OpenInfo(user)">
        <span>{{ user.username }}</span>
        <p>{{ user.profile }}</p>
      </div>
      <div class="is-block" v-if="user.AmIBlocked">
        <span class="tooltips">用戶已將你封鎖</span>
        <c-svg name="Exlcamation" />
      </div>
      <div class="chat" @click="HandleOpenChat(user.id)">
        <span class="tooltips">聊天</span>
        <c-svg name="Chat" />
      </div>
    </div>
  </template>
  <template v-else>
    <h2 class="msg">無好友名單</h2>
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
    border 0.5s;

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
    cursor: pointer;
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
    cursor: pointer;
    span,
    p {
      display: inline-block;
      text-overflow: ellipsis;
      overflow: hidden;
      white-space: nowrap;
      max-width: 200px;
    }
    span {
      font-weight: bold;
    }
    p {
      font-size: 1rem;
      font-weight: 300;
    }
  }

  .chat {
    margin-left: auto;
    cursor: pointer;
    &:hover .tooltips {
      visibility: visible;
      opacity: 1;
    }
  }

  .is-block {
    color: red;
    &:hover .tooltips {
      visibility: visible;
      opacity: 1;
    }
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
