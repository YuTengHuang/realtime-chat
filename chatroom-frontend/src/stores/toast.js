import { defineStore } from 'pinia'
import Swal from 'sweetalert2'

export const useToastStore = defineStore('toast', () => {
  const BlockUserToast = (CallBackFunc) => {
    Swal.fire({
      title: '確定封鎖?',
      html: '<div>封鎖用戶對方將無法與你聯絡!<br/>可以隨時取消封鎖!</div>',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: '確認',
      cancelButtonText: '取消'
    }).then((result) => {
      if (result.isConfirmed) {
        CallBackFunc()
        Swal.fire({
          title: '已封鎖!',
          text: '用戶將無法與你聯絡',
          icon: 'success'
        })
      }
    })
  }

  const UnblockUserToast = (CallBackFunc) => {
    Swal.fire({
      title: '確定解除封鎖?',
      html: '<div>解除封鎖用戶對方將可以與你聯絡!</div>',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: '確認',
      cancelButtonText: '取消'
    }).then((result) => {
      if (result.isConfirmed) {
        CallBackFunc()
        Swal.fire({
          title: '已解除封鎖!',
          text: '用戶將可以與你聯絡',
          icon: 'success'
        })
      }
    })
  }

  const UnfriendToast = (CallBackFunc) => {
    Swal.fire({
      title: '確定移除好友?',
      html: '<div>移除好友後你將會從對方好友名單內移除，但聊天紀錄仍然存在!</div>',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: '確認',
      cancelButtonText: '取消'
    }).then((result) => {
      if (result.isConfirmed) {
        CallBackFunc()
        Swal.fire({
          title: '已移除好友!',
          text: '聊天紀錄仍然存在',
          icon: 'success'
        })
      }
    })
  }

  const PostRequestToast = (CallBackFunc) => {
    Swal.fire({
      title: '確定發送好友邀請?',
      html: '<div>確定後將等待對方回覆!</div>',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: '確認',
      cancelButtonText: '取消'
    }).then((result) => {
      if (result.isConfirmed) {
        CallBackFunc()
        Swal.fire({
          position: 'center',
          title: '已發送好友邀請!',
          icon: 'success',
          showConfirmButton: false,
          timer: 1500
        })
      }
    })
  }

  const QuitGroupChatToast = (CallBackFunc) => {
    Swal.fire({
      title: '確定退出此群組?',
      html: '<div>退出後將移除此聊天紀錄!</div>',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: '確認',
      cancelButtonText: '取消'
    }).then((result) => {
      if (result.isConfirmed) {
        CallBackFunc()
        Swal.fire({
          position: 'center',
          title: '已退出此群組!',
          icon: 'success',
          showConfirmButton: false,
          timer: 1500
        })
      }
    })
  }

  const RemoveAvatarToast = (CallBackFunc) => {
    Swal.fire({
      title: '確定移除當前頭像?',
      html: '<div>確認後將移除當前頭像!</div>',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: '確認',
      cancelButtonText: '取消'
    }).then((result) => {
      if (result.isConfirmed) {
        CallBackFunc()
        Swal.fire({
          title: '移除圖片中...',
          html: '移除速度取決於圖片大小及網路速度',
          allowEscapeKey: false,
          allowOutsideClick: false,
          didOpen: () => {
            Swal.showLoading()
          }
        })
      }
    })
  }

  const SuccessToast = (msg, icon) => {
    Swal.fire({
      position: 'center',
      icon: icon || 'success',
      title: msg,
      showConfirmButton: false,
      timer: 1500
    })
  }

  const CancelToast = (title, icon, html) => {
    Swal.fire({
      position: 'center',
      icon: icon,
      title: title,
      html: `<h3>${html || ''}</h3>`,
      showConfirmButton: false,
      timer: 1500
    })
  }

  const CreateGruopChatToast = () => {
    Swal.fire({
      position: 'center',
      icon: 'warning',
      title: '請輸入群組名稱!',
      showConfirmButton: false,
      timer: 1500
    })
  }

  const JoinGruopRoomToast = () => {
    Swal.fire({
      position: 'center',
      icon: 'success',
      title: '已加入群組!',
      showConfirmButton: false,
      timer: 1500
    })
  }

  const LoadingToast = (title, msg) => {
    Swal.fire({
      title: title,
      html: msg,
      allowEscapeKey: false,
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading()
      }
    })
  }

  const AttentionToast = () => {
    Swal.fire({
      html: `
      <h1>注意事項!</h1>
      <p style="font-size: 30px;">
        此為練習用，無商業用途!<br>
        <mark><u>請勿發送</u></mark>
        <strong>個人資訊</strong>、
        <strong>不雅圖片</strong>及
        <strong>字眼</strong>。
      </p>
      `,
      icon: 'warning'
    })
  }

  return {
    BlockUserToast,
    UnblockUserToast,
    SuccessToast,
    CancelToast,
    UnfriendToast,
    PostRequestToast,
    QuitGroupChatToast,
    CreateGruopChatToast,
    JoinGruopRoomToast,
    LoadingToast,
    RemoveAvatarToast,
    AttentionToast
  }
})
