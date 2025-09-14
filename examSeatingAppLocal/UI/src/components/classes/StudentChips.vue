<template>
  <v-chip-group>
    <v-tooltip
      v-for="student in displayStudents"
      :key="student.id"
      location="top"
    >
      <template #activator="{ props: tooltipProps }">
        <v-chip
          v-bind="tooltipProps"
          size="small"
          :color="student.language ? 'primary' : 'default'"
          :variant="student.language ? 'outlined' : 'flat'"
        >
          {{ student.rollNumber || student.studentName || `Student ${student.id}` }}
        </v-chip>
      </template>
      <div>
        <div><strong>{{ student.studentName || 'No name' }}</strong></div>
        <div v-if="student.language">Language: {{ student.language }}</div>
        <div v-if="student.dateOfBirth">DOB: {{ formatDate(student.dateOfBirth) }}</div>
      </div>
    </v-tooltip>
    
    <v-chip
      v-if="hasMoreStudents"
      size="small"
      variant="outlined"
    >
      +{{ remainingCount }} more
    </v-chip>
  </v-chip-group>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  students: {
    type: Array,
    default: () => []
  },
  maxDisplay: {
    type: Number,
    default: 5
  }
})

const displayStudents = computed(() => 
  props.students.slice(0, props.maxDisplay)
)

const hasMoreStudents = computed(() => 
  props.students.length > props.maxDisplay
)

const remainingCount = computed(() => 
  props.students.length - props.maxDisplay
)

const formatDate = (dateString) => {
  if (!dateString) return ''
  try {
    return new Date(dateString).toLocaleDateString()
  } catch {
    return dateString
  }
}
</script>
