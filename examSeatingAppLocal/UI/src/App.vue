<template>
  <v-app>
    <AppNavigation v-if="isAuthenticated" />
    <AppMain :class="{ 'no-nav': !isAuthenticated }" />
    
    <!-- Global Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
      location="top right"
    >
      {{ snackbar.message }}
      <template #actions>
        <v-btn
          variant="text"
          @click="hideSnackbar"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'
import AppNavigation from '@/components/layout/AppNavigation.vue'
import AppMain from '@/components/layout/AppMain.vue'

const appStore = useAppStore()
const authStore = useAuthStore()

const snackbar = computed(() => appStore.snackbar)
const isAuthenticated = computed(() => authStore.isAuthenticated)
const hideSnackbar = () => appStore.hideSnackbar()

// Initialize auth on app start
onMounted(() => {
  authStore.initializeAuth()
})
</script>

<style scoped>
.no-nav {
  margin-left: 0 !important;
}
</style>
