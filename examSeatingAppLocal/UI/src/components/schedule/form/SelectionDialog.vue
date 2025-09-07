<template>
  <v-dialog v-model="dialog" max-width="800px" scrollable>
    <template #activator="{ props }">
      <v-btn
        v-bind="props"
        :color="buttonColor"
        variant="outlined"
        :prepend-icon="buttonIcon"
        class="mb-2"
      >
        {{ buttonText }}
      </v-btn>
    </template>

    <v-card>
      <v-card-title class="d-flex align-center">
        <v-icon :icon="dialogIcon" class="mr-2" />
        {{ dialogTitle }}
        <v-spacer />
        <v-btn
          icon="mdi-close"
          variant="text"
          @click="dialog = false"
        />
      </v-card-title>

      <v-divider />

      <!-- Search Bar and Filters -->
      <v-card-text class="pb-0">
        <v-row>
          <v-col cols="12" md="8">
            <v-text-field
              v-model="searchQuery"
              :placeholder="searchPlaceholder"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              clearable
              hide-details
            />
          </v-col>
          <v-col cols="12" md="4" class="d-flex align-center">
            <v-btn
              size="small"
              variant="outlined"
              color="primary"
              prepend-icon="mdi-select-all"
              :disabled="filteredItems.length === 0"
              @click="selectAllFiltered"
              block
            >
              Select All ({{ filteredItems.length }})
            </v-btn>
          </v-col>
        </v-row>
        
        <!-- Class-specific filters -->
        <div v-if="type === 'class'" class="mt-3">
          <v-row>
            <v-col cols="12" md="6">
              <v-select
                v-model="shiftFilter"
                label="Filter by Shift"
                :items="shiftOptions"
                variant="outlined"
                density="compact"
                clearable
                hide-details
              />
            </v-col>
            <v-col cols="12" md="6" class="d-flex align-center">
              <v-radio-group
                v-model="splitByLanguage"
                inline
                hide-details
                density="compact"
              >
                <v-radio
                  label="Group by Class"
                  :value="false"
                />
                <v-radio
                  label="Split by Language"
                  :value="true"
                />
              </v-radio-group>
            </v-col>
          </v-row>
        </div>
      </v-card-text>

      <!-- Selection Summary -->
      <v-card-text v-if="selectedItems.length > 0" class="py-2">
        <v-alert type="info" variant="tonal" density="compact">
          <div class="d-flex align-center justify-space-between">
            <span>{{ selectedItems.length }} {{ type }}(s) selected</span>
            <v-btn
              size="small"
              variant="text"
              color="error"
              prepend-icon="mdi-close"
              @click="clearSelection"
            >
              Clear All
            </v-btn>
          </div>
        </v-alert>
      </v-card-text>

      <!-- Items List -->
      <v-card-text style="max-height: 400px;">
        <v-list v-if="filteredItems.length > 0" density="compact">
          <template v-for="item in filteredItems" :key="item.id">
            <v-list-item
              :class="{ 'bg-primary-lighten-5': isSelected(item.id) }"
              @click="toggleSelection(item.id)"
            >
              <template #prepend>
                <v-checkbox-btn
                  :model-value="isSelected(item.id)"
                  color="primary"
                  @click.stop="toggleSelection(item.id)"
                />
              </template>

              <v-list-item-title>
                {{ getItemTitle(item) }}
              </v-list-item-title>

              <v-list-item-subtitle>
                {{ getItemSubtitle(item) }}
              </v-list-item-subtitle>

              <template #append>
                <v-chip
                  :color="getItemChipColor(item)"
                  size="small"
                  variant="tonal"
                >
                  {{ getItemChipText(item) }}
                </v-chip>
              </template>
            </v-list-item>
            <v-divider />
          </template>
        </v-list>

        <v-alert
          v-else-if="searchQuery && filteredItems.length === 0"
          type="info"
          variant="tonal"
          text="No items match your search criteria."
        />

        <v-alert
          v-else-if="items.length === 0"
          type="warning"
          variant="tonal"
          :text="`No ${type}s available. Please add ${type}s first.`"
        />
      </v-card-text>

      <v-divider />

      <!-- Actions -->
      <v-card-actions>
        <v-spacer />
        <v-btn
          variant="text"
          @click="dialog = false"
        >
          Cancel
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          :disabled="selectedItems.length === 0"
          @click="applySelection"
        >
          Apply Selection ({{ selectedItems.length }})
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { getClassDisplayName, getClassLanguages } from '@/utils/classUtils'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  items: {
    type: Array,
    default: () => []
  },
  type: {
    type: String,
    required: true,
    validator: (value) => ['class', 'room'].includes(value)
  }
})

const emit = defineEmits(['update:modelValue'])

// Dialog state
const dialog = ref(false)
const searchQuery = ref('')
const selectedItems = ref([...props.modelValue])
const shiftFilter = ref(null)
const splitByLanguage = ref(false) // Default to group by class

// Computed properties for dynamic content
const buttonColor = computed(() => props.type === 'class' ? 'primary' : 'secondary')
const buttonIcon = computed(() => props.type === 'class' ? 'mdi-school' : 'mdi-door')
const buttonText = computed(() => `Select ${props.type === 'class' ? 'Classes' : 'Exam Rooms'}`)
const dialogIcon = computed(() => props.type === 'class' ? 'mdi-school' : 'mdi-door')
const dialogTitle = computed(() => `Select ${props.type === 'class' ? 'Classes' : 'Exam Rooms'}`)
const searchPlaceholder = computed(() => `Search ${props.type === 'class' ? 'classes' : 'rooms'}...`)

