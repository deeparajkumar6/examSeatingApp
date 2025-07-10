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
          <ClassSelector 
            v-else
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
          <RoomSelector 
            v-else
            v-model="formData.exam_rooms"
            :exam-rooms="examRooms"
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
import ClassSelector from './form/ClassSelector.vue'
import RoomSelector from './form/RoomSelector.vue'
import ScheduleOptions from './form/ScheduleOptions.vue'

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
const valid = ref(false)

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const rules = {
  required: (value) => !!value || 'This field is required'
}

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
  const { valid: isValid } = await form.value.validate()
  if (isValid && canSubmit.value) {
    emit('submit', { ...formData.value })
  }
}

// Watch for changes and emit updates
watch(formData, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })
</script>
