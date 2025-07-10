<template>
  <v-container>
    <!-- Stats Cards -->
    <ExamRoomStats :exam-rooms="examRooms" />
    
    <!-- Main Table Card -->
    <v-card>
      <ExamRoomHeader @add-room="openAddDialog" />
      <ExamRoomTable 
        :exam-rooms="examRooms"
        :loading="loading"
        @edit-room="openEditDialog"
        @delete-room="handleDeleteRoom"
      />
    </v-card>

    <!-- Dialogs -->
    <ExamRoomDialog
      v-model="roomDialog.show"
      :room-data="roomDialog.data"
      :edit-mode="roomDialog.editMode"
      @save="handleSaveRoom"
    />
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useExamRoomsStore } from '@/stores/examRooms'
import ExamRoomStats from './ExamRoomStats.vue'
import ExamRoomHeader from './ExamRoomHeader.vue'
import ExamRoomTable from './ExamRoomTable.vue'
import ExamRoomDialog from './ExamRoomDialog.vue'

const examRoomsStore = useExamRoomsStore()

// Reactive data
const roomDialog = ref({
  show: false,
  data: null,
  editMode: false
})

// Computed
const examRooms = computed(() => examRoomsStore.examRooms)
const loading = computed(() => examRoomsStore.loading)

// Methods
const openAddDialog = () => {
  roomDialog.value = {
    show: true,
    data: null,
    editMode: false
  }
}

const openEditDialog = (roomData) => {
  roomDialog.value = {
    show: true,
    data: { ...roomData },
    editMode: true
  }
}

const handleSaveRoom = async (roomData) => {
  try {
    if (roomDialog.value.editMode) {
      await examRoomsStore.updateExamRoom(roomData.id, roomData)
    } else {
      await examRoomsStore.createExamRoom(roomData)
    }
    roomDialog.value.show = false
  } catch (error) {
    // Error handling is done in the store
  }
}

const handleDeleteRoom = async (roomId) => {
  if (confirm('Are you sure you want to delete this exam room?')) {
    await examRoomsStore.deleteExamRoom(roomId)
  }
}

// Lifecycle
onMounted(() => {
  examRoomsStore.fetchExamRooms()
})
</script>
