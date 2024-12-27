<script setup>
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useGlobalStore } from '@/stores/global'
import { useToastStore } from '@/stores/toast'

const emit = defineEmits(['closeInfo'])
const CloseInfo = () => {
  emit('closeInfo')
}

const globalStore = useGlobalStore()
const { openInfo, groupInfo, friendsList, openChatRoom, openList } = storeToRefs(globalStore)

const { OuitChat, InviteJoinGruopChat } = globalStore

const tostStore = useToastStore()
const { QuitGroupChatToast } = tostStore

const showUsers = ref(true)
const IsUsers = () => {
  showUsers.value = true
}
const IsInvite = () => {
  showUsers.value = false
}

const InviteUsers = ref([])

const CanInviteUsersData = computed(() => {
  const data = friendsList.value.filter((friend) => {
    return !groupInfo.value.some((user) => user.id === friend.id)
  })

  return data
})

const HandleToggleBtn = () => {
  if (showUsers.value) {
    QuitGroupChatToast(() => {
      OuitChat(openChatRoom.value.data.id)
      openList.value = true
    })
    CloseInfo()
  } else {
    if (InviteUsers.value.length !== 0) {
      InviteJoinGruopChat(openChatRoom.value.data.id, InviteUsers.value)
      openInfo.value = false
      InviteUsers.value = []
    }
  }
}
</script>

<template>
  <div :class="['group-info', { show: openInfo }]">
    <div class="close-bar">
      <div class="close-info" @click="CloseInfo">
        <c-svg name="XCircle" w="30" h="30" />
      </div>
    </div>
    <div class="room-name">
      <p>{{ openChatRoom.data?.name }}</p>
    </div>
    <div class="change-page">
      <button :class="['users', { active: showUsers }]" @click="IsUsers">成員</button>
      <button :class="['invite-user', { active: !showUsers }]" @click="IsInvite">邀請</button>
    </div>
    <div class="user-list" v-if="showUsers">
      <div class="user" v-for="user in groupInfo" :key="user.id">
        <div class="info-avatar-bar">
          <div class="info-avatar">
            <img :src="user.avatar" alt="用戶頭像" />
          </div>
        </div>
        <div class="info-texts">
          <h3>{{ user.username }}</h3>
        </div>
      </div>
    </div>
    <div class="user-list invite" v-else>
      <template v-if="CanInviteUsersData.length > 0">
        <div class="user" v-for="user in CanInviteUsersData" :key="user.id">
          <label class="user-invite-info">
            <div class="info-avatar-bar">
              <div class="info-avatar">
                <img :src="user.avatar" alt="用戶頭像" />
              </div>
            </div>
            <div class="info-texts">
              <h3>{{ user.username }}</h3>
            </div>
            <input
              type="checkbox"
              :id="`select-friend-${user.id}`"
              :name="`select-friend-${user.id}`"
              :value="{ id: user.id, username: user.username }"
              v-model="InviteUsers"
            />
            <span class="checkmark"></span>
          </label>
        </div>
      </template>
      <template v-else>
        <h2 class="user">無好友可邀請!</h2>
      </template>
    </div>
    <div class="btns">
      <button class="delete-btn" @click="HandleToggleBtn">
        {{ showUsers ? '退出群組' : '送出邀請' }}
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#app.dark {
  .group-info {
    background-color: rgb(137, 137, 137);
    border: 1px solid var(--dark-mod-text-color);
    .info-avatar {
      img {
        border-radius: 50%;
        width: 100%;
        height: 100%;
      }
    }
  }
}

.group-info {
  position: absolute;
  visibility: hidden;
  opacity: 0;
  display: flex;
  flex-direction: column;
  width: 300px;
  background-color: rgb(192, 192, 192);
  border: 1px solid black;
  z-index: 3;
  gap: 10px;
  border-radius: 10px;
  transition:
    background-color 0.5s,
    border 0.5s;

  &.show {
    visibility: visible;
    opacity: 1;
  }

  .room-name {
    font-size: 1.5rem;
    font-weight: 700;
    padding: 0 10px;
    word-break: break-all;
    text-align: center;
  }

  .change-page {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;

    button {
      position: relative;
      background-color: transparent;
      padding: 10px;
      font-size: 1.2rem;
      border: 0;
      width: 40%;
      cursor: pointer;
      transition:
        transform 0.3s,
        text-shadow 0.3s,
        background-color 0.3s,
        border-radius 0.3s;

      &.active {
        background-color: rgb(106, 200, 255);
        border-radius: 30px;
      }

      &:hover {
        transform: scale(1.1);
        text-shadow: 1px 1px 5px white;
      }

      &::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        background: black;
        width: 0px;
        height: 2px;
        transition: width 0.3s;
      }
      &:hover::after {
        width: 100%;
      }
    }
  }

  .user-list {
    display: flex;
    flex-direction: column;
    height: 300px;
    overflow-y: auto;
    &::-webkit-scrollbar {
      width: 0;
    }

    .user {
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: row;
      padding: 10px;
      .info-avatar-bar {
        display: flex;
        align-items: center;
        justify-content: center;
        .info-avatar {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 40px;
          height: 40px;
          border-radius: 50%;
          object-fit: cover;
          background-color: white;
          transition: background-color 0.5s;
          img {
            border-radius: 50%;
            width: 100%;
            height: 100%;
          }
        }
      }

      .info-texts {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        word-wrap: break-word;
        overflow-wrap: break-word;
        h3 {
          vertical-align: middle;
          padding: 10px;
          margin: 0;
          display: inline-block;
          text-overflow: ellipsis;
          overflow: hidden;
          white-space: nowrap;
          width: 200px;
        }
      }
    }

    &.invite {
      .user-invite-info {
        display: flex;
      }
    }
  }

  .btns {
    display: flex;
    align-items: center;
    justify-content: center;
    .blocked-btn,
    .delete-btn {
      border: 0;
      gap: 5px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 10px;
      color: white;
      background-color: rgb(220, 38, 38);
      font-size: 1.5rem;
      padding: 5px;
      margin: 10px 10px 30px 10px;
      transition: box-shadow 0.2s;
      cursor: pointer;

      &:hover {
        box-shadow:
          (0 0 10px) red,
          (0 0 5px) black;
      }
    }
  }
}
</style>
