import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import Home from '../views/Home.vue';
import Player from '../views/Player.vue';
import Creator from "../views/Creator.vue";
import tests from "@/router/routes/tests";

import About from "@/views/About.vue";

import {AuthService} from "@/services/auth.service";
import auth from "@/router/routes/auth";

let auth_service = new AuthService();

Vue.use(VueRouter);

export function redirectIfNotAuthentication(to: any, from: any, next: Function) {
  if (!auth_service.isAuthenticated()){
    next({'name': 'login'});
  } else {
    next();
  }
}

const routes: RouteConfig[] = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/player',
    name: 'player',
    component: Player
  },
  {
    path: '/creator/:id',
    name: 'creator',
    component: Creator,
    beforeEnter: redirectIfNotAuthentication
  },
  {
    path: '/about',
    name: 'about',
    component: About
  },
  ...tests,
  ...auth


];

const router = new VueRouter({
  routes,
});

export default router;
