<script setup>
import { computed } from 'vue'
import { useToastStore } from '@/stores/toast'

import { storeToRefs } from 'pinia'
import { useGlobalStore } from '@/stores/global'

const globalStore = useGlobalStore()
const { sentList, allUsers, friendsList, requestList, blockedList } = storeToRefs(globalStore)
const { SendFriendRequest, RejectRequest } = globalStore

const toast = useToastStore()
const { PostRequestToast } = toast

const UserStatusData = computed(() => {
  return allUsers.value.map((user) => {
    const existRequest = Array.isArray(requestList.value)
      ? requestList.value.find((req) => req.sender && req.sender.id === user.id)
      : null

    const request = Array.isArray(sentList.value)
      ? sentList.value.find((req) => req.receiver && req.receiver.id === user.id)
      : null

    return {
      user,
      request: request ? request : null,
      existRequest: existRequest ? existRequest : null,
      isFriend: friendsList.value.some((friend) => friend.id === user.id),
      isBlocked: blockedList.value.some((block) => block.id === user.id)
    }
  })
})

const HandleCancelFriendRequest = (request) => {
  RejectRequest(request)
}

const HandleSendFriendRequest = (userId) => {
  PostRequestToast(() => SendFriendRequest(userId))
}
</script>

<template>
  <div class="item" v-for="data in UserStatusData" :key="data.user.id">
    <div class="avatar">
      <img :src="data.user.avatar" alt="用戶頭像" />
    </div>
    <div class="texts">
      <span>{{ data.user.username }}</span>
      <p>{{ data.user.profile }}</p>
    </div>

    <template v-if="data.isFriend">
      <div class="btn friend">
        <c-svg name="IsFriend" />
      </div>
    </template>

    <template v-else-if="data.existRequest">
      <div class="btn notify">
        <span class="tooltips">收到邀請</span>
        <c-svg name="Circle1" />
      </div>
    </template>

    <template v-else-if="data.isBlocked">
      <div class="btn is-blocked">
        <span class="tooltips">已封鎖</span>
        <c-svg name="Exlcamation" />
      </div>
    </template>

    <template v-else-if="data.request">
      <div class="btn wait">
        <span class="tooltips">已寄送邀請</span>
        <c-svg name="Wait" />
      </div>
      <div class="btn cancel" @click="HandleCancelFriendRequest(data.request)">
        <span class="tooltips">取消請求</span>
        <c-svg name="XCircle" />
      </div>
    </template>

    <template v-else>
      <div class="btn" @click="HandleSendFriendRequest(data.user.id)">
        <span class="tooltips">寄送邀請</span>
        <c-svg name="Plus" />
      </div>
    </template>
  </div>
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

  .btn {
    margin-left: auto;
    cursor: pointer;
    &.notify,
    &.friend {
      color: rgb(0, 255, 0);
      cursor: default;
    }
    &.wait {
      color: yellow;
      cursor: default;
    }
    &.cancel,
    &.is-blocked {
      color: red;
    }
    &:hover .tooltips {
      visibility: visible;
      opacity: 1;
    }
  }
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
