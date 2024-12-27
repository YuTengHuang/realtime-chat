<script setup>
import { useGlobalStore } from '@/stores/global'
import { useToastStore } from '@/stores/toast'
import { storeToRefs } from 'pinia'
import { computed } from 'vue'

const tostStore = useToastStore()
const { UnblockUserToast } = tostStore

const globalStore = useGlobalStore()
const { blockedList } = storeToRefs(globalStore)
const { UnblockFriend } = globalStore

const props = defineProps(['filterList'])

const HandleUnBlockedFriend = (id) => {
  UnblockUserToast(() => UnblockFriend(id))
}

const BlockedData = computed(() => {
  const clearFilter = props.filterList.replace(/\s+/g, ' ').trim().toUpperCase()
  if (clearFilter) {
    return blockedList.value.filter((friend) => {
      return friend.username.toUpperCase().includes(clearFilter)
    })
  } else {
    return blockedList.value
  }
})
</script>

<template>
  <template v-if="Array.isArray(BlockedData) && BlockedData.length !== 0">
    <div class="item" v-for="user in BlockedData" :key="user.id">
      <div class="avatar">
        <img :src="user.avatar" alt="用戶頭像" />
      </div>
      <div class="texts">
        <span>{{ user.username }}</span>
        <p>{{ user.profile }}</p>
      </div>
      <div class="cancel-btn" @click="HandleUnBlockedFriend(user.id)">
        <div class="tooltips">解除封鎖</div>
        <c-svg name="XCircle" />
      </div>
    </div>
  </template>

  <template v-else>
    <h2 class="msg">無黑名單用戶</h2>
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
  .cancel-btn {
    margin-left: auto;
    color: red;
    cursor: pointer;

    &:hover .tooltips {
      opacity: 1;
      visibility: visible;
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
