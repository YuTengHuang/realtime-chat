<script setup>
import router from '@/router'
import { ref } from 'vue'
import { LoginAxios } from '@/stores/api'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import Swal from 'sweetalert2'

const userStore = useUserStore()

const toastStore = useToastStore()
const { SuccessToast, CancelToast, LoadingToast } = toastStore

const checkPassword = ref(false)
const ToggleCheckPassword = () => {
  checkPassword.value = !checkPassword.value
}

const errorMsg = ref({
  email: '',
  password: ''
})

const InitUserDataForLogin = () => ({
  email: '',
  password: ''
})

const formData = ref(InitUserDataForLogin())

const CheckField = (key, msg) => {
  errorMsg.value[key] = formData.value[key].length === 0 ? `請輸入${msg}!` : ''
}

const CheckAllFields = () => {
  const invalidFields = Object.keys(formData.value).filter(
    (key) => formData.value[key].length === 0
  )
  return invalidFields.length === 0 ? null : invalidFields
}

const SubmitForm = async () => {
  const invalidFields = CheckAllFields()

  if (invalidFields) {
    CancelToast('未填寫的字段:', 'info', invalidFields.join(', '))
    return
  }

  try {
    LoadingToast('驗證中...', '等待驗證完成')
    const response = await LoginAxios('login/', formData.value)
    userStore.SetToken(response.user)
    formData.value = InitUserDataForLogin()
    router.push({ name: 'chat' })
    SuccessToast('登入成功')
  } catch (error) {
    Swal.close()
    const msg = error.detail || error.response?.data?.detail || '登入失敗，請稍後再試'
    CancelToast('登入失敗', 'error', msg)
    formData.value = InitUserDataForLogin()
  }
}

const selectData = ref('')
const accounts = ref([
  {
    email: 'default@default.com1',
    password: 'VeryLongPassWord'
  },
  {
    email: 'default@default.com2',
    password: 'MyPassWordIsPassWord'
  },
  {
    email: 'default@default.com3',
    password: 'HiIAmPassWord'
  },
  {
    email: 'default@default.com4',
    password: 'AnotherVeryLongPassWord'
  },
  {
    email: 'default@default.com5',
    password: 'PassWordLengthIs18'
  },
  {
    email: 'default@default.com6',
    password: 'DontUseBadPassWord'
  }
])

const UpDateFormData = () => {
  const selected = accounts.value.find((account) => account.email === selectData.value)
  if (selected) {
    formData.value.email = selected.email
    formData.value.password = selected.password
  } else {
    formData.value = InitUserDataForLogin()
  }
}
</script>

<template>
  <div class="login-page">
    <select
      name="choose-accounts"
      id="choose-accounts"
      @change="UpDateFormData"
      v-model="selectData"
    >
      <option value="" selected>選擇預設帳號</option>
      <option v-for="(account, index) in accounts" :key="`預設帳號${index}`" :value="account.email">
        預設{{ index + 1 }}
      </option>
    </select>

    <form @submit.prevent="SubmitForm">
      <h1>Welcome Back</h1>
      <input
        id="login-email"
        type="email"
        v-model="formData.email"
        placeholder="Email"
        autocomplete="off"
        @blur="CheckField('email', 'email')"
      />
      <span>{{ errorMsg.email }}</span>
      <div class="password-container">
        <input
          id="login-password"
          :type="checkPassword ? 'text' : 'password'"
          v-model="formData.password"
          placeholder="Password"
          autocomplete="off"
          @blur="CheckField('password', 'password')"
        />
        <i @click="ToggleCheckPassword">
          <c-svg name="NoCheckPassWord" :class="{ show: !checkPassword }" />
          <c-svg name="CheckPassWord" :class="{ show: checkPassword }" />
        </i>
      </div>
      <span>{{ errorMsg.password }}</span>
      <button>登入</button>
    </form>
  </div>
</template>

<style lang="scss" scoped>
#app.dark {
  form,
  input,
  button,
  select {
    color: var(--dark-mod-text-color);
  }
  button {
    background-color: rgb(31, 144, 210);
  }
  span {
    color: rgb(158, 0, 0);
    text-shadow: 0px 0px 0px rgb(158, 0, 0);
  }
  select {
    background-color: rgba(128, 128, 128, 0.2);
    option {
      background-color: rgba(128, 128, 128, 0.9);
    }
  }
}

.login-page {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  overflow-x: hidden;
  width: 100%;
  height: 100%;
  font-size: 1.5rem;

  .password-container {
    display: flex;
    align-items: center;
    width: 100%;
    i {
      display: flex;
      justify-content: center;
      align-items: center;
    }
    svg {
      opacity: 0;
      position: absolute;
      cursor: pointer;
    }
    svg.show {
      opacity: 1;
    }
  }
}

select {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 30px;
  font-size: 1.5rem;
  padding: 20px;
  width: 30%;
  border-radius: 30px;
  background-color: rgba(128, 128, 128, 0.2);
  color: black;
  transition:
    color 0.5s,
    background-color 0.5s;
  outline: none;
  box-shadow: 0 0 0 5px rgba(128, 128, 128, 1);
  option {
    background-color: rgba(128, 128, 128, 0.2);
  }
}

form {
  display: flex;
  justify-content: center;
  flex-direction: column;
  text-align: center;
  margin: 20px;
  color: black;
  transition:
    background-color 0.5s,
    color 0.5s,
    fill 0.5s,
    filter 0.5s;

  span {
    text-align: left;
    font-weight: bolder;
    color: rgb(200, 0, 0);
    text-shadow: 0px 0px 0px rgb(200, 0, 0);
    transition:
      color 0.5s,
      text-shadow 0.5s;
  }
}

input {
  background: transparent;
  font-size: 2rem;
  border: 0;
  outline: none;
  margin: 20px 0 20px 0;
  border-bottom: 2px solid transparent;
  padding: 5px 20px;
  width: calc(100% - 24px);
  color: black;
  transition:
    border-bottom 0.5s,
    color 0.5s;
  &::placeholder {
    color: rgba($color: #ffffff, $alpha: 0.5);
  }
  &:focus {
    border-bottom: 2px solid black;
  }
}

button {
  border: 0;
  border-radius: 30px;
  background-color: rgb(106, 200, 255);
  padding: 20px;
  font-size: 1.5rem;
  font-weight: bolder;
  color: black;
  margin-top: 10px;
  cursor: pointer;
  transition:
    box-shadow 0.3s,
    background-color 0.5s,
    color 0.5s;
  &:hover {
    box-shadow: 0px 0px 5px white;
  }
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition:
    transform 0.4s ease-out,
    opacity 0.3s ease-in;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-fade-enter-to,
.slide-fade-leave {
  transform: translateX(0%);
  opacity: 1;
}

@media screen and (max-width: 1200px) {
  .login-page {
    font-size: 1.2rem;

    input {
      font-size: 1.2rem;
    }

    button {
      font-size: 1.2rem;
      padding: 10px;
    }
    select {
      font-size: 1.2rem;
      width: 50%;
    }
  }
}
</style>
