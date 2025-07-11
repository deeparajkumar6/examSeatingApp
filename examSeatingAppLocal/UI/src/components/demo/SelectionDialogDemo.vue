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
              This demo showcases the enhanced class and room selection dialogs with language-based class expansion. 
              Classes are now split by language, allowing you to select specific language groups from each class.
            </p>
            
            <v-alert type="info" variant="tonal" class="mb-4">
              <v-icon icon="mdi-information" class="mr-2" />
              <strong>Language-Based Selection:</strong> Each class is expanded into separate selectable entries for each language. 
              For example, "I B.COM -CS - Shift I" becomes multiple options like "I B.COM -CS - Shift I - Hindi" and "I B.COM -CS - Shift I - English".
            </v-alert>

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
                  <v-card-title>Selected Class Groups</v-card-title>
                  <v-card-text>
                    <div v-if="selectedClasses.length === 0" class="text-grey">
                      No class groups selected
                    </div>
                    <div v-else>
                      <v-chip-group column>
                        <v-chip
                          v-for="expandedId in selectedClasses"
                          :key="expandedId"
                          color="primary"
                          variant="tonal"
                        >
                          {{ getExpandedClassName(expandedId) }}
                        </v-chip>
                      </v-chip-group>
                      <v-divider class="my-2" />
                      <div class="text-caption text-grey">
                        Total: {{ selectionSummary.totalStudents }} students from {{ selectionSummary.totalSelections }} language groups
                      </div>
                    </div>
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
import { 
  getClassDisplayName, 
  expandClassesByLanguage,
  getExpandedSelectionSummary 
} from '@/utils/classUtils'

// Reactive data
const selectedClasses = ref([])
const selectedRooms = ref([])
const mockClasses = ref([])
const mockRooms = ref([])

// Computed properties
const expandedClasses = computed(() => {
  return expandClassesByLanguage(mockClasses.value)
})

const selectedExpandedClasses = computed(() => {
  return expandedClasses.value.filter(cls => selectedClasses.value.includes(cls.id))
})

const selectedClassesData = computed(() => {
  return selectedExpandedClasses.value
})

const selectedRoomsData = computed(() => {
  return mockRooms.value.filter(room => selectedRooms.value.includes(room.id))
})

const totalStudents = computed(() => {
  return selectedExpandedClasses.value.reduce((total, cls) => {
    return total + (cls.students?.length || 0)
  }, 0)
})

const totalCapacity = computed(() => {
  return selectedRoomsData.value.reduce((total, room) => {
    return total + (room.roomCapacity || 0)
  }, 0)
})

const selectionSummary = computed(() => {
  return getExpandedSelectionSummary(selectedClasses.value, expandedClasses.value)
})

// Helper methods
const getExpandedClassName = (expandedId) => {
  const expandedClass = expandedClasses.value.find(c => c.id === expandedId)
  return expandedClass ? expandedClass.displayName : ''
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
      className: 'I B.COM -CS',
      shift: 'I',
      students: [
        ...Array.from({ length: 25 }, (_, i) => ({ 
          id: i + 1, 
          name: `Student ${i + 1}`, 
          language: 'Hindi' 
        })),
        ...Array.from({ length: 20 }, (_, i) => ({ 
          id: i + 26, 
          name: `Student ${i + 26}`, 
          language: 'English' 
        }))
      ]
    },
    {
      id: 2,
      className: 'I B.COM -CS',
      shift: 'II',
      students: [
        ...Array.from({ length: 30 }, (_, i) => ({ 
          id: i + 46, 
          name: `Student ${i + 46}`, 
          language: 'Hindi' 
        })),
        ...Array.from({ length: 8 }, (_, i) => ({ 
          id: i + 76, 
          name: `Student ${i + 76}`, 
          language: 'English' 
        }))
      ]
    },
    {
      id: 3,
      className: 'II B.COM -CS',
      shift: 'I',
      students: [
        ...Array.from({ length: 35 }, (_, i) => ({ 
          id: i + 84, 
          name: `Student ${i + 84}`, 
          language: 'English' 
        })),
        ...Array.from({ length: 17 }, (_, i) => ({ 
          id: i + 119, 
          name: `Student ${i + 119}`, 
          language: 'Hindi' 
        }))
      ]
    },
    {
      id: 4,
      className: 'I BCA',
      shift: null,
      students: Array.from({ length: 28 }, (_, i) => ({ 
        id: i + 136, 
        name: `Student ${i + 136}`, 
        language: 'English' 
      }))
    },
    {
      id: 5,
      className: 'II BCA',
      shift: 'I',
      students: [
        ...Array.from({ length: 20 }, (_, i) => ({ 
          id: i + 164, 
          name: `Student ${i + 164}`, 
          language: 'Hindi' 
        })),
        ...Array.from({ length: 15 }, (_, i) => ({ 
          id: i + 184, 
          name: `Student ${i + 184}`, 
          language: 'English' 
        })),
        ...Array.from({ length: 8 }, (_, i) => ({ 
          id: i + 199, 
          name: `Student ${i + 199}`, 
          language: 'Marathi' 
        }))
      ]
    },
    {
      id: 6,
      className: 'I B.SC Mathematics',
      shift: null,
      students: Array.from({ length: 29 }, (_, i) => ({ 
        id: i + 207, 
        name: `Student ${i + 207}`, 
        language: null // Some students without language preference
      }))
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
