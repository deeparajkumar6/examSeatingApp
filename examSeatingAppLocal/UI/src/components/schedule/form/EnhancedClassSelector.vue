<template>
  <div>
    <!-- Current Selection Display -->
    <v-card variant="outlined" class="mb-4">
      <v-card-title class="d-flex align-center">
        <v-icon icon="mdi-school" class="mr-2" />
        Selected Classes
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
          <v-icon icon="mdi-school-outline" size="48" color="grey-lighten-1" />
          <p class="text-grey mt-2">No classes selected</p>
        </div>

        <div v-else>
          <!-- Selected Classes Chips -->
          <div class="d-flex flex-wrap gap-2 mb-3">
            <v-chip
              v-for="expandedId in modelValue"
              :key="expandedId"
              closable
              color="primary"
              variant="tonal"
              @click:close="removeClass(expandedId)"
            >
              <v-icon start icon="mdi-school" />
              {{ getExpandedClassDisplayName(expandedId) }}
              <template #append>
                <span class="text-caption ml-1">
                  ({{ getExpandedStudentCount(expandedId) }})
                </span>
              </template>
            </v-chip>
          </div>

          <!-- Summary Information -->
          <v-alert type="info" variant="tonal" density="compact">
            <div class="d-flex justify-space-between align-center">
              <div>
                <strong>Total Students:</strong> {{ selectionSummary.totalStudents }} •
                <strong>Languages:</strong> {{ selectionSummary.totalLanguages }} •
                <strong>Selections:</strong> {{ selectionSummary.totalSelections }}
              </div>
              <v-btn
                size="small"
                variant="text"
                color="error"
                prepend-icon="mdi-delete"
                @click="clearAllClasses"
              >
                Clear All
              </v-btn>
            </div>
          </v-alert>
          
          <!-- Detailed Selection Summary -->
          <v-expansion-panels variant="accordion" class="mt-2">
            <v-expansion-panel>
              <v-expansion-panel-title>
                <v-icon icon="mdi-format-list-bulleted" class="mr-2" />
                Selection Details
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                <v-table density="compact">
                  <thead>
                    <tr>
                      <th>Class</th>
                      <th>Language</th>
                      <th>Students</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="detail in selectionSummary.details" :key="`${detail.className}_${detail.shift}_${detail.language}`">
                      <td>{{ detail.className }}{{ detail.shift ? ` - Shift ${detail.shift}` : '' }}</td>
                      <td>
                        <v-chip 
                          size="x-small" 
                          :color="getLanguageColor(detail.language)"
                          variant="tonal"
                        >
                          {{ detail.language || 'No Language' }}
                        </v-chip>
                      </td>
                      <td>{{ detail.studentCount }}</td>
                    </tr>
                  </tbody>
                </v-table>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>
      </v-card-text>

      <v-card-actions>
        <!-- Selection Dialog Button -->
        <SelectionDialog
          :model-value="modelValue"
          :items="expandedClasses"
          type="class"
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
              :disabled="classes.length === 0"
            >
              Quick Select
            </v-btn>
          </template>
          
          <v-list>
            <v-list-item @click="selectAllClasses">
              <v-list-item-title>Select All Classes</v-list-item-title>
              <template #prepend>
                <v-icon icon="mdi-select-all" />
              </template>
            </v-list-item>
            
            <v-list-item @click="selectByShift(1)">
              <v-list-item-title>Select Shift 1 Only</v-list-item-title>
              <template #prepend>
                <v-icon icon="mdi-numeric-1-circle" />
              </template>
            </v-list-item>
            
            <v-list-item @click="selectByShift(2)">
              <v-list-item-title>Select Shift 2 Only</v-list-item-title>
              <template #prepend>
                <v-icon icon="mdi-numeric-2-circle" />
              </template>
            </v-list-item>
            
            <v-divider v-if="availableLanguages.length > 0" />
            
            <v-list-item 
              v-for="language in availableLanguages" 
              :key="language"
              @click="selectByLanguage(language)"
            >
              <v-list-item-title>Select {{ language }} Classes</v-list-item-title>
              <template #prepend>
                <v-icon icon="mdi-translate" />
              </template>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-card-actions>
    </v-card>

    <!-- Validation Message -->
    <v-alert
      v-if="showValidationError"
      type="error"
      variant="tonal"
      density="compact"
      class="mb-2"
    >
      At least one class must be selected
    </v-alert>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import SelectionDialog from './SelectionDialog.vue'
