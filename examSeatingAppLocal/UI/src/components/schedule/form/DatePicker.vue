<template>
  <v-menu v-model="menu" :close-on-content-click="false">
    <template #activator="{ props }">
      <v-text-field
        :model-value="displayDate"
        label="Select Exam Date"
        variant="outlined"
        prepend-inner-icon="mdi-calendar"
        readonly
        v-bind="props"
        :rules="[rules.required]"
      />
    </template>
    <v-date-picker
      :model-value="dateValue"
      :min="minDate"
      @update:model-value="updateDate"
    />
  </v-menu>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

const menu = ref(false)

// Get today's date for minimum date restriction
const minDate = computed(() => {
  const today = new Date()
  return new Date(today.getFullYear(), today.getMonth(), today.getDate())
})

const dateValue = computed(() => {
  if (!props.modelValue) return null
  // Parse the date string directly to avoid timezone issues
  const [year, month, day] = props.modelValue.split('-').map(Number)
  return new Date(year, month - 1, day)
})

const displayDate = computed(() => {
  if (!props.modelValue) return ''
  // Parse and format the date to avoid timezone issues
  const [year, month, day] = props.modelValue.split('-').map(Number)
  const date = new Date(year, month - 1, day)
  return date.toLocaleDateString()
})

const rules = {
  required: (value) => !!value || 'Exam date is required'
}

const updateDate = (date) => {
  if (date) {
    // Format date as YYYY-MM-DD without timezone conversion
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const formattedDate = `${year}-${month}-${day}`
    emit('update:modelValue', formattedDate)
  }
  menu.value = false
}
</script>
