<template>
  <div class="block">
    <br><br><br>
    <h3><b>Войдите чтобы продолжить</b></h3><br>
    <b-alert v-if="validationError" show variant="danger" dismissible>Неправильное имя или пароль</b-alert>
    <br>
    <div class="inputs">
        <input v-model="user.username" type="text" class="form-control" placeholder="имя"><br>
        <input v-model="user.password" type="password" class="form-control" placeholder="пароль"><br>
    </div>
    <button v-on:click="login" class="btn btn-dark">Войти</button>
    <br>
  </div>
</template>

<script lang="ts">
import {Component, Vue} from "vue-property-decorator";
import {AuthService} from "@/services/auth.service";


@Component
export default class Login extends Vue{
  user = {
    username: "",
    password: ""
  }

  auth: AuthService = new AuthService();
  validationError = false;

  async login(){

    let response = await this.auth.login(this.user);

    if (response.status == 401){
      this.validationError = true;
    } else {
      this.$router.go(-1);
    }
  }

}
</script>

<style lang="less">

@desktop:   ~"only screen and (min-width: 960px) and (max-width: 1199px)";
@phone:    ~"only screen and (min-width: 20px) and (max-width: 559px)";


.inputs {
  padding: 25px;
}

.block {
  background-image: url("~@/assets/bg.jpg");
  background-size: cover;
  height: 100vh;

}

@media @desktop {
  .block {
    padding-right: 25%;
    padding-left: 25%;
  }
}

@media @phone {
  .block {
    padding-left: 3%;
    padding-right: 3%;
  }
}

</style>