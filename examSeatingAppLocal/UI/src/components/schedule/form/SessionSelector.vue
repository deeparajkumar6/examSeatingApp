<template>
  <v-select
    :model-value="modelValue"
    label="Session"
    prepend-icon="mdi-clock-outline"
    :items="sessionOptions"
    item-title="title"
    item-value="value"
    :rules="[rules.required]"
    @update:model-value="$emit('update:modelValue', $event)"
  />
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

defineEmits(['update:modelValue'])

const sessionOptions = [
  { title: 'Forenoon (FN)', value: 'FN' },
  { title: 'Afternoon (AN)', value: 'AN' }
]

const rules = {
  required: (value) => !!value || 'Session is required'
}
</script>
