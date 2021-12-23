<template>
<div class="mt-3 winners">

  <hr>

  <h1><b>Победители!</b></h1>
  <h2 v-for="(player, index) in winners">
    <b>{{index + 1}}. {{player.name}} - {{Math.ceil(player.score)}}</b>
  </h2>

  <hr>

  <b><i>Остальные</i></b>
  <div v-for="(player, index) in players">
      <p>
        <b>{{index + 4}}. {{player.name}} - {{Math.ceil(player.score)}}</b>
      </p>
      <hr>
  </div>

</div>
</template>

<script lang="ts">
import {Component, Vue, Prop} from "vue-property-decorator";
import {Player} from "@/services/interfaces";

@Component
export default class Winners extends Vue {
   @Prop(Array) winners!: Player[];
   @Prop(Array) players!: Player[];


}
</script>

<style scoped>
.winners {
  background: rgba(255,255,255,0.4);
  backdrop-filter: blur(10px);
}
</style>