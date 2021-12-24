<template>
  <div class="block">
    <br><br><br>
    <h3><b>Регистрация</b></h3><br>
    <b-alert v-if="error400" show variant="danger" dismissible>Пользователь под этим именем уже существует</b-alert>
    <b-alert v-if="error400" show variant="danger" dismissible>Неправильная ссылка у вас</b-alert>
    <b-alert v-if="passwordError" show variant="danger" dismissible>Пароли не совпадают</b-alert>
    <br>
    <div class="inputs">
        <input v-model="username" type="text" class="form-control" placeholder="имя"><br>
        <input v-model="password" type="password" class="form-control" placeholder="пароль"><br>
        <input v-model="password2" type="password" class="form-control" placeholder="повторите пароль"><br>
    </div>
    <button v-on:click="signup" class="btn btn-dark">Зарегистрироваться</button>
    <br>
  </div>
</template>

<script lang="ts">
import {Component, Vue} from "vue-property-decorator";
import {AuthService} from "@/services/auth.service";


@Component
export default class Signup extends Vue{

  username: string = "";
  password: string = "";
  password2: string = "";

  auth: AuthService = new AuthService();

  error400 = false;
  error401 = false;
  passwordError = false;

  async signup(){

    if (this.password != this.password2){
      this.passwordError = true;
    }

    else {

      let status = await this.auth.signup(
          {username: this.username, password: this.password},
          this.$route.params.uuid
      );

      if (status == 401){
        this.error401 = true;
      } else if (status == 400){
        this.error400 = true;
      }
      else {
        this.auth.login({username: this.username, password: this.password});
        this.$router.push("/");
      }

    }

  }

}
</script>

<style lang="less">
.inputs {
  padding: 25px;
}

.block {
  background-image: url("~@/assets/bg.jpg");
  background-size: cover;
  height: 100vh;
  padding-left: 25%;
  padding-right: 25%;

}

</style>
