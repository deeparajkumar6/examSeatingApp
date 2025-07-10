<template>
  <v-row class="mb-4">
    <v-col cols="12" sm="6" md="3">
      <v-card>
        <v-card-text class="text-center">
          <v-icon size="40" color="primary" class="mb-2">
            mdi-door
          </v-icon>
          <div class="text-h4 font-weight-bold">{{ roomCount }}</div>
          <div class="text-subtitle-1">Total Rooms</div>
        </v-card-text>
      </v-card>
    </v-col>
    
    <v-col cols="12" sm="6" md="3">
      <v-card>
        <v-card-text class="text-center">
          <v-icon size="40" color="success" class="mb-2">
            mdi-account-group
          </v-icon>
          <div class="text-h4 font-weight-bold">{{ totalCapacity }}</div>
          <div class="text-subtitle-1">Total Capacity</div>
        </v-card-text>
      </v-card>
    </v-col>
    
    <v-col cols="12" sm="6" md="3">
      <v-card>
        <v-card-text class="text-center">
          <v-icon size="40" color="warning" class="mb-2">
            mdi-calculator
          </v-icon>
          <div class="text-h4 font-weight-bold">{{ averageCapacity }}</div>
          <div class="text-subtitle-1">Avg Capacity</div>
        </v-card-text>
      </v-card>
    </v-col>
    
    <v-col cols="12" sm="6" md="3">
      <v-card>
        <v-card-text class="text-center">
          <v-icon size="40" color="info" class="mb-2">
            mdi-office-building
          </v-icon>
          <div class="text-h4 font-weight-bold">{{ buildingCount }}</div>
          <div class="text-subtitle-1">Buildings</div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  examRooms: {
    type: Array,
    default: () => []
  }
})

const roomCount = computed(() => props.examRooms.length)

const totalCapacity = computed(() => 
  props.examRooms.reduce((total, room) => total + room.roomCapacity, 0)
)

const averageCapacity = computed(() => {
  if (props.examRooms.length === 0) return 0
  return Math.round(totalCapacity.value / props.examRooms.length)
})

const buildingCount = computed(() => {
  const buildings = new Set(props.examRooms.map(room => room.roomBuilding))
  return buildings.size
})
</script>
