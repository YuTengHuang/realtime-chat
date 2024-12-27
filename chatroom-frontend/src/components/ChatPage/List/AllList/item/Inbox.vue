<script setup>
import { storeToRefs } from 'pinia'
import { useGlobalStore } from '@/stores/global'
import { computed } from 'vue'

const globalStore = useGlobalStore()
const { requestList, roomInviteList } = storeToRefs(globalStore)
const { RejectRequest, AgreeRequest, AgreeInvite, RejectInvite } = globalStore

const RequestDatas = computed(() => {
  return requestList.value
})

const InviteDatas = computed(() => {
  return roomInviteList.value
})

const HandleAgreeRequest = (request) => {
  AgreeRequest(request)
}

const HandleRejectRequest = (request) => {
  RejectRequest(request)
}

const HandleAgreeInvite = (id) => {
  AgreeInvite(id)
}

const HandleRejectInvite = (id) => {
  RejectInvite(id)
}
</script>

<template>
  <div class="friend-request-item">
    <h3>好友邀請</h3>
    <template v-if="Array.isArray(RequestDatas) && RequestDatas.length !== 0">
      <div class="item" v-for="request in RequestDatas" :key="request.id">
        <div class="avatar">
          <img :src="request.sender.avatar" alt="用戶頭像" />
        </div>
        <div class="texts">
          <span>{{ request.sender.username }}</span>
          <p>{{ request.timestamp }}</p>
        </div>
        <div class="btns">
          <div class="btn agree" @click="HandleAgreeRequest(request)">
            <c-svg name="CheckCircle" w="30" h="30" />
          </div>
          <div class="btn reject" @click="HandleRejectRequest(request)">
            <c-svg name="XCircle" w="30" h="30" />
          </div>
        </div>
      </div>
    </template>
    <template v-else>
      <h2 class="msg">無好友請求</h2>
    </template>
  </div>

  <div class="room-invite-item">
    <h3>群組邀請</h3>
    <template v-if="Array.isArray(InviteDatas) && InviteDatas.length !== 0">
      <div class="item" v-for="invite in InviteDatas" :key="invite.id">
        <div class="texts">
          <span>{{ invite.sender }}</span>
          <span>邀請你進入群組</span>
          <span>{{ invite.room }}</span>
          <p>{{ invite.timestamp }}</p>
        </div>
        <div class="btns">
          <div class="btn agree" @click="HandleAgreeInvite(invite.id)">
            <c-svg name="CheckCircle" w="30" h="30" />
          </div>
          <div class="btn reject" @click="HandleRejectInvite(invite.id)">
            <c-svg name="XCircle" w="30" h="30" />
          </div>
        </div>
      </div>
    </template>
    <template v-else>
      <h2 class="msg">無群組邀請</h2>
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

.friend-request-item,
.room-invite-item {
  margin-top: 10px;
  height: 50%;
  overflow-y: auto;
  border-bottom: 1px solid #464646;
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
  h3 {
    text-align: center;
    margin-bottom: 10px;
  }

  .msg {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 90%;
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
  .btns {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: auto;
    gap: 20px;
    .btn {
      cursor: pointer;
      &.agree {
        color: rgb(0, 255, 0);
      }
      &.reject {
        color: rgb(255, 0, 0);
      }
    }
  }
}

@media screen and (max-width: 420px) {
  .item {
    gap: 10px;
    padding: 10px;
    .texts {
      span {
        max-width: 130px;
      }
    }
  }
}
</style>
