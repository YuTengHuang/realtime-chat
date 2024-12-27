<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import data from 'emoji-mart-vue-fast/data/all.json'
import 'emoji-mart-vue-fast/css/emoji-mart.css'
import { Picker, EmojiIndex } from 'emoji-mart-vue-fast/src'
import { storeToRefs } from 'pinia'
import { useGlobalStore } from '@/stores/global'
import { useToastStore } from '@/stores/toast'

const globalStore = useGlobalStore()
const { SendMessage } = globalStore
const { openChatRoom, friendsList } = storeToRefs(globalStore)

const toast = useToastStore()
const { LoadingToast } = toast

let emojiIndex = new EmojiIndex(data)
const openEmoji = ref(false)
const msg = ref('')
const imgData = ref({})

const target = computed(() => {
  return friendsList.value.find((item) => item.id === openChatRoom.value.data.users.receiver?.id)
})

const HandleSendClick = () => {
  if ((msg.value.length === 0 && !imgData.value.data) || (IsDisabled() && IsPersonal())) return
  msg.value = msg.value.replace(/\s+/g, ' ').trim()
  const data = {
    room: openChatRoom.value.data.id,
    message: msg.value,
    img: imgData.value
  }
  SendMessage(data)
  if (imgData.value.data) {
    LoadingToast('傳送圖片中...', '傳送速度取決於圖片大小及網路速度')
  }
  msg.value = ''
  imgData.value = {}
}

const PreviewImg = (e) => {
  const img = e.target.files[0]

  if (img) {
    const fr = new FileReader()
    fr.onload = function () {
      imgData.value = {
        format: fr.result.split(',')[0].split('/')[1].split(';')[0],
        data: fr.result.replace(/^data:.+;base64,/, '')
      }
    }
    fr.readAsDataURL(img)
  }
}

const IsDisabled = () => {
  return target.value?.AmIBlocked || target.value === undefined || !target.value?.IsFriend
}

const IsPersonal = () => {
  return openChatRoom.value.data.room_type === 'personal'
}

const CloseImg = () => {
  imgData.value = {}
}

const OnSelectEmoji = (emoji) => {
  msg.value += emoji.native
  openEmoji.value = false
}

const HandleClick = (e) => {
  const btn = document.querySelector('.emoji')
  const emojiList = document.querySelector('.emoji-list')

  if (emojiList.contains(e.target)) {
    openEmoji.value = true
  } else if (!btn.contains(e.target) && !emojiList.contains(e.target)) {
    openEmoji.value = false
  }
}

const HandleOpenEmoji = () => {
  if (IsDisabled() && IsPersonal()) return
  else openEmoji.value = !openEmoji.value
}

const PlaceHolderText = () => {
  if (IsPersonal()) {
    if (target.value?.AmIBlocked) {
      return '你已被封鎖!'
    } else if (target.value === undefined) {
      return '非好友不可傳送訊息!'
    } else if (!target.value?.IsFriend) {
      return '對方已將你移除好友'
    } else {
      return '輸入訊息...'
    }
  } else {
    return '輸入訊息...'
  }
}

onMounted(() => {
  window.addEventListener('click', HandleClick)
})

onBeforeUnmount(() => {
  window.removeEventListener('click', HandleClick)
})
</script>

<template>
  <div class="bottom">
    <div class="add-file">
      <input
        type="file"
        id="file"
        name="file"
        accept=".png, .jpg, .jpeg"
        @change="PreviewImg"
        :disabled="IsDisabled() && IsPersonal()"
      />
      <label for="file">
        <c-svg name="Plus" w="30" h="30" />
      </label>
    </div>
    <div class="msg-bar">
      <input
        type="text"
        id="message"
        name="message"
        :placeholder="PlaceHolderText()"
        v-model="msg"
        autocomplete="off"
        :disabled="IsDisabled() && IsPersonal()"
      />
      <div :class="['emoji', { disabled: IsDisabled() && IsPersonal() }]" @click="HandleOpenEmoji">
        <c-svg name="Emoji" />
        <Picker
          :data="emojiIndex"
          :class="['emoji-list', { show: openEmoji }]"
          set="twitter"
          :showSkinTones="false"
          @select="OnSelectEmoji"
        />
      </div>
    </div>
    <button
      class="send-btn"
      @click="HandleSendClick"
      :disabled="(msg.length === 0 && !imgData.data) || (IsDisabled() && IsPersonal())"
    >
      <c-svg name="Send" />
    </button>
    <div class="check-img" v-if="imgData.data">
      <div class="close-img" @click="CloseImg">
        <c-svg name="XCircle" w="30" h="30" />
        <span class="tooltips" aria-label="取消選取圖片">取消</span>
      </div>
      <img :src="'data:' + imgData.format + ';base64,' + imgData.data" alt="預覽圖片" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
#app.dark {
  .bottom {
    border-top: 1px solid #9b9b9b;
    color: var(--dark-mod-text-color);

    .msg-bar {
      background-color: rgba(17, 25, 40, 0.5);
    }

    .send-btn {
      color: inherit;
    }
  }
}

.check-img {
  position: absolute;
  left: 0;
  bottom: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  width: 300px;
  height: 200px;

  .close-img {
    position: absolute;
    top: 0;
    right: 0;
    z-index: 3;
    color: var(--dark-mod-text-color);
    cursor: pointer;
    &:hover .tooltips {
      visibility: visible;
      opacity: 1;
    }
  }

  img {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
}

.bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  border-top: 1px solid #464646;
  padding: 20px;
  gap: 20px;
  transition:
    color 0.5s,
    border 0.5s;

  .add-file {
    #file {
      display: none;
    }

    label {
      display: flex;
      width: 30px;
      height: 30px;
      cursor: pointer;
    }

    #file:disabled + label {
      cursor: not-allowed;
      opacity: 0.5;
    }
  }

  .msg-bar {
    flex: 1;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 30px;
    padding: 10px;
    gap: 20px;
    background-color: rgba(87, 90, 96, 0.3);
    transition: background-color 0.5s;

    input {
      color: var(--dark-mod-text-color);
      background-color: transparent;
      outline: none;
      padding-left: 10px;
      font-size: 1.2rem;
      width: 90%;
      border: 0;
      transition: color 0.5s;
      &::placeholder {
        color: var(--dark-mod-text-color);
      }
    }

    .emoji {
      cursor: pointer;

      &.disabled {
        cursor: not-allowed;
      }

      .emoji-list {
        visibility: hidden;
        position: absolute;
        width: 300px !important;
        transform: translateX(-90%) translateY(-110%);
        opacity: 0;
        &.show {
          visibility: visible;
          opacity: 1;
        }
      }
    }
  }

  .send-btn {
    width: 30px;
    height: 30px;
    background-color: transparent;
    transition: color 0.5s;
    border: 0;
    cursor: pointer;
  }
}

@media screen and (max-width: 420px) {
  .bottom {
    gap: 10px;
    padding: 10px;
    .msg-bar {
      gap: 10px;
    }
  }
}
</style>
