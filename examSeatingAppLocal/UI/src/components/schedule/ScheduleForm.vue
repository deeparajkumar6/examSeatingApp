<template>
  <v-card-text>
    <v-form ref="form" v-model="valid">
      <v-row>
        <!-- Date Selection -->
        <v-col cols="12" md="6">
          <DatePicker v-model="formData.date" />
        </v-col>
        
        <!-- Session Selection -->
        <v-col cols="12" md="6">
          <SessionSelector v-model="formData.session" />
        </v-col>
      </v-row>
      
      <!-- Examination Title -->
      <v-row>
        <v-col cols="12">
          <v-text-field
            v-model="formData.title"
            label="Examination Title"
            variant="outlined"
            prepend-inner-icon="mdi-format-title"
            :rules="[rules.required]"
            required
          />
        </v-col>
      </v-row>
      
      
      <!-- Class Selection -->
      <v-row>
        <v-col cols="12">
          <div v-if="!classes || classes.length === 0">
            <v-alert type="info" variant="tonal">
              <v-icon left>mdi-information</v-icon>
              No classes available. Please add classes first.
            </v-alert>
          </div>
          <EnhancedClassSelector 
            v-else
            ref="classSelector"
            v-model="formData.classes"
            :classes="classes"
          />
        </v-col>
      </v-row>
      
      <!-- Room Selection -->
      <v-row>
        <v-col cols="12">
          <div v-if="!examRooms || examRooms.length === 0">
            <v-alert type="info" variant="tonal">
              <v-icon left>mdi-information</v-icon>
              No exam rooms available. Please add exam rooms first.
            </v-alert>
          </div>
          <EnhancedRoomSelector 
            v-else
            ref="roomSelector"
            v-model="formData.exam_rooms"
            :exam-rooms="examRooms"
            :total-students="totalStudents"
          />
        </v-col>
      </v-row>
      
      <!-- Capacity Analysis -->
      <v-row v-if="formData.classes.length > 0 && formData.exam_rooms.length > 0">
        <v-col cols="12">
          <CapacityAnalysis 
            :selected-classes="selectedClassesData"
            :selected-rooms="selectedRoomsData"
            :total-students="totalStudents"
            :total-capacity="totalCapacity"
          />
        </v-col>
      </v-row>
      
      <!-- Options -->
      <v-row>
        <v-col cols="12">
          <ScheduleOptions v-model="formData.split" />
        </v-col>
      </v-row>
      
      <!-- Submit Button -->
      <v-row>
        <v-col cols="12" class="text-center">
          <v-btn
            color="primary"
            size="large"
            :loading="loading"
            :disabled="!valid || !canSubmit"
            @click="handleSubmit"
          >
            <v-icon left>mdi-calendar-plus</v-icon>
            Generate Schedule
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-card-text>
</template>

<script setup>
import { ref, computed, watch, toRefs } from 'vue'
import DatePicker from './form/DatePicker.vue'
import SessionSelector from './form/SessionSelector.vue'
import EnhancedClassSelector from './form/EnhancedClassSelector.vue'
import EnhancedRoomSelector from './form/EnhancedRoomSelector.vue'
import ScheduleOptions from './form/ScheduleOptions.vue'
import CapacityAnalysis from './form/CapacityAnalysis.vue'
import { 
  expandClassesByLanguage, 
  convertExpandedSelectionsToOriginal,
  getExpandedSelectionSummary 
} from '@/utils/classUtils'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  classes: {
    type: Array,
    default: () => []
  },
  examRooms: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'submit'])

// Destructure props for template access
const { classes, examRooms, loading } = toRefs(props)

const form = ref(null)
const classSelector = ref(null)
const roomSelector = ref(null)
const valid = ref(false)

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const rules = {
  required: (value) => !!value || 'This field is required'
}

// Computed properties for analysis
const expandedClasses = computed(() => {
  return expandClassesByLanguage(props.classes)
})

const selectedExpandedClasses = computed(() => {
  return expandedClasses.value.filter(cls => formData.value.classes.includes(cls.id))
})

