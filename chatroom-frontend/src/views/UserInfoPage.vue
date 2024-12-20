<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import { useGlobalStore } from '@/stores/global'
import { useToastStore } from '@/stores/toast'

const userStore = useUserStore()
const { user } = storeToRefs(userStore)

const globalStore = useGlobalStore()
const { openInfo, userInfo, friendsList, blockedList, sentList } = storeToRefs(globalStore)

const { BlockFriend, RemoveFriend, UnblockFriend, SendFriendRequest, RejectRequest } = globalStore

const tostStore = useToastStore()
const { BlockUserToast, UnfriendToast, UnblockUserToast, PostRequestToast } = tostStore

const emit = defineEmits(['closeInfo'])
const CloseInfo = () => {
  emit('closeInfo')
}

const IsMe = computed(() => {
  if (user.value.id && userInfo.value.id) {
    return userInfo.value.id === user.value.id
  }
  return false
})

const IsBlocked = computed(() => {
  if (Array.isArray(blockedList.value)) {
    return blockedList.value.some((item) => item.id === userInfo.value.id)
  }
  return null
})

const IsFriend = computed(() => {
  if (Array.isArray(friendsList.value)) {
    return friendsList.value.some((item) => item.id === userInfo.value.id)
  }
  return null
})

const Request = computed(() => {
  if (Array.isArray(sentList.value)) {
    return sentList.value.find((req) => req.receiver && req.receiver.id === userInfo.value.id)
  }
  return null
})

const HandleBlockOrUnblock = (userId) => {
  if (IsBlocked.value) {
    UnblockUserToast(() => UnblockFriend(userId))
  } else {
    BlockUserToast(() => BlockFriend(userId))
  }
  CloseInfo()
}

const HandleSendOrRemove = (userId) => {
  if (IsFriend.value) {
    UnfriendToast(() => RemoveFriend(userId))
  } else if (Request.value) {
    RejectRequest(Request.value)
  } else {
    PostRequestToast(() => SendFriendRequest(userId))
  }
  CloseInfo()
}

const HandleButtonText = () => {
  if (IsFriend.value) {
    return '刪除'
  } else if (Request.value) {
    return '取消邀請'
  } else {
    return '寄送邀請'
  }
}

const HandleButtonIcon = () => {
  if (IsFriend.value) {
    return 'Delete'
  } else if (Request.value) {
    return 'XCircle'
  } else {
    return 'Plus'
  }
}
</script>

<template>
  <div :class="['user-info', { show: openInfo }]">
    <div class="close-bar">
      <div class="close-info" @click="CloseInfo()">
        <c-svg name="XCircle" w="30" h="30" />
      </div>
    </div>
    <div class="info-avatar-bar">
      <div class="info-avatar">
        <img :src="userInfo.avatar" alt="用戶頭像" />
      </div>
    </div>
    <div class="info-texts">
      <h1>{{ userInfo.username }}</h1>
      <p>{{ userInfo.profile === 'null' ? '' : userInfo.profile }}</p>
    </div>
    <div class="btns" v-if="!IsMe">
      <button
        class="delete-btn"
        @click="HandleSendOrRemove(userInfo.id)"
        v-if="IsFriend || (!IsFriend && !IsBlocked)"
      >
        {{ HandleButtonText() }}
        <c-svg :name="HandleButtonIcon()" />
      </button>
      <button
        class="blocked-btn"
        @click="HandleBlockOrUnblock(userInfo.id)"
        v-if="IsFriend || IsBlocked"
      >
        {{ IsBlocked ? '取消封鎖' : '封鎖' }}
        <c-svg :name="IsBlocked ? 'XCircle' : 'Block'" />
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#app.dark {
  .user-info {
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

.user-info {
  visibility: hidden;
  opacity: 0;
  position: absolute;
  width: 300px;
  background-color: rgb(192, 192, 192);
  border: 1px solid black;
  display: flex;
  flex-direction: column;
  z-index: 3;
  gap: 20px;
  border-radius: 10px;
  transition:
    background-color 0.5s,
    border 0.5s;

  &.show {
    visibility: visible;
    opacity: 1;
  }

  .info-avatar-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    .info-avatar {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100px;
      height: 100px;
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
    word-break: break-all;
    overflow-wrap: break-word;
    h1,
    p {
      padding: 10px 20px;
      margin: 0;
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
