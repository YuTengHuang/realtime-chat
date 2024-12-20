import customAxios from './customAxios'

export const LoginAxios = async (url, params) => {
  try {
    const response = await customAxios.post(url, params)
    return response.data
  } catch (error) {
    if (error.response) {
      return Promise.reject(error.response.data)
    } else {
      return Promise.reject({ detail: '無法連接伺服器，請檢查網路或服務器狀態。' })
    }
  }
}

export const SignUpAxios = async (url, params) => {
  try {
    const response = await customAxios.post(url, params)
    return response.data
  } catch (error) {
    return Promise.reject(error)
  }
}

export const PostFriendRequestAxios = async (url, params) => {
  try {
    const response = await customAxios.post(url, params)
    return response.data
  } catch (error) {
    return Promise.reject(error)
  }
}

export const GetFriendRequestAxios = async (url, params) => {
  try {
    const response = await customAxios.get(url, params)
    return response.data
  } catch (error) {
    return Promise.reject(error)
  }
}

export const GetAllRoomsAxios = async (url, params) => {
  try {
    const response = await customAxios.get(url, params)
    return response.data
  } catch (error) {
    return Promise.reject(error)
  }
}

export const GetAllAccountsAxios = async (url, params) => {
  try {
    const response = await customAxios.get(url, params)
    return response.data
  } catch (error) {
    return Promise.reject(error)
  }
}

export const GetFriendsAxios = async (url, params) => {
  try {
    const response = await customAxios.get(url, params)
    return response.data
  } catch (error) {
    return Promise.reject(error)
  }
}

export const AgreeRequestAxios = async (url, params) => {
  try {
    const response = await customAxios.patch(url, params)
    return response.data
  } catch (error) {
    return Promise.reject(error)
  }
}
export const RejectRequestAxios = async (url, params) => {
  try {
    const response = await customAxios.patch(url, params)
    return response.data
  } catch (error) {
    return Promise.reject(error)
  }
}

export const deltefriends = async (url, params) => {
  try {
    const response = await customAxios.delete(url, params)
    return response.data
  } catch (error) {
    return Promise.reject(error)
  }
}

export const blockedfriend = async (url, params) => {
  try {
    const response = await customAxios.post(url, params)
    return response.data
  } catch (error) {
    return Promise.reject(error)
  }
}

export const unblockedfriend = async (url, params) => {
  try {
    const response = await customAxios.delete(url, params)
    return response.data
  } catch (error) {
    return Promise.reject(error)
  }
}
