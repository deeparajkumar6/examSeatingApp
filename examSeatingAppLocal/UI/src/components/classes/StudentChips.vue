<template>
  <v-chip-group>
    <v-chip
      v-for="student in displayStudents"
      :key="student.id"
      size="small"
    >
      {{ student.rollNumber }}
    </v-chip>
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
</script>
