<template>
  <v-card-text>
    <!-- Search Field -->
    <v-text-field
      v-model="search"
      label="Search classes..."
      prepend-inner-icon="mdi-magnify"
      variant="outlined"
      density="compact"
      clearable
      class="mb-4"
    />
    
    <v-data-table 
      :headers="headers" 
      :items="classes"
      :loading="loading"
      :search="search"
      item-key="id"
    >
      <template #item.shift="{ item }">
        <v-chip 
          v-if="item.shift" 
          size="small" 
          color="primary" 
          variant="outlined"
        >
          {{ item.shift }}
        </v-chip>
        <span v-else class="text-grey">-</span>
      </template>
      
      <template #item.studentCount="{ item }">
        {{ item.students?.length || 0 }}
      </template>
      
      <template #item.actions="{ item }">
        <ClassActions 
          @edit="$emit('edit-class', item)"
          @delete="$emit('delete-class', item.id)"
        />
      </template>
    </v-data-table>
  </v-card-text>
</template>

<script setup>
import { ref } from 'vue'
import ClassActions from './ClassActions.vue'

defineProps({
  classes: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['edit-class', 'delete-class'])

// Search functionality
const search = ref('')

const headers = [
  { title: 'Class Name', key: 'className', sortable: true },
  { title: 'Shift', key: 'shift', sortable: true },
  { title: 'Student Count', key: 'studentCount', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false }
]
</script>
