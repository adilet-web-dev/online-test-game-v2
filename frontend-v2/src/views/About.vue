<template>
<div class="block">
  <Navbar></Navbar>
  <br>
  <h2>Обзор</h2>
  <hr>
  <p>
    Проходить тесты можно c интересом и то что участники могут видеть
    рейтинг делает прохождение теста конкурентных, так они более
    мотивированы учится. Учение без интереса - плохое учение.
    Мы хотим разработать проекты которые сделают обучение более интересным.
    Следовательно мотивировать учеников, студентов на учебу
  </p>
  <hr>
  <br><br>
  <b>Авторы: <a href="https://github.com/adilet-web-dev">Усонов Адилет</a>,
    <a href="https://github.com/JKLeorio">Козубаев Жуманазар</a>
  </b>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Navbar from '../components/Navbar.vue';

@Component({
  components: {Navbar}
})
export default class About extends Vue {
}

</script>

<style scoped>
.block {
  color: white;
  height: 100vh;
  width: 100vw;
  background-color: black;
  text-align: center;

}
</style>