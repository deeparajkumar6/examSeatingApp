<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-icon icon="mdi-test-tube" class="mr-2" />
            Selection Dialog Demo
          </v-card-title>
          <v-card-text>
            <p class="text-body-1 mb-4">
              This demo showcases the enhanced class and room selection dialogs with search functionality and multi-select capabilities.
            </p>

            <!-- Mock Data Controls -->
            <v-row class="mb-4">
              <v-col cols="12" md="6">
                <v-btn
                  color="primary"
                  variant="outlined"
                  prepend-icon="mdi-database-plus"
                  @click="generateMockData"
                >
                  Generate Mock Data
                </v-btn>
              </v-col>
              <v-col cols="12" md="6">
                <v-btn
                  color="error"
                  variant="outlined"
                  prepend-icon="mdi-delete"
                  @click="clearMockData"
                >
                  Clear Data
                </v-btn>
              </v-col>
            </v-row>

            <v-divider class="mb-4" />

            <!-- Class Selection Demo -->
            <div class="mb-6">
              <h3 class="text-h6 mb-3">Class Selection</h3>
              <EnhancedClassSelector
                v-model="selectedClasses"
                :classes="mockClasses"
              />
            </div>

            <!-- Room Selection Demo -->
            <div class="mb-6">
              <h3 class="text-h6 mb-3">Room Selection</h3>
              <EnhancedRoomSelector
                v-model="selectedRooms"
                :exam-rooms="mockRooms"
                :total-students="totalStudents"
              />
            </div>

            <!-- Capacity Analysis -->
            <div v-if="selectedClasses.length > 0 && selectedRooms.length > 0">
              <h3 class="text-h6 mb-3">Capacity Analysis</h3>
              <CapacityAnalysis
                :selected-classes="selectedClassesData"
                :selected-rooms="selectedRoomsData"
                :total-students="totalStudents"
                :total-capacity="totalCapacity"
              />
            </div>

            <!-- Selection Summary -->
            <v-row class="mt-4">
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Selected Classes</v-card-title>
                  <v-card-text>
                    <div v-if="selectedClasses.length === 0" class="text-grey">
                      No classes selected
                    </div>
                    <v-chip-group v-else column>
                      <v-chip
                        v-for="classId in selectedClasses"
                        :key="classId"
                        color="primary"
                        variant="tonal"
                      >
                        {{ getClassName(classId) }}
                      </v-chip>
                    </v-chip-group>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-title>Selected Rooms</v-card-title>
                  <v-card-text>
                    <div v-if="selectedRooms.length === 0" class="text-grey">
                      No rooms selected
                    </div>
                    <v-chip-group v-else column>
                      <v-chip
                        v-for="roomId in selectedRooms"
                        :key="roomId"
                        color="secondary"
                        variant="tonal"
                      >
                        {{ getRoomName(roomId) }}
                      </v-chip>
                    </v-chip-group>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import EnhancedClassSelector from '../schedule/form/EnhancedClassSelector.vue'
import EnhancedRoomSelector from '../schedule/form/EnhancedRoomSelector.vue'
import CapacityAnalysis from '../schedule/form/CapacityAnalysis.vue'

// Reactive data
const selectedClasses = ref([])
const selectedRooms = ref([])
const mockClasses = ref([])
const mockRooms = ref([])

// Computed properties
const selectedClassesData = computed(() => {
  return mockClasses.value.filter(cls => selectedClasses.value.includes(cls.id))
})

const selectedRoomsData = computed(() => {
  return mockRooms.value.filter(room => selectedRooms.value.includes(room.id))
})

const totalStudents = computed(() => {
  return selectedClassesData.value.reduce((total, cls) => {
    return total + (cls.students?.length || 0)
  }, 0)
})

const totalCapacity = computed(() => {
  return selectedRoomsData.value.reduce((total, room) => {
    return total + (room.roomCapacity || 0)
  }, 0)
})

// Helper methods
const getClassName = (classId) => {
  const cls = mockClasses.value.find(c => c.id === classId)
  if (!cls) return ''
  const shiftText = cls.shift ? ` - Shift ${cls.shift}` : ''
  return `${cls.className}${shiftText}`
}

const getRoomName = (roomId) => {
  const room = mockRooms.value.find(r => r.id === roomId)
  return room ? room.roomNumber : ''
}

// Mock data generation
const generateMockData = () => {
  // Generate mock classes
  mockClasses.value = [
    {
      id: 1,
      className: 'Computer Science I',
      shift: 1,
      students: Array.from({ length: 45 }, (_, i) => ({ id: i + 1, name: `Student ${i + 1}` }))
    },
    {
      id: 2,
      className: 'Computer Science I',
      shift: 2,
      students: Array.from({ length: 38 }, (_, i) => ({ id: i + 46, name: `Student ${i + 46}` }))
    },
    {
      id: 3,
      className: 'Mathematics II',
      shift: 1,
      students: Array.from({ length: 52 }, (_, i) => ({ id: i + 84, name: `Student ${i + 84}` }))
    },
    {
      id: 4,
      className: 'Physics I',
      shift: null,
      students: Array.from({ length: 28 }, (_, i) => ({ id: i + 136, name: `Student ${i + 136}` }))
    },
    {
      id: 5,
      className: 'Chemistry I',
      shift: 1,
      students: Array.from({ length: 35 }, (_, i) => ({ id: i + 164, name: `Student ${i + 164}` }))
    },
    {
      id: 6,
      className: 'English Literature',
      shift: null,
      students: Array.from({ length: 42 }, (_, i) => ({ id: i + 199, name: `Student ${i + 199}` }))
    }
  ]

  // Generate mock rooms
  mockRooms.value = [
    {
      id: 1,
      roomNumber: 'A101',
      roomBuilding: 'Main Building',
      roomFloor: 1,
      roomCapacity: 60
    },
    {
      id: 2,
      roomNumber: 'A102',
      roomBuilding: 'Main Building',
      roomFloor: 1,
      roomCapacity: 45
    },
    {
      id: 3,
      roomNumber: 'B201',
      roomBuilding: 'Science Block',
      roomFloor: 2,
      roomCapacity: 80
    },
    {
      id: 4,
      roomNumber: 'B202',
      roomBuilding: 'Science Block',
      roomFloor: 2,
      roomCapacity: 50
    },
    {
      id: 5,
      roomNumber: 'C301',
      roomBuilding: 'Arts Block',
      roomFloor: 3,
      roomCapacity: 35
    },
    {
      id: 6,
      roomNumber: 'C302',
      roomBuilding: 'Arts Block',
      roomFloor: 3,
      roomCapacity: 40
    },
    {
      id: 7,
      roomNumber: 'D101',
      roomBuilding: 'Engineering Block',
      roomFloor: 1,
      roomCapacity: 100
    },
    {
      id: 8,
      roomNumber: 'D102',
      roomBuilding: 'Engineering Block',
      roomFloor: 1,
      roomCapacity: 75
    }
  ]
}

const clearMockData = () => {
  mockClasses.value = []
  mockRooms.value = []
  selectedClasses.value = []
  selectedRooms.value = []
}

// Initialize with some mock data
generateMockData()
</script>

<style scoped>
.v-chip-group {
  max-height: 200px;
  overflow-y: auto;
}
</style>
