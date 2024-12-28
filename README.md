# :speech_balloon: Realtime-Chat

## Live Demo
- [Demo](https://ytcustom.sytes.net/)

## 簡介
這是一個基於 Vue.js 、 Django 的即時聊天室，透過 Websokcet API 連線並結合 Django Channels 實現即時的互動功能。支援私人聊天、群組討論及圖片上傳。

## 功能
- 用戶註冊和登入
- 提供預設帳號使用
- 好友列表管理
- 即時聊天

## 技術堆疊
- 前端: Vue.js
- 後端: Django 、 Django REST framework
- 伺服器: Nginx
- ASGI 伺服器: Daphne
- 容器化: Docker 、 Docker Compose
- 資料庫: PostgreSQL

## 環境需求
- Docker 20.x
- Docker Compose v2.x

OR
- Python 3.8+
- Node.js v18+

## 安裝與使用 ( 2種 )
### ( 一 ) 使用 Docker 執行
#### 1. clone 專案
```
git clone https://github.com/YuTengHuang/realtime-chat.git 
```
#### 2. 建置Docker容器
```
cd realtime-chat
docker compose up --build
```
#### 3. 運行完成
開啟瀏覽器並輸入:
```
127.0.0.1
```
Django admin
```
127.0.0.1:8080/admin

Email: admin@admin.com
Password: admin123456789
```
#### 4. 關閉，移除專案
在終端機按下 ``` Crtl + C ``` 停止運行

移除專案:
```
docker compose down -v --rmi all
```
這會移除所有由該docker-compose.yml建置的container、images、volumns，最後可直接移除專案資料夾。


### ( 二 ) 使用本地環境執行
#### 1. 創建資料夾
新增資料夾如: mychat ，後續操作皆在該資料夾內。
#### 2. 創建虛擬環境

創建虛擬環境:
```
python -m venv myenv
```
啟動虛擬環境:
```
myenv\Scripts\activate
```

> [!NOTE] 
> 若無法啟動則需要用管理員模式開啟 PowerShell 執行以下:
>```bash
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> 參考: [官方文檔](https://docs.python.org/zh-tw/3.13/library/venv.html#creating-virtual-environments)

#### 3. clone 專案
```
git clone https://github.com/YuTengHuang/realtime-chat.git 
```

#### 4. 安裝依賴項
開啟2個終端機並啟動虛擬環境

安裝 Django 依賴項:
```
cd .\realtime-chat\chatroom\
pip install -r requirements.txt
```
設置資料庫:
```
python manage.py migrate
```
> [!TIP]
> 如果想要使用 Django admin 請創建超級用戶
> ```
> python manage.py createsuperuser
> 
> Email: admin@admin.com
> Username: admin
> Password: admin123456789
> ```

啟動 Django 伺服器:
```
python manage.py runserver 0.0.0.0:8080
```

安裝並啟動 Vue 開發伺服器:
```
cd .\realtime-chat\chatroom-frontend\
npm ci
npm run dev
```

#### 5. 運行完成
開啟瀏覽器並輸入:
```
127.0.0.1
```
Django admin
```
127.0.0.1:8080/admin

Email: admin@admin.com
Password: admin123456789
```

#### 6. 關閉，移除專案
停止 Django 伺服器： ``` Ctrl + C ```

停止 Vue 開發伺服器: ``` q + Enter ```

停用虛擬環境:
```
deactivate
```
移除 mychat 資料夾即可。