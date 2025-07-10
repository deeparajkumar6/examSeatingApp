<template>
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
</script>
