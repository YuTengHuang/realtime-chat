<script setup>
import router from '@/router'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { useGlobalStore } from '@/stores/global'
import { computed, onMounted, ref } from 'vue'

const userStore = useUserStore()
const { user } = storeToRefs(userStore)
const { InitStore } = userStore

const toastStore = useToastStore()
const { RemoveAvatarToast, LoadingToast, SuccessToast } = toastStore

const globalStore = useGlobalStore()
const { RemoveAvatar, UpdateUserInfo, ConnectWebsocket } = globalStore

const fields = ref([
  {
    name: 'email',
    title: '電子郵件',
    maxlength: 45,
    disabled: true
  },
  {
    name: 'username',
    title: '名稱',
    maxlength: 45,
    disabled: false
  },
  {
    name: 'profile',
    title: '簡介',
    maxlength: 50,
    disabled: false
  }
])
const imgData = ref({})
const inputData = ref({})
const originData = ref({})

const userData = computed(() => {
  return user.value
})

const Prev = () => {
  router.push({ name: 'chat' })
}

const CloseImg = () => {
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

const HandleUpdateUserInfo = () => {
  if (user.value.is_default === true) return
  if (
    originData.value.username === inputData.value.username &&
    originData.value.profile === inputData.value.profile &&
    !imgData.value.data
  ) {
    SuccessToast('請輸入變更資料!', 'warning')
    return
  }
  const data = {
    username: inputData.value.username,
    profile: inputData.value.profile,
    avatar: imgData.value || null
  }
  UpdateUserInfo(data)
  if (imgData.value.data) {
    LoadingToast('傳送圖片中...', '傳送速度取決於圖片大小及網路速度')
  }
  imgData.value = {}
}

const HandleRemoveAvatar = () => {
  if (user.value.is_default === 'true') return
  RemoveAvatarToast(() => RemoveAvatar())
}

function ProtectEmail(email) {
  if (email) {
    let localPart = email.split('@')[0]
    const domainLength = email.length - localPart.length
    if (localPart.length <= 2) {
      return '*'.repeat(localPart.length - 1) + email.slice(-domainLength)
    }
    const markPart = '*'.repeat(localPart.length - 2)
    return localPart[0] + markPart + localPart[localPart.length - 1] + email.slice(-domainLength)
  }
  return ''
}

onMounted(() => {
  InitStore()
  ConnectWebsocket()

  inputData.value = {
    email: ProtectEmail(user.value.email),
    username: user.value.username,
    profile: user.value.profile,
    IsDefault: user.value.is_default
  }
  originData.value = {
    username: user.value.username,
    profile: user.value.profile
  }

  if (inputData.value.IsDefault === 'true') {
    SuccessToast('預設用戶不可變更用戶資訊!', 'warning')
  }
})
</script>

<template>
  <div class="update-userInfo">
    <div class="top-bar">
      <div class="prev" @click="Prev">
        <c-svg name="Prev" w="30" h="30" />
      </div>
      <div class="text">
        <p>更新用戶資料</p>
      </div>
    </div>
    <div class="content">
      <form @submit.prevent="HandleUpdateUserInfo">
        <div :class="['field', field.name]" v-for="field in fields" :key="field.name">
          <label :for="field.name">{{ field.title }}</label>
          <div class="custom-input">
            <input
              type="text"
              :id="field.name"
              :disabled="field.disabled || inputData.IsDefault === 'true'"
              :maxlength="field.maxlength"
              v-model="inputData[field.name]"
              autocomplete="off"
            />
          </div>
        </div>
        <div class="field avatar">
          <div class="update-avatar">
            <h2>頭像</h2>
            <img :src="userData.avatar" alt="當前頭像" />
            <label
              :class="['img-file', { disabled: inputData.IsDefault === 'true' }]"
              for="img-file"
              >變更頭像</label
            >
            <input
              :disabled="inputData.IsDefault === 'true'"
              type="file"
              id="img-file"
              name="img-file"
              accept=".png, .jpg, .jpeg"
              @change="PreviewImg"
            />
            <p
              :class="['remove-avatar', { disabled: inputData.IsDefault === 'true' }]"
              @click="HandleRemoveAvatar"
              v-if="
                userData.avatar !== 'https://vuedjangochats3.s3.amazonaws.com/avatar/default.svg'
              "
            >
              移除頭像
            </p>
          </div>
          <div class="check-img">
            <p>預覽頭像</p>
            <div class="close-img" @click="CloseImg" v-if="imgData.data">
              <c-svg name="XCircle" w="30" h="30" />
              <span class="tooltips" aria-label="取消選取圖片">取消</span>
            </div>
            <img
              :src="'data:' + imgData.format + ';base64,' + imgData.data"
              alt="預覽更新頭像"
              v-if="imgData.data"
            />
          </div>
        </div>
        <div class="btns">
          <button type="submit" class="save-btn" :disabled="inputData.IsDefault === 'true'">
            儲存
          </button>
          <button type="button" @click="Prev" class="cancel-btn">取消</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#app.dark {
  .update-userInfo {
    color: var(--dark-mod-text-color);

    .update-avatar label {
      background-color: green;
    }
  }
}

