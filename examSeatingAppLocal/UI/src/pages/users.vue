<template>
  <v-container>
    <v-card>
      <v-card-title class="d-flex align-center">
        <v-icon class="mr-2">mdi-account-group</v-icon>
        User Management
        <v-spacer />
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="openAddDialog"
        >
          Add User
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="users"
          :loading="loading"
          class="elevation-1"
        >
          <template #item.created_at="{ item }">
            {{ formatDate(item.created_at) }}
          </template>
          
          <template #item.actions="{ item }">
            <v-btn
              icon="mdi-delete"
              size="small"
              color="error"
              variant="text"
              @click="confirmDelete(item)"
            />
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Add User Dialog -->
    <v-dialog v-model="dialog" max-width="500px" persistent>
      <v-card>
        <v-card-title>Add New User</v-card-title>
        
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="newUser.name"
              label="Full Name"
              variant="outlined"
              :rules="[rules.required]"
              required
            />
            
            <v-text-field
              v-model="newUser.username"
              label="Username"
              variant="outlined"
              :rules="[rules.required]"
              required
            />
            
            <v-text-field
              v-model="newUser.password"
              label="Password"
              type="password"
              variant="outlined"
              :rules="[rules.required, rules.minLength]"
              required
            />
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer />
          <v-btn @click="closeDialog">Cancel</v-btn>
          <v-btn
            color="primary"
            :disabled="!valid"
            @click="saveUser"
          >
            Create User
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUsersStore } from '@/stores/users'

const usersStore = useUsersStore()

const dialog = ref(false)
const form = ref(null)
const valid = ref(false)

const newUser = ref({
  name: '',
  username: '',
  password: ''
})

const headers = [
  { title: 'Name', key: 'name' },
  { title: 'Username', key: 'username' },
  { title: 'Created At', key: 'created_at' },
  { title: 'Actions', key: 'actions', sortable: false }
]

const rules = {
  required: (value) => !!value || 'This field is required',
  minLength: (value) => value.length >= 6 || 'Password must be at least 6 characters'
}

// Computed
const users = computed(() => usersStore.users)
const loading = computed(() => usersStore.loading)

// Methods
const openAddDialog = () => {
  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  newUser.value = { name: '', username: '', password: '' }
}

const saveUser = async () => {
  try {
    await usersStore.createUser(newUser.value)
    closeDialog()
  } catch (error) {
    // Error handling is done in the store
  }
}

const confirmDelete = (user) => {
  if (confirm(`Are you sure you want to delete user "${user.name}"?`)) {
    usersStore.deleteUser(user.id)
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

// Lifecycle
onMounted(() => {
  usersStore.fetchUsers()
})
</script>