<script setup>
import { ref, onMounted, defineAsyncComponent } from 'vue'
import { storeToRefs } from 'pinia'
import { useGlobalStore } from '@/stores/global'
import { useUserStore } from './stores/user'
import { useToastStore } from '@/stores/toast'

const CreateGroupPage = defineAsyncComponent(() => import('./views/CreateGroupPage.vue'))
const UserInfoPage = defineAsyncComponent(() => import('./views/UserInfoPage.vue'))
const GroupInfoPage = defineAsyncComponent(() => import('./views/GroupInfoPage.vue'))
const PreviewImg = defineAsyncComponent(() => import('./views/PreviewImg.vue'))

const userStore = useUserStore()
const { user } = storeToRefs(userStore)

const globalStore = useGlobalStore()
const { openInfo, userInfo, groupInfo, imgInfo, openCreateGroupChat, openList } =
  storeToRefs(globalStore)

const toastStore = useToastStore()
const { AttentionToast } = toastStore

const isLight = ref(true)
const appElement = ref(null)
const IsLight = () => {
  isLight.value = !isLight.value
  if (appElement.value) {
    appElement.value.classList.toggle('dark', !isLight.value)
  }
}

const CloseInfo = () => {
  openInfo.value = false
  userInfo.value = null
  groupInfo.value = null
  imgInfo.value = null
}

const CloseImg = () => {
  openInfo.value = false
  imgInfo.value = null
}

const HandleOpenList = () => {
  openList.value = !openList.value
}

AttentionToast()

onMounted(() => {
  appElement.value = document.getElementById('app')
})
</script>

<template>
  <div class="tool-bar">
    <div class="navbar-list" @click="HandleOpenList" v-if="user.isAuth">
      <c-svg name="List" />
    </div>
    <div class="toggle-light" @click="IsLight">
      <div class="toggle-light-background">
        <c-svg name="LightOff" w="20" h="18" :class="['off', { toggle: !isLight }]" />
        <c-svg name="LightOn" w="20" h="18" :class="['on', { toggle: isLight }]" />
      </div>
      <button :class="['toggle-light-btn', { toggle: !isLight }]"></button>
    </div>
  </div>
  <div id="main">
    <RouterView />
  </div>

  <UserInfoPage v-if="userInfo" @closeInfo="CloseInfo" />
  <GroupInfoPage v-if="groupInfo" @closeInfo="CloseInfo" />
  <PreviewImg v-if="imgInfo" @closeImg="CloseImg" />
  <CreateGroupPage v-if="openCreateGroupChat.open" />
  <div class="overlay" v-if="openInfo" @click="CloseInfo" />
</template>
