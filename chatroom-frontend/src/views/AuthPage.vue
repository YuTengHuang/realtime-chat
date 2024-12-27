<script setup>
import { ref, defineAsyncComponent } from 'vue'
import LoginForm from '@/components/AuthPage/LoginForm.vue'
const SignUpForm = defineAsyncComponent(() => import('@/components/AuthPage/SignUpForm.vue'))

const showLogin = ref(true)
const IsLogin = () => {
  showLogin.value = true
}
const IsSignUp = () => {
  showLogin.value = false
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-bar">
      <button @click="IsLogin" :class="{ active: showLogin }">Login</button>
      <div class="mid-line"></div>
      <button @click="IsSignUp" :class="{ active: !showLogin }">SignUp</button>
    </div>
    <div class="auth-content">
      <transition name="slide-fade">
        <component :is="showLogin ? LoginForm : SignUpForm" key="form" />
      </transition>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#app.dark {
  .auth-bar {
    button {
      color: rgba(255, 255, 255, 0.7);
      &.active {
        background: rgb(31, 144, 210);
      }
    }
  }
}
.auth-page {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

button {
  position: relative;
  background-color: transparent;
  padding: 10px;
  font-size: 2.5rem;
  border: 0;
  width: 40%;
  cursor: pointer;
  transition:
    transform 0.3s,
    text-shadow 0.3s,
    background-color 0.3s,
    border-radius 0.3s,
    color 0.3s;

  &.active {
    background-color: rgb(106, 200, 255);
    border-radius: 30px;
  }

  &:hover {
    transform: scale(1.1);
    text-shadow: 1px 1px 5px white;
  }

  &::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    background-color: black;
    width: 0px;
    height: 2px;
    transition: width 0.3s;
  }
  &:hover::after {
    width: 100%;
  }
}

.auth-bar {
  display: flex;
  justify-content: space-around;
  margin: 10px;

  .mid-line {
    border: 1px solid black;
  }
}

.auth-content {
  display: flex;
  flex-direction: row;
  overflow: hidden;
  width: 100%;
  height: 100%;
}

@media screen and (max-width: 1200px) {
  button {
    font-size: 1.5rem;
  }
  .auth-bar {
    margin: 0;
    margin-top: 10px;
  }
}
</style>
