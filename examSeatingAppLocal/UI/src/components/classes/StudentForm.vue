<template>
  <v-card variant="outlined" class="mb-3">
    <v-card-text class="pb-2">
      <v-row>
        <v-col cols="12" md="3">
          <v-text-field
            v-model="studentData.rollNumber"
            label="Roll Number"
            variant="outlined"
            density="compact"
            :rules="[rules.required]"
            required
            @update:model-value="updateStudent"
          />
        </v-col>
        
        <v-col cols="12" md="4">
          <v-text-field
            v-model="studentData.studentName"
            label="Student Name"
            variant="outlined"
            density="compact"
            @update:model-value="updateStudent"
          />
        </v-col>
        
        <v-col cols="12" md="2">
          <v-text-field
            v-model="studentData.language"
            label="Language"
            variant="outlined"
            density="compact"
            placeholder="Optional"
            @update:model-value="updateStudent"
          />
        </v-col>
        
        <v-col cols="12" md="2">
          <v-text-field
            v-model="studentData.dateOfBirth"
            label="Date of Birth"
            variant="outlined"
            density="compact"
            type="date"
            placeholder="YYYY-MM-DD"
            @update:model-value="updateStudent"
          />
        </v-col>
        
        <v-col cols="12" md="1" class="d-flex align-center">
          <v-btn
            icon
            variant="flat"
            color="error"
            size="small"
            @click="$emit('remove')"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      rollNumber: '',
      studentName: '',
      language: '',
      dateOfBirth: ''
    })
  }
})

const emit = defineEmits(['update:modelValue', 'remove'])

const studentData = ref({ ...props.modelValue })

const rules = {
  required: (value) => !!value || 'Roll number is required'
}

watch(() => props.modelValue, (newValue) => {
  studentData.value = { ...newValue }
}, { deep: true })

const updateStudent = () => {
  emit('update:modelValue', { ...studentData.value })
}
</script>
