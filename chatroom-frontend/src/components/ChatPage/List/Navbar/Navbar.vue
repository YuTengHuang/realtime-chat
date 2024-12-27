<script setup>
import router from '@/router'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import { useGlobalStore } from '@/stores/global'
import { useToastStore } from '@/stores/toast'
import { computed, ref } from 'vue'

const globalStore = useGlobalStore()
const { requestList, roomInviteList, openInfo, userInfo, totalMessageCount } =
  storeToRefs(globalStore)
const { CloseWebsocket } = globalStore

const userStore = useUserStore()
const { user } = storeToRefs(userStore)

const toastStore = useToastStore()
const { SuccessToast } = toastStore

const TotalInviteLength = computed(() => {
  return requestList.value.length + roomInviteList.value.length
})

const GoToUpdateUserInfo = () => {
  router.push('/update-user-info')
}

const OpenInfo = (user) => {
  userInfo.value = user
  openInfo.value = true
}

const activeIndex = ref(0)
const svgItem = ref([
  {
    name: 'Chat',
    chinese: '聊天室'
  },
  {
    name: 'IsFriend',
    chinese: '好友'
  },
  {
    name: 'People',
    chinese: '所有用戶'
  },
  {
    name: 'Email',
    chinese: '收件匣'
  },
  {
    name: 'Block',
    chinese: '黑名單'
  }
])
const emit = defineEmits(['ChangeItem'])
const EmitChange = (index) => {
  activeIndex.value = index
  emit('ChangeItem', index)
}

const LogOut = () => {
  userStore.RemoveToken()
  CloseWebsocket()
  SuccessToast('已登出')
  router.push({ name: 'auth' })
}
</script>

<template>
  <div class="navbar">
    <div class="update-user-info-btn" @click="GoToUpdateUserInfo">
      <c-svg name="ThreeDot" />
      <span class="tooltips" aria-label="更新個人資訊">更新資訊</span>
    </div>
    <div class="user">
      <div class="avatar" @click="OpenInfo(user)">
        <img :src="user.avatar" alt="用戶頭像" />
      </div>
      <span class="tooltips" aria-label="資訊">資訊</span>
    </div>
    <div class="btns">
      <div
        v-for="(item, index) in svgItem"
        :key="item.name"
        :class="[`btn btn-${item.name}`, { active: activeIndex === index }]"
        @click="EmitChange(index)"
      >
        <c-svg :name="item.name" w="30" h="30" />
        <div v-if="item.name === 'Email' && TotalInviteLength !== 0" class="notification">
          {{ TotalInviteLength > 99 ? '99+' : TotalInviteLength }}
        </div>
        <div v-if="item.name === 'Chat' && totalMessageCount !== 0" class="notification">
          {{ totalMessageCount > 99 ? '99+' : totalMessageCount }}
        </div>
        <span class="tooltips" :aria-label="item.chinese">{{ item.chinese }}</span>
      </div>
    </div>
    <div class="logout" @click="LogOut">
      <c-svg name="Logout" w="30" h="30" />
      <span class="tooltips" aria-label="登出">登出</span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#app.dark {
  .navbar {
    color: var(--dark-mod-text-color);
    border-right: 1px solid #9b9b9b;

    .btn:hover,
    .update-user-info-btn:hover,
    .logout:hover {
      background-color: rgba(0, 0, 0, 0.5);
    }

    .btn.active {
      border-left: 5px solid green;
      background-color: rgba(0, 0, 0, 0.5);
    }
  }
}

.tooltips {
  transform: translateY(-120%);
}

.update-user-info-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 100px;
  transition: background-color 0.2s;
  cursor: pointer;

  .tooltips {
    transform: translateY(0%) translateX(0%);
  }

  &:hover {
    background-color: rgb(255, 255, 255, 0.5);
  }

  &:hover .tooltips {
    visibility: visible;
    opacity: 1;
  }
}

.navbar {
  border-right: 1px solid #464646;
  gap: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition:
    color 0.5s,
    border 0.5s;

  .user {
    display: flex;
    align-items: center;
    gap: 20px;
    margin: auto;
    cursor: pointer;

    .tooltips {
      transform: translateY(-120%) translateX(20%);
    }

    &:hover .tooltips {
      visibility: visible;
      opacity: 1;
    }

    .avatar {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 50px;
      height: 50px;
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
  }

  .btns {
    display: flex;
    align-items: center;
    flex-direction: column;
    width: 100%;
    height: 100%;

    .btn {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 30px 0;
      width: 100%;
      transition:
        background-color 0.2s,
        border 0.2s;
      cursor: pointer;

      &.active {
        border-left: 5px solid rgba(0, 255, 0, 0.7);
        background-color: rgb(255, 255, 255, 0.5);
      }

      &:hover {
        background-color: rgb(255, 255, 255, 0.5);
      }

      &:hover .tooltips {
        visibility: visible;
        opacity: 1;
      }
    }

    .notification {
      display: flex;
      align-items: center;
      justify-content: center;
      position: absolute;
      top: 25%;
      left: 55%;
      font-size: 0.7rem;
      width: 20px;
      height: 20px;
      color: white;
      border-radius: 50%;
      background-color: red;
    }
  }

  .logout {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 30px 0;
    width: 100%;
    transition: background-color 0.2s;
    cursor: pointer;
    &:hover {
      background-color: rgb(255, 255, 255, 0.5);
    }

    &:hover .tooltips {
      visibility: visible;
      opacity: 1;
    }
  }
}

@media screen and (max-width: 420px) {
  .navbar {
    .update-user-info-btn {
      width: 65px;
    }
    .user {
      .avatar {
        width: 40px;
        height: 40px;
      }
    }
  }
}
</style>
