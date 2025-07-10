<template>
  <v-select
    :model-value="modelValue"
    chips
    item-title="roomDisplayName"
    item-value="id"
    :items="roomOptions"
    label="Select Exam Rooms"
    multiple
    prepend-icon="mdi-door"
    :rules="[rules.required]"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <template #item="{ props, item }">
      <v-list-item v-bind="props">
        <v-list-item-title>{{ item.raw.roomNumber }}</v-list-item-title>
        <v-list-item-subtitle>
          Capacity: {{ item.raw.roomCapacity }} | 
          Floor: {{ item.raw.roomFloor }} | 
          Building: {{ item.raw.roomBuilding }}
        </v-list-item-subtitle>
      </v-list-item>
    </template>
    
    <template #chip="{ props, item }">
      <v-chip v-bind="props" :color="getCapacityColor(item.value)">
        {{ getRoomNumber(item.value) }}
        <template #append>
          <span class="text-caption ml-1">
            ({{ getRoomCapacity(item.value) }})
          </span>
        </template>
      </v-chip>
    </template>
  </v-select>
  
  <div v-if="modelValue.length > 0" class="mt-2">
    <v-alert type="info" variant="tonal">
      <strong>Total Capacity:</strong> {{ totalCapacity }} seats across {{ modelValue.length }} rooms
    </v-alert>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  examRooms: {
    type: Array,
    default: () => []
  }
})

defineEmits(['update:modelValue'])

const roomOptions = computed(() => 
  props.examRooms.map(room => ({
    ...room,
    roomDisplayName: `${room.roomNumber} - ${room.roomBuilding} (${room.roomCapacity} seats)`
  }))
)

const totalCapacity = computed(() => {
  return props.modelValue.reduce((total, roomId) => {
    const room = props.examRooms.find(r => r.id === roomId)
    return total + (room ? room.roomCapacity : 0)
  }, 0)
})

const rules = {
  required: (value) => value.length > 0 || 'At least one exam room must be selected'
}

const getRoomNumber = (roomId) => {
  const room = props.examRooms.find(r => r.id === roomId)
  return room ? room.roomNumber : ''
}

const getRoomCapacity = (roomId) => {
  const room = props.examRooms.find(r => r.id === roomId)
  return room ? room.roomCapacity : 0
}

const getCapacityColor = (roomId) => {
  const capacity = getRoomCapacity(roomId)
  if (capacity >= 50) return 'success'
  if (capacity >= 30) return 'warning'
  return 'error'
}
</script>
