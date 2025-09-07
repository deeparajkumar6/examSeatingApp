<template>
  <v-app-bar color="primary" dark>
    <v-app-bar-nav-icon @click="$emit('toggle-drawer')" />
    <v-toolbar-title>{{ appTitle }}</v-toolbar-title>
    <v-spacer />
    <v-btn
      v-if="isAuthenticated"
      icon="mdi-logout"
      @click="handleLogout"
    />
  </v-app-bar>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'

defineEmits(['toggle-drawer'])

const router = useRouter()
const appStore = useAppStore()
const authStore = useAuthStore()

const appTitle = computed(() => appStore.title)
const isAuthenticated = computed(() => authStore.isAuthenticated)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
