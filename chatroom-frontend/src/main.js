import './assets/global.scss'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import icon from './assets/svg/SvgIcon.vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('c-svg', icon)
app.mount('#app')
