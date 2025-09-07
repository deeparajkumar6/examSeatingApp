<template>
  <v-card variant="outlined" class="mb-4">
    <v-card-title class="d-flex align-center">
      <v-icon icon="mdi-chart-pie" class="mr-2" />
      Capacity Analysis
      <v-spacer />
      <v-chip
        :color="capacityStatus.color"
        size="small"
        variant="tonal"
      >
        {{ capacityStatus.text }}
      </v-chip>
    </v-card-title>

    <v-card-text>
      <v-row>
        <!-- Students Summary -->
        <v-col cols="12" md="4">
          <v-card variant="tonal" color="primary">
            <v-card-text class="text-center">
              <v-icon icon="mdi-account-group" size="32" class="mb-2" />
              <div class="text-h4 font-weight-bold">{{ totalStudents }}</div>
              <div class="text-caption">Total Students</div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Capacity Summary -->
        <v-col cols="12" md="4">
          <v-card variant="tonal" color="secondary">
            <v-card-text class="text-center">
              <v-icon icon="mdi-seat" size="32" class="mb-2" />
              <div class="text-h4 font-weight-bold">{{ totalCapacity }}</div>
              <div class="text-caption">Total Capacity</div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Utilization -->
        <v-col cols="12" md="4">
          <v-card variant="tonal" :color="utilizationColor">
            <v-card-text class="text-center">
              <v-icon icon="mdi-percent" size="32" class="mb-2" />
              <div class="text-h4 font-weight-bold">{{ utilizationPercentage }}%</div>
              <div class="text-caption">Utilization</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Progress Bar -->
      <v-row class="mt-2">
        <v-col cols="12">
          <div class="text-subtitle-2 mb-2">Capacity Utilization</div>
          <v-progress-linear
            :model-value="utilizationPercentage"
            :color="utilizationColor"
            height="20"
            rounded
          >
            <template #default="{ value }">
              <strong>{{ Math.ceil(value) }}%</strong>
            </template>
          </v-progress-linear>
        </v-col>
      </v-row>

      <!-- Detailed Breakdown -->
      <v-expansion-panels v-if="selectedClasses.length > 0 || selectedRooms.length > 0" class="mt-4">
        <v-expansion-panel>
          <v-expansion-panel-title>
            <v-icon icon="mdi-chart-bar" class="mr-2" />
            Detailed Breakdown
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-row>
              <!-- Classes Breakdown -->
              <v-col cols="12" md="6" v-if="selectedClasses.length > 0">
                <div class="text-subtitle-1 mb-2">
                  <v-icon icon="mdi-school" class="mr-1" />
                  Classes ({{ selectedClasses.length }})
                </div>
                <v-table density="compact">
                  <thead>
                    <tr>
                      <th>Class</th>
                      <th>Students</th>
                      <th>%</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="cls in selectedClasses" :key="cls.id">
                      <td>
                        {{ cls.className }}
                        <span v-if="cls.shift" class="text-caption text-grey">
                          - Shift {{ cls.shift }}
                        </span>
                      </td>
                      <td>{{ cls.students?.length || 0 }}</td>
                      <td>
                        <v-chip size="x-small" color="primary" variant="tonal">
                          {{ getClassPercentage(cls) }}%
                        </v-chip>
                      </td>
                    </tr>
                  </tbody>
                </v-table>
              </v-col>

              <!-- Rooms Breakdown -->
              <v-col cols="12" md="6" v-if="selectedRooms.length > 0">
                <div class="text-subtitle-1 mb-2">
                  <v-icon icon="mdi-door" class="mr-1" />
                  Rooms ({{ selectedRooms.length }})
                </div>
                <v-table density="compact">
                  <thead>
                    <tr>
                      <th>Room</th>
                      <th>Capacity</th>
                      <th>%</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="room in selectedRooms" :key="room.id">
                      <td>
                        {{ room.roomNumber }}
                        <div class="text-caption text-grey">
                          {{ room.roomBuilding }}
                        </div>
                      </td>
                      <td>{{ room.roomCapacity }}</td>
                      <td>
                        <v-chip 
                          size="x-small" 
                          :color="getRoomCapacityColor(room.roomCapacity)" 
                          variant="tonal"
                        >
                          {{ getRoomPercentage(room) }}%
                        </v-chip>
                      </td>
                    </tr>
                  </tbody>
                </v-table>
              </v-col>
            </v-row>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>

      <!-- Recommendations -->
      <v-alert
        v-if="recommendations.length > 0"
        type="info"
        variant="tonal"
        class="mt-4"
      >
        <div class="text-subtitle-2 mb-2">
          <v-icon icon="mdi-lightbulb" class="mr-1" />
          Recommendations
        </div>
        <ul class="ml-4">
          <li v-for="(recommendation, index) in recommendations" :key="index">
            {{ recommendation }}
          </li>
        </ul>
      </v-alert>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  selectedClasses: {
    type: Array,
    default: () => []
  },
  selectedRooms: {
    type: Array,
    default: () => []
  },
  totalStudents: {
    type: Number,
    default: 0
  },
  totalCapacity: {
    type: Number,
    default: 0
  }
})

// Computed properties
const utilizationPercentage = computed(() => {
  if (props.totalCapacity === 0) return 0
  return Math.round((props.totalStudents / props.totalCapacity) * 100)
})

const utilizationColor = computed(() => {
  const percentage = utilizationPercentage.value
  if (percentage <= 60) return 'success'
  if (percentage <= 80) return 'warning'
  if (percentage <= 100) return 'orange'
  return 'error'
})

const capacityStatus = computed(() => {
  const percentage = utilizationPercentage.value
  if (percentage === 0) {
    return { color: 'grey', text: 'No Data' }
  } else if (percentage <= 60) {
    return { color: 'success', text: 'Excellent' }
  } else if (percentage <= 80) {
    return { color: 'warning', text: 'Good' }
  } else if (percentage <= 100) {
    return { color: 'orange', text: 'Tight' }
  } else {
    return { color: 'error', text: 'Overcapacity' }
  }
})

const recommendations = computed(() => {
  const recs = []
  const percentage = utilizationPercentage.value
  
  if (percentage > 100) {
    recs.push('Add more exam rooms or reduce the number of students')
  } else if (percentage > 90) {
    recs.push('Consider adding buffer rooms for optimal seating arrangement')
  } else if (percentage < 50) {
    recs.push('You may have excess capacity - consider optimizing room selection')
  }
  
  if (props.selectedRooms.length > 0) {
    const smallRooms = props.selectedRooms.filter(room => room.roomCapacity < 30)
    if (smallRooms.length > 0) {
      recs.push(`Consider replacing ${smallRooms.length} small room(s) with larger ones for better efficiency`)
    }
  }
  
  return recs
})

// Helper methods
const getClassPercentage = (cls) => {
  if (props.totalStudents === 0) return 0
  const studentCount = cls.students?.length || 0
  return Math.round((studentCount / props.totalStudents) * 100)
}

const getRoomPercentage = (room) => {
  if (props.totalCapacity === 0) return 0
  return Math.round((room.roomCapacity / props.totalCapacity) * 100)
}

const getRoomCapacityColor = (capacity) => {
  if (capacity >= 50) return 'success'
  if (capacity >= 30) return 'warning'
  return 'error'
}
</script>

<style scoped>
.v-progress-linear {
  border-radius: 10px;
}
</style>
