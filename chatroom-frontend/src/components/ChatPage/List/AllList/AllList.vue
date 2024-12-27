<script setup>
import { computed, defineAsyncComponent, ref } from 'vue'
import { useGlobalStore } from '@/stores/global'
import { storeToRefs } from 'pinia'
import AllChatRoom from './item/AllChatRoom.vue'

const AllUsers = defineAsyncComponent(() => import('./item/AllUsers.vue'))
const FriendsList = defineAsyncComponent(() => import('./item/FriendsList.vue'))
const Inbox = defineAsyncComponent(() => import('./item/Inbox.vue'))
const BlockedList = defineAsyncComponent(() => import('./item/BlockedList.vue'))

const props = defineProps({
  titleIndex: {
    type: Number
  }
})

const filterList = ref('')

const titleName = computed(() => {
  switch (props.titleIndex) {
    case 0:
      return '聊天室'
    case 1:
      return '好友'
    case 2:
      return '全部用戶'
    case 3:
      return '收件匣'
    case 4:
      return '黑名單'
    default:
      return ''
  }
})

const globalStore = useGlobalStore()
const { openCreateGroupChat } = storeToRefs(globalStore)

const HandleCreateGroupRoom = () => {
  openCreateGroupChat.value.open = true
}
</script>

<template>
  <div class="all-list">
    <div class="search">
      <div class="search-bar">
        <input
          type="text"
          placeholder="搜尋"
          id="search-name"
          name="search-name"
          v-model="filterList"
        />
        <c-svg name="Search" />
      </div>
    </div>

    <div class="items">
      <div class="title">
        <h2>{{ titleName }}</h2>
        <div class="create-group-chat" v-if="titleIndex == 0" @click="HandleCreateGroupRoom">
          <span class="tooltips" aria-label="創建群組">創建群組</span>
          <c-svg name="Plus" w="30" h="30" />
        </div>
      </div>

      <AllChatRoom v-if="titleIndex == 0" :filterList="filterList" />
      <FriendsList v-if="titleIndex == 1" :filterList="filterList" />
      <AllUsers v-if="titleIndex == 2" />
      <Inbox v-if="titleIndex == 3" />
      <BlockedList v-if="titleIndex == 4" :filterList="filterList" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
#app.dark {
  .search {
    color: var(--dark-mod-text-color);
    .list-btn {
      background-color: rgba(17, 25, 40, 0.5);
      .list-content {
        color: black;
      }
    }
    .search-bar {
      background-color: rgba(17, 25, 40, 0.5);
    }
  }
  .items {
    &::-webkit-scrollbar-thumb {
      background-color: rgba(0, 0, 0, 0.4);
    }
  }
}
.all-list {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.search {
  display: flex;
  align-items: center;
  transition: color 0.5s;
  padding: 20px;

  .list-btn {
    display: flex;
    padding: 10px;
    background-color: rgba(87, 90, 96, 0.3);
    transition: background-color 0.5s;
    border-radius: 10px;
    cursor: pointer;

    .list-content {
      z-index: 1;
      top: 120%;
      left: 0;
      width: 120px;
      height: auto;
      position: absolute;
      border-radius: 10px;
      transition: background-color 0.3s;
      background-color: white;
      overflow: hidden;
      opacity: 0;
      visibility: hidden;
      transition: opacity 0.25s;
      &.show {
        opacity: 1;
        visibility: visible;
      }
      li {
        display: flex;
        justify-content: center;
        align-items: center;
        list-style: none;
        width: 100%;
        height: 30px;
        cursor: pointer;
        &:not(:last-child) {
          border-bottom: 1px solid black;
        }
        &:hover {
          background-color: rgb(220, 220, 220);
        }
      }
    }
  }

  .search-bar {
    display: flex;
    align-items: center;
    background-color: rgba(87, 90, 96, 0.3);
    border-radius: 10px;
    gap: 20px;
    width: 100%;
    padding: 5px;
    flex: 1;
    transition: background-color 0.5s;

    input {
      color: var(--dark-mod-text-color);
      background-color: transparent;
      outline: none;
      padding: 10px;
      font-size: 1.2rem;
      width: 100%;
      border: 0;
      transition: color 0.5s;
      &::placeholder {
        color: var(--dark-mod-text-color);
      }
    }
  }
}

.items {
  display: flex;
  flex-direction: column;
  flex: 1;
  width: 100%;
  overflow-y: scroll;
  &::-webkit-scrollbar {
    width: 0;
  }

  .title {
    display: flex;
    h2 {
      padding: 0 20px;
    }
    .create-group-chat {
      display: flex;
      align-items: center;
      justify-content: center;
      margin-left: auto;
      margin-right: 20px;
      cursor: pointer;

      &:hover .tooltips {
        transform: translateX(-90%);
        visibility: visible;
        opacity: 1;
      }
    }
  }
}

@media screen and (max-width: 420px) {
  .search {
    padding: 10px;
    .search-bar {
      gap: 0px;
    }
  }
}
</style>
