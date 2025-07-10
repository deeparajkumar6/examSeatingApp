<template>
  <v-card variant="outlined" class="mb-3">
    <v-card-text class="pb-2">
      <div class="d-flex gap-3 align-center">
        <v-text-field
          v-model="studentData.rollNumber"
          label="Roll Number"
          density="compact"
          :rules="[rules.required]"
          @update:model-value="updateStudent"
        />
        
        <v-text-field
          v-model="studentData.studentName"
          label="Student Name"
          density="compact"
          @update:model-value="updateStudent"
        />
        
        <v-btn
          icon
          variant="flat"
          color="error"
          size="small"
          @click="$emit('remove')"
        >
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </div>
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
      studentName: ''
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
