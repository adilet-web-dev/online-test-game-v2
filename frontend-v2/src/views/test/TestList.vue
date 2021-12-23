<template>
  <div>
    <Navbar></Navbar>
    <b-alert v-if="error" show variant="danger" dismissible>
      Не получилось получить список тестов :( <br>
      Это либо у вас интернет не работает или на сервере что-то случилось
    </b-alert>
    <div class="row">
      <div class="col-4"></div>
      <div class="col-4"><h3>Список тестов</h3></div>
      <div class="col-4">
        <router-link :to="{name: 'test create'}" class="btn btn-outline-dark">Создать тест</router-link>
      </div>
    </div>

    <hr>
    <div v-for="test in tests">
      <div class="row">
        <hr>
        <div class="col-4">
          <h5><b>{{test.name}}</b></h5>
        </div>
        <div class="col-4">
          <div class="row">
            <div class="col-6">
              <p>{{test.questions.length}} вопросов</p>
            </div>
            <div class="col-6">
              <button v-on:click="$router.push('tests/' + test.id)" class="btn btn-outline-dark mybtn">обзор</button>
              <br>
<!--              <button v-on:click="$router.push({'name': 'test edit', params: {'id': test.id}})"-->
<!--                      class="btn btn-primary mybtn">-->
<!--                редактировать-->
<!--              </button>-->
            </div>
          </div>

        </div>
        <div class="col-4">
          <button class="btn btn-dark" v-on:click="play(test.id)">Играть</button>
        </div>

      </div>
      <hr>
    </div>

  </div>

</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {ApiService} from "@/services/api.service";
import Navbar from '../../components/Navbar.vue';

@Component({
  components: {Navbar}
})
export default class TestList extends Vue {

  tests = [];
  error = false;

  async mounted(){
    let api: ApiService = new ApiService();

    let response = await api.getTestList();
    if (response.status == 401) {
      this.$router.push("/login");
    }
    else if (response.status == 405) {
      this.error = true;
    }
    this.tests = response.tests;

  }

  play(id: number){

    this.$router.push("/creator/"+ id);
  }
}
</script>

<style lang="less">
.mybtn {
  width: 150px;
  height: 40px;
}

</style>
