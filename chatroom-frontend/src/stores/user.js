import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const user = ref({
    isAuth: false,
    id: null,
    email: null,
    username: null,
    avatar: null,
    profile: null,
    access: null,
    refresh: null,
    is_default: false
  })

  const keys = ['id', 'email', 'username', 'avatar', 'profile', 'access', 'is_default']

  function InitStore() {
    if (user.value.id || user.value.isAuth) {
      return
    }

    const token = localStorage.getItem('access')
    if (token) {
      keys.forEach((key) => {
        user.value[key] = localStorage.getItem(key)
      })
      user.value.isAuth = true
    }
  }

  function SetToken(data) {
    ;[...keys, 'access'].forEach((key) => {
      localStorage.setItem(key, data[key])
    })

    user.value.id = data.id
    user.value.email = data.email
    user.value.username = data.username
    user.value.avatar = data.avatar
    user.value.profile = data.profile
    user.value.access = data.access
    user.value.refresh = data.refresh
    user.value.is_default = data.is_default
    user.value.isAuth = true
  }

  function RemoveToken() {
    ;[...keys, 'access'].forEach((key) => {
      localStorage.removeItem(key)
    })

    user.value.id = null
    user.value.email = null
    user.value.username = null
    user.value.avatar = null
    user.value.profile = null
    user.value.access = null
    user.value.refresh = null
    user.value.is_default = false
    user.value.isAuth = false
  }

  return { user, InitStore, SetToken, RemoveToken }
})
