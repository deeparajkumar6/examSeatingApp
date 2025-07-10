<template>
  <v-card-text>
    <v-data-table 
      :headers="headers" 
      :items="examRooms"
      :loading="loading"
      item-key="id"
    >
      <template #item.roomInfo="{ item }">
        <div>
          <div class="font-weight-medium">{{ item.roomNumber }}</div>
          <div class="text-caption text-medium-emphasis">
            {{ item.roomBuilding }} - {{ item.roomFloor }}
          </div>
        </div>
      </template>
      
      <template #item.roomCapacity="{ item }">
        <v-chip 
          :color="getCapacityColor(item.roomCapacity)"
          size="small"
        >
          {{ item.roomCapacity }} seats
        </v-chip>
      </template>
      
      <template #item.actions="{ item }">
        <ExamRoomActions 
          @edit="$emit('edit-room', item)"
          @delete="$emit('delete-room', item.id)"
        />
      </template>
    </v-data-table>
  </v-card-text>
</template>

<script setup>
import ExamRoomActions from './ExamRoomActions.vue'

defineProps({
  examRooms: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['edit-room', 'delete-room'])

const headers = [
  { title: 'Room Info', key: 'roomInfo', sortable: true },
  { title: 'Capacity', key: 'roomCapacity', sortable: true },
  { title: 'Floor', key: 'roomFloor', sortable: true },
  { title: 'Building', key: 'roomBuilding', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false }
]

const getCapacityColor = (capacity) => {
  if (capacity >= 50) return 'success'
  if (capacity >= 30) return 'warning'
  return 'error'
}
</script>
