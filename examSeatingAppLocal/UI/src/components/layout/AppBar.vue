<template>
  <v-app-bar color="primary" dark>
    <v-app-bar-nav-icon @click="$emit('toggle-drawer')" />
    <v-toolbar-title>{{ appTitle }}</v-toolbar-title>
  </v-app-bar>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'

defineEmits(['toggle-drawer'])

const appStore = useAppStore()
const appTitle = computed(() => appStore.title)
</script>
