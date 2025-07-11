<template>
  <v-card variant="outlined" class="mb-4">
    <v-card-title class="d-flex justify-space-between align-center">
      <div>
        <v-icon color="primary" class="mr-2">mdi-door</v-icon>
        {{ room.room_number }}
      </div>
      <v-chip :color="utilizationColor" size="small">
        {{ room.students?.length || 0 }}/{{ room.room_capacity || 0 }}
      </v-chip>
    </v-card-title>
    
    <v-card-subtitle>
      {{ room.room_building }} - {{ room.room_floor }}
    </v-card-subtitle>
    
    <v-card-text>
      <!-- Utilization Progress -->
      <v-progress-linear
        :model-value="utilizationPercentage"
        :color="utilizationColor"
        height="8"
        rounded
        class="mb-3"
      />
      
      <!-- Students List -->
      <div class="text-subtitle-2 mb-2">Assigned Students:</div>
      
      <div v-if="!room.students || room.students.length === 0" class="text-center text-medium-emphasis py-4">
        No students assigned
      </div>
      
      <v-data-table
        v-else
        :headers="headers"
        :items="room.students"
        :items-per-page="5"
        density="compact"
        class="elevation-0"
      >
        <template #item.className="{ item }">
          <v-chip size="x-small" :color="getClassColor(item.className)">
            {{ item.className }}
          </v-chip>
        </template>
        
        <template #item.language="{ item }">
          <v-chip 
            v-if="item.language" 
            size="x-small" 
            :color="getLanguageColor(item.language)"
            variant="outlined"
          >
            {{ item.language }}
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  room: {
    type: Object,
    required: true
  }
})

const headers = [
  { title: 'Roll Number', key: 'rollNumber', sortable: true },
  { title: 'Student Name', key: 'studentName', sortable: true },
  { title: 'Class', key: 'className', sortable: true },
  { title: 'Language', key: 'language', sortable: true }
]

const utilizationPercentage = computed(() => {
  if (!props.room?.students || !props.room?.room_capacity) return 0
  return Math.round((props.room.students.length / props.room.room_capacity) * 100)
})

const utilizationColor = computed(() => {
  const percentage = utilizationPercentage.value
  if (percentage >= 90) return 'error'
  if (percentage >= 70) return 'warning'
  if (percentage >= 50) return 'success'
  return 'info'
})

const getClassColor = (className) => {
  // Generate consistent colors for classes
  const colors = ['primary', 'secondary', 'success', 'warning', 'error', 'info']
  const hash = className.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0)
  return colors[Math.abs(hash) % colors.length]
}

const getLanguageColor = (language) => {
  // Generate consistent colors for languages
  const languageColors = {
    'HINDI': 'orange',
    'ENGLISH': 'blue',
    'TAMIL': 'green',
    'SANSKRIT': 'purple',
    'TELUGU': 'teal',
    'KANNADA': 'indigo',
    'MALAYALAM': 'pink'
  }
  return languageColors[language?.toUpperCase()] || 'grey'
}
</script>
