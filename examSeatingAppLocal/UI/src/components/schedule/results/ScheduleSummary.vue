<template>
  <div>
    <!-- Main Statistics -->
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card variant="outlined">
          <v-card-text class="text-center">
            <v-icon size="32" color="primary" class="mb-2">
              mdi-account-group
            </v-icon>
            <div class="text-h5 font-weight-bold">{{ totalStudents }}</div>
            <div class="text-caption">Total Students</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="3">
        <v-card variant="outlined">
          <v-card-text class="text-center">
            <v-icon size="32" color="success" class="mb-2">
              mdi-door
            </v-icon>
            <div class="text-h5 font-weight-bold">{{ totalRooms }}</div>
            <div class="text-caption">Rooms Used</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="3">
        <v-card variant="outlined">
          <v-card-text class="text-center">
            <v-icon size="32" color="warning" class="mb-2">
              mdi-percent
            </v-icon>
            <div class="text-h5 font-weight-bold">{{ utilizationRate }}%</div>
            <div class="text-caption">Room Utilization</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="3">
        <v-card variant="outlined">
          <v-card-text class="text-center">
            <v-icon size="32" color="info" class="mb-2">
              mdi-school
            </v-icon>
            <div class="text-h5 font-weight-bold">{{ totalClasses }}</div>
            <div class="text-caption">Classes Scheduled</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Language Summary -->
    <v-row v-if="languageSummary && Object.keys(languageSummary).length > 0" class="mt-4">
      <v-col cols="12">
        <v-card variant="outlined">
          <v-card-title class="d-flex align-center">
            <v-icon color="primary" class="mr-2">mdi-translate</v-icon>
            Language Distribution
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col 
                v-for="(count, language) in languageSummary" 
                :key="language"
                cols="12" sm="6" md="4" lg="3"
              >
                <div class="d-flex align-center justify-space-between pa-2 rounded" 
                     :style="{ backgroundColor: getLanguageColor(language) + '20' }">
                  <div class="d-flex align-center">
                    <v-chip 
                      size="small" 
                      :color="getLanguageColor(language)"
                      class="mr-2"
                    >
                      {{ language }}
                    </v-chip>
                  </div>
                  <div class="text-h6 font-weight-bold">{{ count }}</div>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  schedule: {
    type: Object,
    required: true
  }
})

const totalStudents = computed(() => {
  if (!props.schedule?.room_assignments) return 0
  return props.schedule.room_assignments.reduce(
    (total, room) => total + (room.students?.length || 0), 0
  )
})

const totalRooms = computed(() => {
  if (!props.schedule?.room_assignments) return 0
  return props.schedule.room_assignments.length
})

const totalCapacity = computed(() => {
  if (!props.schedule?.room_assignments) return 0
  return props.schedule.room_assignments.reduce(
    (total, room) => total + (room.room_capacity || 0), 0
  )
})

const utilizationRate = computed(() => {
  if (totalCapacity.value === 0) return 0
  return Math.round((totalStudents.value / totalCapacity.value) * 100)
})

const totalClasses = computed(() => {
  if (!props.schedule?.room_assignments) return 0
  const classes = new Set()
  props.schedule.room_assignments.forEach(room => {
    if (room.students) {
      room.students.forEach(student => {
        if (student.className) {
          classes.add(student.className)
        }
      })
    }
  })
  return classes.size
})

const languageSummary = computed(() => {
  // First try to get language summary from API response
  if (props.schedule?.language_summary) {
    // Aggregate language counts across all rooms
    const totalLanguages = {}
    Object.values(props.schedule.language_summary).forEach(roomLanguages => {
      Object.entries(roomLanguages).forEach(([language, count]) => {
        totalLanguages[language] = (totalLanguages[language] || 0) + count
      })
    })
    return totalLanguages
  }
  
  // Fallback: calculate from student data
  if (!props.schedule?.room_assignments) return {}
  const languages = {}
  props.schedule.room_assignments.forEach(room => {
    if (room.students) {
      room.students.forEach(student => {
        if (student.language) {
          languages[student.language] = (languages[student.language] || 0) + 1
        }
      })
    }
  })
  return languages
})

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
