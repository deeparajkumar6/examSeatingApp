<template>
  <div>
    <!-- Current Selection Display -->
    <v-card variant="outlined" class="mb-4">
      <v-card-title class="d-flex align-center">
        <v-icon icon="mdi-door" class="mr-2" />
        Selected Exam Rooms
        <v-spacer />
        <v-chip
          :color="modelValue.length > 0 ? 'success' : 'default'"
          size="small"
        >
          {{ modelValue.length }} selected
        </v-chip>
      </v-card-title>

      <v-card-text>
        <div v-if="modelValue.length === 0" class="text-center py-4">
          <v-icon icon="mdi-door-open" size="48" color="grey-lighten-1" />
          <p class="text-grey mt-2">No exam rooms selected</p>
        </div>

        <div v-else>
          <!-- Selected Rooms Chips -->
          <div class="d-flex flex-wrap gap-2 mb-3">
            <v-chip
              v-for="roomId in modelValue"
              :key="roomId"
              closable
              :color="getCapacityColor(roomId)"
              variant="tonal"
              @click:close="removeRoom(roomId)"
            >
              <v-icon start icon="mdi-door" />
              {{ getRoomNumber(roomId) }}
              <template #append>
                <span class="text-caption ml-1">
                  ({{ getRoomCapacity(roomId) }})
                </span>
              </template>
            </v-chip>
          </div>

          <!-- Summary Information -->
          <v-row>
            <v-col cols="12" md="6">
              <v-alert type="info" variant="tonal" density="compact">
                <strong>Total Capacity:</strong> {{ totalCapacity }} seats
              </v-alert>
            </v-col>
            <v-col cols="12" md="6">
              <v-alert 
                :type="capacityStatus.type" 
                variant="tonal" 
                density="compact"
              >
                <strong>Status:</strong> {{ capacityStatus.message }}
              </v-alert>
            </v-col>
          </v-row>

          <!-- Room Distribution -->
          <div class="mt-3">
            <v-expansion-panels variant="accordion">
              <v-expansion-panel>
                <v-expansion-panel-title>
                  <v-icon icon="mdi-chart-bar" class="mr-2" />
                  Room Details
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <v-simple-table density="compact">
                    <thead>
                      <tr>
                        <th>Room</th>
                        <th>Building</th>
                        <th>Floor</th>
                        <th>Capacity</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="roomId in modelValue" :key="roomId">
                        <td>{{ getRoomNumber(roomId) }}</td>
                        <td>{{ getRoomBuilding(roomId) }}</td>
                        <td>{{ getRoomFloor(roomId) }}</td>
                        <td>
                          <v-chip 
                            :color="getCapacityColor(roomId)" 
                            size="small"
                          >
                            {{ getRoomCapacity(roomId) }}
                          </v-chip>
                        </td>
                      </tr>
                    </tbody>
                  </v-simple-table>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </div>
        </div>
      </v-card-text>

      <v-card-actions>
        <!-- Selection Dialog Button -->
        <SelectionDialog
          :model-value="modelValue"
          :items="examRooms"
          type="room"
          @update:model-value="$emit('update:modelValue', $event)"
        />
        
        <v-spacer />
        
        <!-- Quick Actions -->
        <v-menu>
          <template #activator="{ props }">
            <v-btn
              v-bind="props"
              variant="text"
              prepend-icon="mdi-lightning-bolt"
              :disabled="examRooms.length === 0"
            >
              Quick Select
            </v-btn>
          </template>
          
          <v-list>
            <v-list-item @click="selectAllRooms">
              <v-list-item-title>Select All Rooms</v-list-item-title>
              <template #prepend>
                <v-icon icon="mdi-select-all" />
              </template>
            </v-list-item>
            
            <v-list-item @click="selectByBuilding">
              <v-list-item-title>Select by Building</v-list-item-title>
              <template #prepend>
                <v-icon icon="mdi-office-building" />
              </template>
            </v-list-item>
            
            <v-list-item @click="optimizeSelection">
              <v-list-item-title>Auto-Optimize Selection</v-list-item-title>
              <template #prepend>
                <v-icon icon="mdi-auto-fix" />
              </template>
            </v-list-item>
          </v-list>
        </v-menu>

        <v-btn
          variant="text"
          color="error"
          prepend-icon="mdi-delete"
          :disabled="modelValue.length === 0"
          @click="clearAllRooms"
        >
          Clear All
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Building Selection Dialog -->
    <v-dialog v-model="buildingDialog" max-width="400px">
      <v-card>
        <v-card-title>Select Building</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item
              v-for="building in availableBuildings"
              :key="building"
              @click="selectRoomsByBuilding(building)"
            >
              <v-list-item-title>{{ building }}</v-list-item-title>
              <template #append>
                <v-chip size="small">
                  {{ getRoomCountByBuilding(building) }} rooms
                </v-chip>
              </template>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="buildingDialog = false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Validation Message -->
    <v-alert
      v-if="showValidationError"
      type="error"
      variant="tonal"
      density="compact"
      class="mb-2"
    >
      At least one exam room must be selected
    </v-alert>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import SelectionDialog from './SelectionDialog.vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  examRooms: {
    type: Array,
    default: () => []
  },
  totalStudents: {
    type: Number,
    default: 0
  },
  required: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue'])

