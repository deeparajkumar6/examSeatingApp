<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-card-title class="text-center pa-6">
            <div class="text-h4 font-weight-bold">Login</div>
            <div class="text-subtitle-1 text-grey">Exam Seating System</div>
          </v-card-title>
          
          <v-card-text>
            <v-form ref="form" v-model="valid" @submit.prevent="handleLogin">
              <v-text-field
                v-model="credentials.username"
                label="Username"
                variant="outlined"
                prepend-inner-icon="mdi-account"
                :rules="[rules.required]"
                required
              />
              
              <v-text-field
                v-model="credentials.password"
                label="Password"
                :type="showPassword ? 'text' : 'password'"
                variant="outlined"
                prepend-inner-icon="mdi-lock"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="showPassword = !showPassword"
                :rules="[rules.required]"
                required
              />
              
              <v-btn
                type="submit"
                color="primary"
                size="large"
                :loading="loading"
                :disabled="!valid"
                block
                class="mt-4"
              >
                Login
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'

const router = useRouter()
const authStore = useAuthStore()
const appStore = useAppStore()

const form = ref(null)
const valid = ref(false)
const loading = ref(false)
const showPassword = ref(false)

const credentials = ref({
  username: '',
  password: ''
})

const rules = {
  required: (value) => !!value || 'This field is required'
}

const handleLogin = async () => {
  try {
    loading.value = true
    await authStore.login(credentials.value)
    appStore.showSuccess('Login successful')
    router.push('/')
  } catch (error) {
    appStore.showError('Invalid username or password')
  } finally {
    loading.value = false
  }
}
</script>