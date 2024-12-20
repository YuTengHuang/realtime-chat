<script setup>
import { useGlobalStore } from '@/stores/global'
import { storeToRefs } from 'pinia'

const globalStore = useGlobalStore()
const { openChatRoom, openInfo, userInfo, groupInfo, openList } = storeToRefs(globalStore)

const Prev = () => {
  openChatRoom.value.open = false
  openChatRoom.value.data = null
  openList.value = true
}

const HandleInfoClick = () => {
  if (openChatRoom.value.data.room_type === 'personal') {
    OpenInfo(openChatRoom.value.data.users.receiver)
  } else {
    GroupInfo(openChatRoom.value.data.users)
  }
}

const OpenInfo = (user) => {
  userInfo.value = user
  openInfo.value = true
}

const GroupInfo = (users) => {
  groupInfo.value = users
  openInfo.value = true
}
</script>

<template>
  <div class="top">
    <div class="prev" @click="Prev()">
      <c-svg name="Prev" w="30" h="30" />
    </div>
    <div class="user" v-if="openChatRoom && openChatRoom.data.room_type === 'personal'">
      <div class="avatar">
        <img :src="openChatRoom.data.users.receiver.avatar" alt="用戶頭像" />
      </div>
      <div class="texts">
        <span>{{ openChatRoom.data.users.receiver.username }}</span>
      </div>
    </div>
    <div class="user" v-else>
      <div class="avatar">
        <img
          src="https://vuedjangochats3.s3.ap-northeast-1.amazonaws.com/room_avatar/People.svg"
          alt="群組頭像"
        />
      </div>
      <div class="texts">
        <span>{{ openChatRoom.data.name }}</span>
      </div>
    </div>

    <div class="icons">
      <div class="info" @click="HandleInfoClick">
        <span class="tooltips">資訊</span>
        <c-svg name="Info" />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#app.dark {
  .top {
    color: var(--dark-mod-text-color);
    border-bottom: 1px solid #9b9b9b;
  }
}

.top {
  padding: 20px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #464646;
  transition:
    color 0.5s,
    border 0.5s;

  .prev {
    width: 30px;
    height: 30px;
    cursor: pointer;
  }

  .user {
    display: flex;
    align-items: center;
    margin-left: 10px;
    gap: 10px;
    .avatar {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 60px;
      height: 60px;
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
      display: flex;
      flex-direction: column;
      gap: 5px;
      span {
        display: inline-block;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
        max-width: 300px;
        font-size: 1.2rem;
        font-weight: bold;
      }
      p {
        font-size: 1rem;
        font-weight: 300;
      }
    }
  }

  .icons {
    display: flex;
    margin-left: auto;
    gap: 20px;

    .info {
      cursor: pointer;
      &:hover .tooltips {
        visibility: visible;
        opacity: 1;
      }
    }

    .tooltips {
      transform: translateY(80%) translateX(-25%);
    }
  }
}

@media screen and (max-width: 1200px) {
  .top {
    padding: 10px;
    .user {
      .texts {
        span {
          max-width: 180px;
        }
      }
    }
  }
}

@media screen and (max-width: 420px) {
  .top {
    padding: 10px;
    .user {
      .avatar {
        width: 40px;
        height: 40px;
      }
      .texts {
        span {
          max-width: 100px;
        }
      }
    }
  }
}
</style>
