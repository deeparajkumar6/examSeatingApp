<template>
  <v-menu v-model="menu" :close-on-content-click="false">
    <template #activator="{ props }">
      <v-text-field
        :model-value="displayDate"
        label="Select Exam Date"
        prepend-icon="mdi-calendar"
        readonly
        v-bind="props"
        :rules="[rules.required]"
      />
    </template>
    <v-date-picker
      :model-value="dateValue"
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

const dateValue = computed(() => {
  return props.modelValue ? new Date(props.modelValue) : null
})

const displayDate = computed(() => {
  if (!props.modelValue) return ''
  return new Date(props.modelValue).toLocaleDateString()
})

const rules = {
  required: (value) => !!value || 'Exam date is required'
}

const updateDate = (date) => {
  if (date) {
    const formattedDate = date.toISOString().split('T')[0]
    emit('update:modelValue', formattedDate)
  }
  menu.value = false
}
</script>
