<script setup>
import { ref } from 'vue'
import { SignUpAxios } from '@/stores/api'
import { useToastStore } from '@/stores/toast'
import Swal from 'sweetalert2'

const toastStore = useToastStore()
const { SuccessToast, CancelToast, LoadingToast } = toastStore

const checkPassword = ref({
  password: false,
  confirmPassword: false
})
const ToggleCheckPassword = (key) => {
  checkPassword.value[key] = !checkPassword.value[key]
}

const errorMsg = ref({
  email: '',
  username: '',
  password: '',
  confirmPassword: ''
})

const InitUserDataForSignUp = () => ({
  email: '',
  username: '',
  password: '',
  confirmPassword: ''
})

const formData = ref(InitUserDataForSignUp())

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

  if (formData.value.password !== formData.value.confirmPassword) {
    CancelToast('密碼不一樣!', 'error')
    return
  }

  try {
    LoadingToast('驗證中...', '等待驗證完成')
    const signupResponse = await SignUpAxios('signup/', formData.value)
    formData.value = InitUserDataForSignUp()
    SuccessToast(signupResponse.message)
  } catch (error) {
    Swal.close()
    const msg = error.response.data
    CancelToast('註冊失敗', 'error', msg.non_field_errors ? msg.non_field_errors[0] : msg.email[0])
    formData.value = InitUserDataForSignUp()
  }
}
</script>

<template>
  <div class="signup-page">
    <form @submit.prevent="SubmitForm">
      <h1>Join Us</h1>
      <input
        id="signup-email"
        type="email"
        v-model="formData.email"
        placeholder="Email"
        autocomplete="off"
        maxlength="50"
        @blur="CheckField('email', 'email')"
      />
      <span>{{ errorMsg.email }}</span>

      <input
        id="signup-username"
        type="text"
        v-model="formData.username"
        placeholder="UserName"
        autocomplete="off"
        maxlength="20"
        @blur="CheckField('username', 'username')"
      />
      <span>{{ errorMsg.username }}</span>

      <div class="password-container">
        <div class="input-group">
          <input
            id="signup-password"
            :type="checkPassword.password ? 'text' : 'password'"
            v-model="formData.password"
            placeholder="Password"
            autocomplete="off"
            minlength="8"
            @blur="CheckField('password', 'password')"
          />
          <i @click="ToggleCheckPassword('password')">
            <c-svg name="NoCheckPassWord" :class="{ show: !checkPassword.password }" />
            <c-svg name="CheckPassWord" :class="{ show: checkPassword.password }" />
          </i>
        </div>
        <span>{{ errorMsg.password }}</span>

        <div class="input-group">
          <input
            id="signup-confirmPassword"
            :type="checkPassword.confirmPassword ? 'text' : 'password'"
            v-model="formData.confirmPassword"
            placeholder="Confirm Password"
            autocomplete="off"
            minlength="8"
            @blur="CheckField('confirmPassword', 'confirmPassword')"
          />
          <i @click="ToggleCheckPassword('confirmPassword')">
            <c-svg name="NoCheckPassWord" :class="{ show: !checkPassword.confirmPassword }" />
            <c-svg name="CheckPassWord" :class="{ show: checkPassword.confirmPassword }" />
          </i>
        </div>
        <span>{{ errorMsg.confirmPassword }}</span>
      </div>
      <button type="submit">註冊</button>
    </form>
  </div>
</template>

<style lang="scss" scoped>
#app.dark {
  form {
    color: var(--dark-mod-text-color);
    input,
    button {
      color: inherit;
    }
    button {
      background-color: rgb(31, 144, 210);
    }
    span {
      color: rgb(158, 0, 0);
    }
  }
}

.signup-page {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow-x: hidden;
  width: 100%;
  height: 100%;
  font-size: 1.5rem;

  .password-container {
    display: flex;
    align-items: start;
    flex-direction: column;
    width: 100%;
    .input-group {
      display: flex;
      align-items: center;
      margin: 10px 0;
      i {
        display: flex;
        justify-content: center;
        align-items: center;
      }
      svg {
        margin: 0;
        padding: 0;
        opacity: 0;
        position: absolute;
        cursor: pointer;
      }
      svg.show {
        opacity: 1;
      }
    }
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
  outline: none;
  flex: 1;
  border: 0;
  font-size: 2rem;
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
  transform: translateX(100%);
  opacity: 0;
}

.slide-fade-enter-to,
.slide-fade-leave {
  transform: translateX(0%);
  opacity: 1;
}

@media screen and (max-width: 1200px) {
  .signup-page {
    font-size: 1.2rem;

    input {
      font-size: 1.2rem;
    }

    button {
      font-size: 1.2rem;
      padding: 10px;
    }
  }
}
</style>