// Shift options for filtering
const shiftOptions = computed(() => {
  if (props.type !== 'class') return []
  const shifts = new Set()
  props.items.forEach(item => {
    if (item.shift) {
      shifts.add(item.shift)
    }
  })
  return Array.from(shifts).sort().map(shift => ({
    title: `Shift ${shift}`,
    value: shift
  }))
})

// Items to display based on language splitting preference
const displayItems = computed(() => {
  if (props.type !== 'class') return props.items
  
  if (splitByLanguage.value) {
    // Use expanded classes (split by language)
    return props.items
  } else {
    // Group by original class, combine language data
    const groupedClasses = new Map()
    
    props.items.forEach(item => {
      const originalId = item.originalId || item.id
      
      if (groupedClasses.has(originalId)) {
        // Merge students from different language groups
        const existing = groupedClasses.get(originalId)
        existing.students = [...existing.students, ...item.students]
      } else {
        // Create new grouped entry
        groupedClasses.set(originalId, {
          ...item,
          id: originalId,
          originalId: originalId,
          displayName: getClassDisplayName(item),
          language: null, // No specific language for grouped view
          languageLabel: 'All Languages',
          students: [...item.students]
        })
      }
    })
    
    return Array.from(groupedClasses.values())
  }
})

// Filtered items based on search and shift filter
const filteredItems = computed(() => {
  let items = displayItems.value
  
  // Apply shift filter
  if (shiftFilter.value && props.type === 'class') {
    items = items.filter(item => item.shift === shiftFilter.value)
  }
  
  // Apply search filter
  if (!searchQuery.value) return items

  const query = searchQuery.value.toLowerCase()
  return items.filter(item => {
    if (props.type === 'class') {
      const className = item.className?.toLowerCase() || ''
      const shift = item.shift?.toString().toLowerCase() || ''
      const language = item.language?.toLowerCase() || ''
      const displayName = item.displayName?.toLowerCase() || ''
      return className.includes(query) || 
             shift.includes(query) || 
             language.includes(query) ||
             displayName.includes(query)
    } else {
      const roomNumber = item.roomNumber?.toLowerCase() || ''
      const building = item.roomBuilding?.toLowerCase() || ''
      const floor = item.roomFloor?.toString().toLowerCase() || ''
      return roomNumber.includes(query) || building.includes(query) || floor.includes(query)
    }
  })
})

// Item display methods
const getItemTitle = (item) => {
  if (props.type === 'class') {
    // For expanded classes, use the displayName which includes language
    return item.displayName || getClassDisplayName(item)
  } else {
    return item.roomNumber
  }
}

const getItemSubtitle = (item) => {
  if (props.type === 'class') {
    const studentCount = item.students?.length || 0
    let subtitle = `${studentCount} students`
    
    // For expanded classes, show the language info
    if (item.language) {
      subtitle += ` • ${item.language}`
    } else if (item.languageLabel) {
      subtitle += ` • ${item.languageLabel}`
    }
    
    return subtitle
  } else {
    return `${item.roomBuilding} - Floor ${item.roomFloor}`
  }
}

const getItemChipText = (item) => {
  if (props.type === 'class') {
    return `${item.students?.length || 0} students`
  } else {
    return `${item.roomCapacity} seats`
  }
}

const getItemChipColor = (item) => {
  if (props.type === 'class') {
    const studentCount = item.students?.length || 0
    if (studentCount >= 50) return 'success'
    if (studentCount >= 30) return 'warning'
    return 'info'
  } else {
    const capacity = item.roomCapacity || 0
    if (capacity >= 50) return 'success'
    if (capacity >= 30) return 'warning'
    return 'error'
  }
}

// Selection methods
const isSelected = (itemId) => {
  return selectedItems.value.includes(itemId)
}

const toggleSelection = (itemId) => {
  const index = selectedItems.value.indexOf(itemId)
  if (index > -1) {
    selectedItems.value.splice(index, 1)
  } else {
    selectedItems.value.push(itemId)
  }
}

const clearSelection = () => {
  selectedItems.value = []
}

const selectAllFiltered = () => {
  const filteredIds = filteredItems.value.map(item => item.id)
  selectedItems.value = [...new Set([...selectedItems.value, ...filteredIds])]
}

const applySelection = () => {
  emit('update:modelValue', [...selectedItems.value])
  dialog.value = false
}

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
  selectedItems.value = [...newValue]
}, { deep: true })

// Reset search when dialog closes
watch(dialog, (isOpen) => {
  if (!isOpen) {
    searchQuery.value = ''
    shiftFilter.value = null
  } else {
    // Sync selected items when dialog opens
    selectedItems.value = [...props.modelValue]
  }
})

// Watch for language splitting toggle changes
watch(splitByLanguage, () => {
  // Clear selection when switching between modes to avoid confusion
  selectedItems.value = []
})
</script>

<style scoped>
.v-list-item {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.v-list-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.08);
}

.bg-primary-lighten-5 {
  background-color: rgba(var(--v-theme-primary), 0.12);
}
</style>