.update-userInfo {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 100%;
  height: 100%;
  transition: color 0.5s;

  .top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid black;
    width: 100%;
    .prev {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      cursor: pointer;
      &:hover {
        background-color: rgb(255, 255, 255, 0.5);
      }
    }
    .text {
      flex: 1;
      text-align: center;
      font-size: 2.5rem;
      font-weight: bolder;
    }
  }

  .content {
    display: flex;
    justify-content: center;
    margin-top: 50px;
    width: 100%;
    height: 100%;
    overflow-y: auto;

    &::-webkit-scrollbar {
      width: 0;
    }

    form {
      width: 500px;
      height: 500px;
      padding: 20px;

      .field {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;

        & input:disabled {
          cursor: not-allowed;
        }

        label {
          display: flex;
          align-items: center;
          flex: 1;
          height: 100%;
          font-size: 1.5rem;
          font-weight: bolder;
        }

        .custom-input {
          display: flex;
          align-items: center;
          background-color: rgba(87, 90, 96, 0.3);
          border-radius: 10px;
          height: 50px;
          flex: 2;

          input[type='text'] {
            color: var(--dark-mod-text-color);
            padding: 0 10px;
            font-size: 1.2rem;
            width: 100%;
            border: 0;
            outline: none;
            background-color: transparent;
          }
        }

        .update-avatar {
          display: flex;
          flex-direction: column;
          width: 50%;
          gap: 20px;
          margin-bottom: 10px;

          img {
            background-color: white;
            border-radius: 50%;
            width: 100px;
            height: 100px;
          }

          .img-file {
            display: flex;
            justify-content: center;
            border: 1px solid black;
            border-radius: 10px;
            background-color: rgb(0, 164, 0);
            color: var(--dark-mod-text-color);
            padding: 10px;
            width: 70%;
            font-size: 1rem;
            transition:
              box-shadow 0.2s,
              background-color 0.2s;
            cursor: pointer;

            &:hover {
              background-color: green;
              box-shadow:
                (0 0 10px) rgb(0, 255, 0),
                (0 0 5px) black;
            }

            &.disabled {
              cursor: not-allowed;
              background-color: rgba(0, 0, 0, 0.5);
            }
          }

          .remove-avatar {
            text-align: center;
            width: 70%;
            border: 0;
            border-bottom: 0px solid black;
            font-size: 1.2rem;
            background-color: transparent;
            cursor: pointer;

            &.disabled {
              cursor: not-allowed;
            }

            &::after {
              content: '';
              position: absolute;
              bottom: -5px;
              left: 50%;
              transform: translateX(-50%);
              background-color: black;
              width: 0;
              height: 2px;
              transition:
                width 0.3s,
                background-color 0.3s;
            }

            &:hover::after {
              width: 70%;
            }
          }

          input[type='file'] {
            display: none;
          }
        }

        .check-img {
          display: flex;
          align-items: center;
          justify-content: center;
          background-color: rgba(87, 90, 96, 0.3);
          width: 100%;
          height: 200px;
          border-radius: 10px;

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
            z-index: 2;
            width: 100%;
            height: 100%;
            object-fit: contain;
            border-radius: 10px;
            background-color: rgba(87, 90, 96, 1);
          }

          p {
            font-size: 1.2rem;
            color: var(--dark-mod-text-color);
          }
        }
      }

      .btns {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;

        button {
          border: 0;
          width: 100%;
          padding: 5px;
          font-size: 1.5rem;
          border-radius: 10px;
          color: white;
          cursor: pointer;
        }
        .save-btn {
          background-color: rgb(220, 38, 38);
          transition: box-shadow 0.2s;

          &:hover {
            box-shadow:
              (0 0 10px) red,
              (0 0 5px) black;
          }

          &:disabled {
            cursor: not-allowed;
            background-color: rgba(0, 0, 0, 0.5);
          }
        }
        .cancel-btn {
          background-color: rgb(21, 128, 61);
          transition: box-shadow 0.2s;

          &:hover {
            box-shadow:
              (0 0 10px) green,
              (0 0 5px) black;
          }
        }
      }
    }
  }
}

@media screen and (max-width: 1200px) {
  .update-userInfo {
    .top-bar {
      .text {
        font-size: 1.7rem;
      }
    }
    .content {
      margin-top: 30px;
      margin-bottom: 20px;
      form {
        .field {
          display: block;
          .update-avatar {
            align-items: center;
            width: 100%;
          }
        }
      }
    }
  }
}
</style>