const showValidationError = ref(false)
const buildingDialog = ref(false)

// Computed properties
const totalCapacity = computed(() => {
  if (!props.examRooms || !Array.isArray(props.examRooms)) return 0
  return props.modelValue.reduce((total, roomId) => {
    const room = props.examRooms.find(r => r.id === roomId)
    return total + (room ? room.roomCapacity : 0)
  }, 0)
})

const capacityStatus = computed(() => {
  if (props.totalStudents === 0) {
    return { type: 'info', message: 'No students to accommodate' }
  }
  
  const ratio = totalCapacity.value / props.totalStudents
  if (ratio >= 1.5) {
    return { type: 'success', message: 'Excellent capacity' }
  } else if (ratio >= 1.2) {
    return { type: 'success', message: 'Good capacity' }
  } else if (ratio >= 1.0) {
    return { type: 'warning', message: 'Adequate capacity' }
  } else {
    return { type: 'error', message: 'Insufficient capacity' }
  }
})

const availableBuildings = computed(() => {
  if (!props.examRooms || !Array.isArray(props.examRooms)) return []
  const buildings = [...new Set(props.examRooms.map(room => room.roomBuilding))]
  return buildings.sort()
})

// Helper methods
const getRoomNumber = (roomId) => {
  if (!props.examRooms || !Array.isArray(props.examRooms)) return ''
  const room = props.examRooms.find(r => r.id === roomId)
  return room ? room.roomNumber : ''
}

const getRoomCapacity = (roomId) => {
  if (!props.examRooms || !Array.isArray(props.examRooms)) return 0
  const room = props.examRooms.find(r => r.id === roomId)
  return room ? room.roomCapacity : 0
}

const getRoomBuilding = (roomId) => {
  if (!props.examRooms || !Array.isArray(props.examRooms)) return ''
  const room = props.examRooms.find(r => r.id === roomId)
  return room ? room.roomBuilding : ''
}

const getRoomFloor = (roomId) => {
  if (!props.examRooms || !Array.isArray(props.examRooms)) return ''
  const room = props.examRooms.find(r => r.id === roomId)
  return room ? room.roomFloor : ''
}

const getCapacityColor = (roomId) => {
  const capacity = getRoomCapacity(roomId)
  if (capacity >= 50) return 'success'
  if (capacity >= 30) return 'warning'
  return 'error'
}

const getRoomCountByBuilding = (building) => {
  return props.examRooms.filter(room => room.roomBuilding === building).length
}

// Selection methods
const removeRoom = (roomId) => {
  const newSelection = props.modelValue.filter(id => id !== roomId)
  emit('update:modelValue', newSelection)
}

const clearAllRooms = () => {
  emit('update:modelValue', [])
}

const selectAllRooms = () => {
  const allRoomIds = props.examRooms.map(room => room.id)
  emit('update:modelValue', allRoomIds)
}

const selectByBuilding = () => {
  buildingDialog.value = true
}

const selectRoomsByBuilding = (building) => {
  const buildingRooms = props.examRooms
    .filter(room => room.roomBuilding === building)
    .map(room => room.id)
  emit('update:modelValue', buildingRooms)
  buildingDialog.value = false
}

const optimizeSelection = () => {
  if (props.totalStudents === 0) return
  
  // Sort rooms by capacity (largest first)
  const sortedRooms = [...props.examRooms].sort((a, b) => b.roomCapacity - a.roomCapacity)
  
  let selectedRooms = []
  let currentCapacity = 0
  const targetCapacity = Math.ceil(props.totalStudents * 1.2) // 20% buffer
  
  for (const room of sortedRooms) {
    if (currentCapacity >= targetCapacity) break
    selectedRooms.push(room.id)
    currentCapacity += room.roomCapacity
  }
  
  emit('update:modelValue', selectedRooms)
}

// Validation
const validate = () => {
  if (props.required && props.modelValue.length === 0) {
    showValidationError.value = true
    return false
  }
  showValidationError.value = false
  return true
}

// Expose validation method
defineExpose({
  validate
})
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