const selectedClassesData = computed(() => {
  // Check if we have expanded IDs or original class IDs
  const hasExpandedIds = formData.value.classes.some(id => 
    expandedClasses.value.some(cls => cls.id === id)
  )
  
  if (hasExpandedIds) {
    // Use existing logic for expanded classes
    const selectionSummary = getExpandedSelectionSummary(formData.value.classes, expandedClasses.value)
    return selectionSummary.details.map(detail => ({
      id: `${detail.className}_${detail.shift}_${detail.language}`,
      className: detail.className,
      shift: detail.shift,
      language: detail.language,
      students: Array.from({ length: detail.studentCount }, (_, i) => ({
        id: i,
        name: `Student ${i + 1}`,
        language: detail.language
      }))
    }))
  } else {
    // Handle original class IDs (Group by Class mode)
    return formData.value.classes.map(classId => {
      const originalClass = props.classes.find(cls => cls.id === classId)
      if (originalClass) {
        const studentCount = originalClass.students?.length || 0
        return {
          id: `${originalClass.className}_${originalClass.shift}_all`,
          className: originalClass.className,
          shift: originalClass.shift,
          language: 'All Languages',
          students: Array.from({ length: studentCount }, (_, i) => ({
            id: i,
            name: `Student ${i + 1}`,
            language: 'Mixed'
          }))
        }
      }
      return null
    }).filter(Boolean)
  }
})

const selectedRoomsData = computed(() => {
  if (!props.examRooms || !Array.isArray(props.examRooms)) return []
  return props.examRooms.filter(room => formData.value.exam_rooms.includes(room.id))
})

const totalStudents = computed(() => {
  // Check if we have expanded IDs or original class IDs
  const hasExpandedIds = formData.value.classes.some(id => 
    expandedClasses.value.some(cls => cls.id === id)
  )
  
  if (hasExpandedIds) {
    // Use existing logic for expanded classes
    const summary = getExpandedSelectionSummary(formData.value.classes, expandedClasses.value)
    return summary.totalStudents
  } else {
    // Handle original class IDs (Group by Class mode)
    return formData.value.classes.reduce((total, classId) => {
      const originalClass = props.classes.find(cls => cls.id === classId)
      return total + (originalClass?.students?.length || 0)
    }, 0)
  }
})

const totalCapacity = computed(() => {
  return selectedRoomsData.value.reduce((total, room) => {
    return total + (room.roomCapacity || 0)
  }, 0)
})

const canSubmit = computed(() => {
  return formData.value.date &&
         formData.value.title &&
         formData.value.session &&
         formData.value.classes.length > 0 &&
         formData.value.exam_rooms.length > 0 &&
         classes.value && classes.value.length > 0 &&
         examRooms.value && examRooms.value.length > 0
})

const handleSubmit = async () => {
  // Validate form
  const { valid: isFormValid } = await form.value.validate()
  
  // Validate selectors
  const isClassSelectorValid = classSelector.value?.validate() ?? true
  const isRoomSelectorValid = roomSelector.value?.validate() ?? true
  
  if (isFormValid && isClassSelectorValid && isRoomSelectorValid && canSubmit.value) {
    // Check if we have expanded IDs or original class IDs
    const hasExpandedIds = formData.value.classes.some(id => 
      expandedClasses.value.some(cls => cls.id === id)
    )
    
    let submitData
    
    if (hasExpandedIds) {
      // Convert expanded class selections to original format for API
      const convertedSelections = convertExpandedSelectionsToOriginal(
        formData.value.classes, 
        expandedClasses.value
      )
      
      submitData = {
        date: formData.value.date,
        title: formData.value.title,
        session: formData.value.session,
        classes: convertedSelections.classSelections, // Original class IDs for API
        exam_rooms: formData.value.exam_rooms,
        split: formData.value.split,
        language_selections: convertedSelections.languageSelections // Language selections for API
      }
    } else {
      // Handle original class IDs (Group by Class mode)
      submitData = {
        date: formData.value.date,
        title: formData.value.title,
        session: formData.value.session,
        classes: formData.value.classes, // Already original class IDs
        exam_rooms: formData.value.exam_rooms,
        split: formData.value.split
        // No language_selections for Group by Class mode
      }
    }
    
    console.log('Submitting data:', submitData)
    emit('submit', submitData)
  }
}

// Watch for changes and emit updates
watch(formData, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })
</script>
