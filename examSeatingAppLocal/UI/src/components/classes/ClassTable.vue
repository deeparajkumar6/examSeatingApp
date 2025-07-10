<template>
  <v-card-text>
    <v-data-table 
      :headers="headers" 
      :items="classes"
      :loading="loading"
      item-key="id"
    >
      <template #item.studentCount="{ item }">
        {{ item.students.length }}
      </template>
      
      <template #item.rollNumbers="{ item }">
        <StudentChips :students="item.students" />
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
import StudentChips from './StudentChips.vue'
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

const headers = [
  { title: 'Class Name', key: 'className', sortable: true },
  { title: 'Student Count', key: 'studentCount', sortable: true },
  { title: 'Roll Numbers', key: 'rollNumbers', sortable: false },
  { title: 'Actions', key: 'actions', sortable: false }
]
</script>
