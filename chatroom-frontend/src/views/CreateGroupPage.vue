<script setup>
import { useGlobalStore } from '@/stores/global'
import { useToastStore } from '@/stores/toast'
import { storeToRefs } from 'pinia'

const globalStore = useGlobalStore()
const { openCreateGroupChat, friendsList } = storeToRefs(globalStore)
const { CreateGruopChat } = globalStore

const tostStore = useToastStore()
const { CreateGruopChatToast } = tostStore

const HandleCloseGroup = () => {
  openCreateGroupChat.value.open = false
  openCreateGroupChat.value.name = null
  openCreateGroupChat.value.users = []
}

const HandleCreateGruopChat = () => {
  if (openCreateGroupChat.value.name === null || openCreateGroupChat.value.name.length <= 0) {
    CreateGruopChatToast()
    return
  }
  CreateGruopChat(openCreateGroupChat.value.name, openCreateGroupChat.value.users)
  HandleCloseGroup()
}
</script>

<template>
  <div class="create-group-page">
    <div class="title">
      <h1>創建聊天室</h1>
      <div class="close-btn" @click="HandleCloseGroup">
        <c-svg name="XCircle" w="30" h="30" />
      </div>
    </div>
    <div class="gruop-name">
      <input
        type="text"
        placeholder="輸入群組名稱 限50字"
        v-model="openCreateGroupChat.name"
        maxlength="50"
      />
    </div>
    <div class="select-users-list">
      <div class="select-user" v-for="friend in friendsList" :key="friend.id">
        <label :for="`select-friend-${friend.id}`">
          <div class="avatar">
            <img :src="friend.avatar" alt="用戶頭像" />
          </div>
          <div class="name">{{ friend.username }}</div>
          <input
            type="checkbox"
            :id="`select-friend-${friend.id}`"
            :name="`select-friend-${friend.id}`"
            :value="{ id: friend.id, username: friend.username }"
            v-model="openCreateGroupChat.users"
          />
          <span class="checkmark"></span>
        </label>
      </div>
    </div>

    <div class="btns">
      <button class="submit-btn" @click="HandleCreateGruopChat">創建</button>
      <button class="close-btn" @click="HandleCloseGroup">取消</button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#app.dark {
  .create-group-page {
    color: var(--dark-mod-text-color);

    .gruop-name {
      input {
        color: var(--dark-mod-text-color);
      }
    }
  }
}

.create-group-page {
  position: absolute;
  top: 30%;
  display: flex;
  flex-direction: column;
  background-color: rgba(0, 0, 0, 0.2);
  width: 300px;
  height: 500px;
  border: 1px solid black;
  border-radius: 10px;
  backdrop-filter: blur(20px);
  transition: color 0.5s;

  .title {
    display: flex;
    align-items: center;
    justify-content: space-between;

    h1 {
      margin-left: 70px;
    }

    .close-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 5px;
      cursor: pointer;
    }
  }

  .gruop-name {
    display: flex;
    justify-content: center;
    border-bottom: 1px solid black;
    gap: 20px;
    width: 100%;
    height: auto;
    transition: background-color 0.5s;

    input {
      background-color: transparent;
      text-align: center;
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

  .select-users-list {
    display: flex;
    flex-direction: column;
    padding: 20px;
    gap: 10px;
    height: 100%;
    overflow-y: auto;
    user-select: none;

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

    .select-user {
      display: flex;
      align-items: center;
      justify-content: flex-start;

      label {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 10px;
        gap: 20px;
        font-size: 1.5rem;
        cursor: pointer;

        .avatar {
          width: 35px;
          height: 35px;
          border-radius: 50%;
          object-fit: cover;
          background-color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: background-color 0.5s;
          img {
            border-radius: 50%;
            width: inherit;
            height: inherit;
          }
        }

        .name {
          display: inline-block;
          text-overflow: ellipsis;
          overflow: hidden;
          white-space: nowrap;
          width: 150px;
        }

        .checkmark {
          left: 100%;
        }
      }
    }
  }

  .btns {
    display: flex;
    align-items: center;
    justify-content: center;
    .submit-btn,
    .close-btn {
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
