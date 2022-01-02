<template>
  <div class="pl-2 pr-2">
    <Navbar></Navbar>
    <b-alert v-if="error" show variant="danger" dismissible>
      Не получилось получить список тестов :( <br>
      Это либо у вас интернет не работает или на сервере что-то случилось
    </b-alert>

    <h5>Список тестов</h5>

    <hr>
    <div v-for="test in tests">
      <div class="row">
        <hr>
        <div class="col-4">
          <router-link v-bind:to="'tests/' + test.id" class="test-link"><h6><b>{{test.name}}</b></h6></router-link>
        </div>
        <div class="col-4">
          <p>{{test.questions.length}} вопросов</p>
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
import Navbar from "@/components/Navbar.vue";

@Component({
  components: {Navbar}
})
export default class UserTestList extends Vue {

  tests = [];
  error = false;
  api: ApiService = new ApiService();


  play(id: number){

    this.$router.push("/creator/"+ id);
  }


  async mounted(){

    let response = await this.api.getUserTestList();

    if (response.status == 401) this.$router.push('/login');
    if (response.status == 405) this.error = true;
    else {
      this.tests = response.tests;
    }
  }
}
</script>

<style lang="less">
.mybtn {
  width: 150px;
  height: 40px;
}

.test-link {
  color: black;
  text-decoration: underline;
}


</style>