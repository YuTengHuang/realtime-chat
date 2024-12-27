import { ref } from 'vue'
import { defineStore, storeToRefs } from 'pinia'
import { useToastStore } from '@/stores/toast'
import { useUserStore } from './user'
import Swal from 'sweetalert2'
import router from '@/router'

export const useGlobalStore = defineStore('global', () => {
  const toastStore = useToastStore()
  const { SuccessToast, CancelToast, JoinGruopRoomToast } = toastStore

  const userStore = useUserStore()
  const { user } = storeToRefs(userStore)

  const allUsers = ref([])
  const allRooms = ref([])
  const allMessage = ref([])

  const sentList = ref([])
  const requestList = ref([])

  const friendsList = ref([])
  const blockedList = ref([])

  const roomInviteList = ref([])

  const socket = ref(null)
  const callbacks = {}

  const openInfo = ref(false)
  const userInfo = ref(null)
  const groupInfo = ref(null)
  const imgInfo = ref(null)
  const openList = ref(true)

  const openCreateGroupChat = ref({
    open: false,
    name: null,
    users: []
  })

  const totalMessageCount = ref(0)
  const roomMessageCount = ref([])

  const openChatRoom = ref({
    open: false,
    data: null
  })

  const ActionsFunc = {
    'token.expired': (data) => {
      CancelToast(data, 'warning')
    },

    'unknow.action': (data) => {
      CancelToast(data, 'error')
    },

    'get.all.users': (data) => {
      allUsers.value = data
    },

    'get.friends.list': (data) => {
      if (!data.error) {
        friendsList.value = data.friends
        blockedList.value = data.blocked
      }
    },

    'get.friend.request': (data) => {
      sentList.value = data.sentRequests
      requestList.value = data.receivedRequests
    },

    'get.all.rooms': (data) => {
      allRooms.value = data
      data.forEach((room) => {
        roomMessageCount.value[room.id] = 0
      })
    },

    'get.room.invite': (data) => {
      roomInviteList.value = data
    },

    'send.friend.request': (data) => {
      if (data.sentRequests !== undefined) {
        sentList.value.push(data.sentRequests)
      }
      if (data.receivedRequests !== undefined) {
        requestList.value.push(data.receivedRequests)
      }
    },

    'agree.friend.request': (data) => {
      const sentIndex = sentList.value.findIndex((item) => item.id === data.request)
      const requestIndex = requestList.value.findIndex((item) => item.id === data.request)

      if (data.error) {
        SuccessToast(data.error, 'error')
      } else if (!data.error && !friendsList.value.some((item) => item.id === data.friend.id)) {
        friendsList.value.push(data.friend)
      }

      if (sentIndex !== -1) {
        sentList.value.splice(sentIndex, 1)
      }
      if (requestIndex !== -1) {
        requestList.value.splice(requestIndex, 1)
        const targetUser = friendsList.value.find((item) => item.id === data.friend.id)
        if (targetUser) {
          targetUser.IsFriend = true
          SuccessToast('添加成功')
        }
      }
    },

    'reject.friend.request': (data) => {
      const sentIndex = sentList.value.findIndex((item) => item.id === data.request)
      const requestIndex = requestList.value.findIndex((item) => item.id === data.request)
      if (sentIndex !== -1) {
        sentList.value.splice(sentIndex, 1)
        if (data.reject) {
          CancelToast('取消邀請!', 'success')
        }
      }
      if (requestIndex !== -1) {
        requestList.value.splice(requestIndex, 1)
        if (data.reject) {
          CancelToast('拒絕成功!')
        }
      }
    },

    'get.all.message': (data) => {
      allMessage.value = data
    },

    'send.message': (data) => {
      if (!allRooms.value.some((room) => room.id === data.room.id)) {
        allRooms.value.push(data.room)
      }
      allMessage.value.push(data.message)
      if (!(openChatRoom.value?.data?.id === data.message.room)) {
        roomMessageCount.value[data.message.room] =
          (roomMessageCount.value[data.message.room] || 0) + 1
        totalMessageCount.value++
      }
      Swal.close()
    },

    'block.friend': (data) => {
      if (data.id && data.sender) {
        const targetUser = friendsList.value.find((item) => item.id === data.id)
        if (targetUser) {
          friendsList.value = friendsList.value.filter((item) => item.id !== data.id)
          blockedList.value.push(targetUser)
        }
        openInfo.value = false
        userInfo.value = null
      }

      if (data.id && !data.sender) {
        const friend = friendsList.value.find((item) => item.id === data.id)
        const block = blockedList.value.find((item) => item.id === data.id)
        if (friend) {
          friend.AmIBlocked = data.AmIBlocked
        }
        if (block) {
          block.AmIBlocked = data.AmIBlocked
        }
      }
    },

    'unblock.friend': (data) => {
      if (data.friend && data.sender) {
        const index = blockedList.value.findIndex((item) => item.id === data.friend.id)
        if (index !== -1) {
          blockedList.value.splice(index, 1)
          friendsList.value.push(data.friend)
        }
      }

      if (data.id && !data.sender) {
        const friend = friendsList.value.find((item) => item.id === data.id)
        const block = blockedList.value.find((item) => item.id === data.id)
        if (friend) {
          friend.AmIBlocked = data.AmIBlocked
          friend.IsFriend = true
        }
        if (block) {
          block.AmIBlocked = data.AmIBlocked
        }
      }
    },

    'remove.friend': (data) => {
      const targetUserIndex = friendsList.value.findIndex((item) => item.id === data.id)
      if (targetUserIndex !== -1) {
        friendsList.value.splice(targetUserIndex, 1)
        openInfo.value = false
        userInfo.value = null
      }
    },

    'quit.chat': (data) => {
      if (data.roomId) {
        allRooms.value = allRooms.value.filter((room) => room.id !== data.roomId)
        openChatRoom.value.open = false
        openChatRoom.value.data = null
      } else {
        allMessage.value.push(data.message)
        if (groupInfo.value !== null) {
          const quitUserIndex = groupInfo.value.findIndex((user) => user.id === data.userId)
          groupInfo.value.splice(quitUserIndex, 1)
        }
        let room = allRooms.value.find((room) => room.id === data.message.room)
        if (room) {
          room.users = data.updateRoom.users
        }
      }
    },

    'create.group.chat': (data) => {
      if (data.room) {
        allRooms.value.push(data.room)
        roomMessageCount.value[data.room.id] = 0
      }
      if (data.roomInvite) {
        roomInviteList.value.push(data.roomInvite)
      }
    },

    'invite.join.group.chat': (data) => {
      if (data.message) {
        SuccessToast(data.message)
      }
      if (data.roomInvite) {
        roomInviteList.value.push(data.roomInvite)
      }
    },

    'agree.invite': (data) => {
      if (data.id) {
        allRooms.value.push(data.room)
        roomMessageCount.value[data.room.id] = 0
        roomInviteList.value = roomInviteList.value.filter((inv) => inv.id !== data.id)
        JoinGruopRoomToast()
      }

      if (data.error) {
        const inviteIndex = roomInviteList.value.findIndex((inv) => inv.id === data.error)
        if (inviteIndex !== -1) {
          roomInviteList.value.splice(inviteIndex, 1)
          CancelToast('此群組已關閉!')
        }
      }

      if (data.message) {
        let room = allRooms.value.find((room) => room.id === data.room.id)
        if (room) {
          room.users = data.room?.users
        }

        allMessage.value.push(data.message)
      }
    },

    'reject.invite': (data) => {
      const inviteIndex = roomInviteList.value.findIndex((inv) => inv.id === data.id)
      if (inviteIndex !== -1) {
        roomInviteList.value.splice(inviteIndex, 1)
        CancelToast('拒絕成功!')
      }
    },

    'update.user.info': (data) => {
      if (data.message) {
        user.value.username = data.user.username
        user.value.profile = data.user.profile
        localStorage.setItem('username', data.user.username)
        localStorage.setItem('profile', data.user.profile)
        if (data.user.avatar !== user.value.avatar) {
          localStorage.setItem('avatar', data.user.avatar)
          user.value.avatar = data.user.avatar
          Swal.close()
        }
        SuccessToast(data.message)
      } else {
        UpdateTargetUserInfo(data)
      }
    },

    'remove.avatar': (data) => {
      if (data.message) {
        localStorage.setItem('avatar', data.avatar)
        user.value.avatar = data.avatar
        Swal.close()
        SuccessToast(data.message)
      } else {
        UpdateTargetUserInfo(data)
      }
    }
  }

  function ConnectWebsocket() {
    if (!socket.value || socket.value.readyState === WebSocket.CLOSED) {
      socket.value = new WebSocket(
        // `wss://your-domain.com/ws/chat_rooms/?token=${localStorage.getItem('access')}`
        `ws://127.0.0.1:8080/ws/chat_rooms/?token=${localStorage.getItem('access')}` // dev
      )
      socket.value.onopen = () => {
        GetInitData()
      }
    }

    socket.value.onerror = () => {
      userStore.RemoveToken()
      CancelToast('連線錯誤，請重新登入!', 'error')
      router.push('/')
    }

    socket.value.onmessage = (e) => {
      const msg = JSON.parse(e.data)

      // get.or.create.room GetOrCreatePersonalRoom()
      if (msg.action && callbacks[msg.action]) {
        callbacks[msg.action](msg.data)
        delete callbacks[msg.action]
      }

      if (ActionsFunc[msg.action]) {
        ActionsFunc[msg.action](msg.data)
      }
    }

    socket.value.onclose = (event) => {
      if (event.code === 4000) {
        userStore.RemoveToken()
        router.push({ name: 'auth' })
      } else if (event.code === 4001) {
        userStore.RemoveToken()
        router.push({ name: 'auth' })
      }
    }
  }

  function GetInitData() {
    socket.value.send(
      JSON.stringify({
        action: 'get.all.users'
      })
    )

    socket.value.send(
      JSON.stringify({
        action: 'get.friends.list'
      })
    )

    socket.value.send(
      JSON.stringify({
        action: 'get.friend.request'
      })
    )

    socket.value.send(
      JSON.stringify({
        action: 'get.all.rooms'
      })
    )

    socket.value.send(
      JSON.stringify({
        action: 'get.room.invite'
      })
    )
  }

  function GetOrCreatePersonalRoom(id) {
    return new Promise((resolve) => {
      if (id) {
        callbacks['get.or.create.room'] = (data) => {
          const existRoom = allRooms.value.some((room) => room.id === data.id)
          if (!existRoom) {
            allRooms.value.push(data)
            roomMessageCount.value[data.id] = 0
          }
          resolve(data)
        }

        socket.value.send(
          JSON.stringify({
            action: 'get.or.create.room',
            receiver: id
          })
        )
      }
      return
    })
  }

  function UpdateTargetUserInfo(data) {
    let user = allUsers.value.find((user) => user.id === data.friend.id)
    let room = allRooms.value.find(
      (room) => room.room_type === 'personal' && room.users.receiver.id === data.friend.id
    )
    let friend = friendsList.value.find((friend) => friend.id === data.friend.id)

    allRooms.value.forEach((room) => {
      if (room.room_type === 'group') {
        const groupUser = room.users.find((user) => user.id === data.friend.id)
        if (groupUser) {
          UpdateTargetUsernameAvatar(groupUser, data)
        }
      }
    })

    if (friend && user && room) {
      UpdateTargetUsernameAvatar(user, data)
      UpdateTargetUsernameAvatar(room.users.receiver, data)
      UpdateTargetUsernameAvatar(friend, data)
      friend.profile = data.friend.profile
    }
  }

  function UpdateTargetUsernameAvatar(user, data) {
    if (user) {
      user.username = data.friend.username
      user.avatar = data.friend.avatar
    }
  }

  function SendFriendRequest(id) {
    if (id) {
      socket.value.send(
        JSON.stringify({
          action: 'send.friend.request',
          receiver: id
        })
      )
    }
    return
  }

  function SendMessage(data) {
    if (data) {
      socket.value.send(
        JSON.stringify({
          action: 'send.message',
          data: data
        })
      )
    }
    return
  }

  function GetAllMessage(roomId) {
    socket.value.send(
      JSON.stringify({
        action: 'get.all.message',
        room: roomId
      })
    )
  }

  function AgreeRequest(request) {
    if (request) {
      socket.value.send(
        JSON.stringify({
          action: 'agree.friend.request',
          request: request
        })
      )
    }
    return
  }

  function RejectRequest(request) {
    if (request) {
      socket.value.send(
        JSON.stringify({
          action: 'reject.friend.request',
          request: request
        })
      )
    }
    return
  }

  function BlockFriend(id) {
    if (id) {
      socket.value.send(
        JSON.stringify({
          action: 'block.friend',
          receiver: id
        })
      )
    }
    return
  }

  function UnblockFriend(id) {
    if (id) {
      socket.value.send(
        JSON.stringify({
          action: 'unblock.friend',
          receiver: id
        })
      )
    }
    return
  }

  function RemoveFriend(id) {
    if (id) {
      socket.value.send(
        JSON.stringify({
          action: 'remove.friend',
          receiver: id
        })
      )
    }
    return
  }

  function CreateGruopChat(name, users) {
    if ((name, users)) {
      socket.value.send(
        JSON.stringify({
          action: 'create.group.chat',
          name: name,
          users: users
        })
      )
    }
    return
  }

  function InviteJoinGruopChat(id, users) {
    if ((id, users)) {
      socket.value.send(
        JSON.stringify({
          action: 'invite.join.group.chat',
          id: id,
          users: users
        })
      )
    }
    return
  }

  function OuitChat(id) {
    if (id) {
      socket.value.send(
        JSON.stringify({
          action: 'quit.chat',
          room: id
        })
      )
    }
    return
  }

  function AgreeInvite(id) {
    if (id) {
      socket.value.send(
        JSON.stringify({
          action: 'agree.invite',
          invite: id
        })
      )
    }
    return
  }

  function RejectInvite(id) {
    if (id) {
      socket.value.send(
        JSON.stringify({
          action: 'reject.invite',
          invite: id
        })
      )
    }
    return
  }

  function UpdateUserInfo(data) {
    if (data) {
      socket.value.send(
        JSON.stringify({
          action: 'update.user.info',
          updateData: data
        })
      )
    }
    return
  }

  function RemoveAvatar() {
    socket.value.send(
      JSON.stringify({
        action: 'remove.avatar'
      })
    )
  }

  function CloseWebsocket() {
    socket.value.close()
  }

  return {
    allUsers,
    allRooms,
    friendsList,
    requestList,
    sentList,
    blockedList,
    openInfo,
    userInfo,
    groupInfo,
    imgInfo,
    openList,
    openChatRoom,
    allMessage,
    totalMessageCount,
    roomMessageCount,
    openCreateGroupChat,
    roomInviteList,
    ConnectWebsocket,
    CloseWebsocket,
    SendFriendRequest,
    RejectRequest,
    AgreeRequest,
    GetOrCreatePersonalRoom,
    SendMessage,
    GetAllMessage,
    BlockFriend,
    UnblockFriend,
    RemoveFriend,
    OuitChat,
    CreateGruopChat,
    AgreeInvite,
    RejectInvite,
    InviteJoinGruopChat,
    UpdateUserInfo,
    RemoveAvatar
  }
})