import { 
  getClassDisplayName, 
  getUniqueLanguages, 
  getClassLanguages,
  expandClassesByLanguage,
  getExpandedSelectionSummary
} from '@/utils/classUtils'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  classes: {
    type: Array,
    default: () => []
  },
  required: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue'])

const showValidationError = ref(false)

// Computed properties
const expandedClasses = computed(() => {
  return expandClassesByLanguage(props.classes)
})

const selectionSummary = computed(() => {
  // Check if we have expanded IDs or original class IDs
  const hasExpandedIds = props.modelValue.some(id => 
    expandedClasses.value.some(cls => cls.id === id)
  )
  
  if (hasExpandedIds) {
    // Use existing function for expanded classes
    return getExpandedSelectionSummary(props.modelValue, expandedClasses.value)
  } else {
    // Handle original class IDs (Group by Class mode)
    let totalStudents = 0
    let totalLanguages = new Set()
    const selectionDetails = []
    
    props.modelValue.forEach(classId => {
      const originalClass = props.classes.find(cls => cls.id === classId)
      if (originalClass) {
        const studentCount = originalClass.students?.length || 0
        totalStudents += studentCount
        
        // Collect languages from students
        if (originalClass.students) {
          originalClass.students.forEach(student => {
            if (student.language) {
              totalLanguages.add(student.language)
            }
          })
        }
        
        selectionDetails.push({
          className: originalClass.className,
          shift: originalClass.shift,
          language: 'All Languages',
          studentCount: studentCount,
          displayName: getClassDisplayName(originalClass)
        })
      }
    })
    
    return {
      totalStudents,
      totalLanguages: totalLanguages.size,
      totalClasses: props.modelValue.length,
      totalSelections: props.modelValue.length,
      languages: Array.from(totalLanguages).sort(),
      details: selectionDetails
    }
  }
})

const availableLanguages = computed(() => {
  return getUniqueLanguages(props.classes)
})

// Helper methods
const getExpandedClassDisplayName = (classId) => {
  // First try to find in expanded classes
  const expandedClass = expandedClasses.value.find(c => c.id === classId)
  if (expandedClass) {
    return expandedClass.displayName
  }
  
  // If not found, try original classes (Group by Class mode)
  const originalClass = props.classes.find(c => c.id === classId)
  return originalClass ? getClassDisplayName(originalClass) : ''
}

const getExpandedStudentCount = (classId) => {
  // First try to find in expanded classes
  const expandedClass = expandedClasses.value.find(c => c.id === classId)
  if (expandedClass) {
    return expandedClass.students.length
  }
  
  // If not found, try original classes (Group by Class mode)
  const originalClass = props.classes.find(c => c.id === classId)
  return originalClass ? (originalClass.students?.length || 0) : 0
}

const getLanguageColor = (language) => {
  const colors = {
    'Hindi': 'orange',
    'English': 'blue',
    'Marathi': 'green',
    'Tamil': 'purple',
    'Telugu': 'teal',
    'Gujarati': 'indigo',
    'Bengali': 'pink'
  }
  return colors[language] || 'grey'
}

// Selection methods
const removeClass = (expandedId) => {
  const newSelection = props.modelValue.filter(id => id !== expandedId)
  emit('update:modelValue', newSelection)
}

const clearAllClasses = () => {
  emit('update:modelValue', [])
}

const selectAllClasses = () => {
  const allExpandedIds = expandedClasses.value.map(cls => cls.id)
  emit('update:modelValue', allExpandedIds)
}

const selectByShift = (shift) => {
  const shiftClasses = expandedClasses.value
    .filter(cls => cls.shift === shift)
    .map(cls => cls.id)
  emit('update:modelValue', shiftClasses)
}

const selectByLanguage = (language) => {
  const languageClasses = expandedClasses.value
    .filter(cls => cls.language && cls.language.toLowerCase() === language.toLowerCase())
    .map(cls => cls.id)
  emit('update:modelValue', languageClasses)
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
