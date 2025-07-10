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
        <v-list-item-title>{{ item.raw.className }}</v-list-item-title>
        <v-list-item-subtitle>
          {{ item.raw.students.length }} students
        </v-list-item-subtitle>
      </v-list-item>
    </template>
    
    <template #chip="{ props, item }">
      <v-chip v-bind="props">
        {{ getClassName(item.value) }}
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

const classOptions = computed(() => 
  props.classes.map(cls => ({
    ...cls,
    classDisplayName: `${cls.className} (${cls.students.length} students)`
  }))
)

const rules = {
  required: (value) => value.length > 0 || 'At least one class must be selected'
}

const getClassName = (classId) => {
  const cls = props.classes.find(c => c.id === classId)
  return cls ? cls.className : ''
}

const getStudentCount = (classId) => {
  const cls = props.classes.find(c => c.id === classId)
  return cls ? cls.students.length : 0
}
</script>
