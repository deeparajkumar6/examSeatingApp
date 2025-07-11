<template>
  <v-select
    :model-value="modelValue"
    chips
    item-title="classDisplayName"
    item-value="id"
    :items="classOptions"
    label="Select Classes"
    multiple
    prepend-icon="mdi-school"
    :rules="[rules.required]"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <template #item="{ props, item }">
      <v-list-item v-bind="props">
        <v-list-item-title>{{ item.raw.classDisplayName }}</v-list-item-title>
        <v-list-item-subtitle>
          {{ item.raw.students?.length || 0 }} students
        </v-list-item-subtitle>
      </v-list-item>
    </template>
    
    <template #chip="{ props, item }">
      <v-chip v-bind="props">
        {{ getClassDisplayName(item.value) }}
        <template #append>
          <span class="text-caption ml-1">
            ({{ getStudentCount(item.value) }})
          </span>
        </template>
      </v-chip>
    </template>
  </v-select>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  classes: {
    type: Array,
    default: () => []
  }
})

defineEmits(['update:modelValue'])

const classOptions = computed(() => {
  if (!props.classes || !Array.isArray(props.classes)) return []
  return props.classes.map(cls => {
    const shiftText = cls.shift ? ` - Shift ${cls.shift}` : ''
    const displayName = `${cls.className}${shiftText}`
    return {
      ...cls,
      classDisplayName: displayName
    }
  })
})

const rules = {
  required: (value) => value.length > 0 || 'At least one class must be selected'
}

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
</script>
