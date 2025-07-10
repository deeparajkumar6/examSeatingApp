<template>
  <v-app>
    <AppNavigation />
    <AppMain />
    
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
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import AppNavigation from '@/components/layout/AppNavigation.vue'
import AppMain from '@/components/layout/AppMain.vue'

const appStore = useAppStore()

const snackbar = computed(() => appStore.snackbar)
const hideSnackbar = () => appStore.hideSnackbar()
</script>

<style scoped>
/* Global app styles can be moved to separate style files */
</style>
