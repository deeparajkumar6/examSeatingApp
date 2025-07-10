<template>
  <div>
    <AppBar @toggle-drawer="toggleDrawer" />
    <NavigationDrawer v-model="drawer" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppBar from './AppBar.vue'
import NavigationDrawer from './NavigationDrawer.vue'

const drawer = ref(true)

const toggleDrawer = () => {
  drawer.value = !drawer.value
}
</script>
