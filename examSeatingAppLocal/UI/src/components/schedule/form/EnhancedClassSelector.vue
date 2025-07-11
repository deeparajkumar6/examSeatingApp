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
              v-for="classId in modelValue"
              :key="classId"
              closable
              color="primary"
              variant="tonal"
              @click:close="removeClass(classId)"
            >
              <v-icon start icon="mdi-school" />
              {{ getClassDisplayName(classId) }}
              <template #append>
                <span class="text-caption ml-1">
                  ({{ getStudentCount(classId) }})
                </span>
              </template>
            </v-chip>
          </div>

          <!-- Summary Information -->
          <v-alert type="info" variant="tonal" density="compact">
            <div class="d-flex justify-space-between align-center">
              <span>
                <strong>Total Students:</strong> {{ totalStudents }}
              </span>
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
        </div>
      </v-card-text>

      <v-card-actions>
        <!-- Selection Dialog Button -->
        <SelectionDialog
          :model-value="modelValue"
          :items="classes"
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
const totalStudents = computed(() => {
  if (!props.classes || !Array.isArray(props.classes)) return 0
  return props.modelValue.reduce((total, classId) => {
    const cls = props.classes.find(c => c.id === classId)
    return total + (cls ? (cls.students?.length || 0) : 0)
  }, 0)
})

// Helper methods
const getClassDisplayName = (classId) => {
  if (!props.classes || !Array.isArray(props.classes)) return ''
  const cls = props.classes.find(c => c.id === classId)
  if (!cls) return ''
  const shiftText = cls.shift ? ` - Shift ${cls.shift}` : ''
  return `${cls.className}${shiftText}`
}

const getStudentCount = (classId) => {
  if (!props.classes || !Array.isArray(props.classes)) return 0
  const cls = props.classes.find(c => c.id === classId)
  return cls ? (cls.students?.length || 0) : 0
}

// Selection methods
const removeClass = (classId) => {
  const newSelection = props.modelValue.filter(id => id !== classId)
  emit('update:modelValue', newSelection)
}

const clearAllClasses = () => {
  emit('update:modelValue', [])
}

const selectAllClasses = () => {
  const allClassIds = props.classes.map(cls => cls.id)
  emit('update:modelValue', allClassIds)
}

const selectByShift = (shift) => {
  const shiftClasses = props.classes
    .filter(cls => cls.shift === shift)
    .map(cls => cls.id)
  emit('update:modelValue', shiftClasses)
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
