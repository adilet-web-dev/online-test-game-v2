<template>
<div>
  <div id="nav" class="text-left">
    <a v-b-toggle.sidebar-1 class="text-dark" ><b-icon-list class="h1 cm-animate-fat-cursor"></b-icon-list></a>
    <b-sidebar
        id="sidebar-1"
        title="Меню"
        shadow
        backdrop
        bg-variant="dark"
        text-variant="light"
        backdrop-variant="dark"
    >
      <div class="px-3 py-2">

        <router-link to="/" class="router">Главная</router-link><br>
        <router-link :to="{name: 'test list'}" class="router">Все тесты</router-link><br>
        <router-link :to="{name: 'user test list'}" class="router">Мои тесты</router-link><br>
        <router-link :to="{name: 'test create'}" class="router">Создать тест</router-link><br>
        <router-link to="/about"  class="router">О нас</router-link><br>
      </div>
    </b-sidebar>

  </div>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {BIconList} from 'bootstrap-vue';

@Component({
  components: {BIconList}
})
export default class Navbar extends Vue {}
</script>

<style lang="less">

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #ffffff;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

.router {
  font-size: 1.5em;
}
</style>