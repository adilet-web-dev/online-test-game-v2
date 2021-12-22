<template>
  <div class="home">
    <Navbar></Navbar>
    <h1><b>Проходить тесты можно увлекательно!</b></h1>
    <h4>Какая у вас роль?</h4>
    <p class="text-muted">чтобы создать игру вам нужно зарегистрироваться</p><br>
    <router-link to="/tests" class="btn btn-dark">Создатель</router-link>
    <br>
    <router-link to="/player" class="btn btn-outline-dark">Игрок</router-link>

  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Navbar from '../components/Navbar.vue';

@Component({
  components: {Navbar}
})
export default class Home extends Vue {
}
</script>

<style lang="less">
.home {
  background-image: url("~@/assets/bg.jpg");
  background-size: cover;
  height: 100vh;

  .btn {
    width: 150px;
    height: 40px;
    margin-top: 10px;
  }

}


</style>
