<template>
  <v-container>
    <!-- Schedule Creation Form -->
    <v-card class="mb-6">
      <ScheduleHeader />
      <ScheduleForm 
        v-model="scheduleData"
        :classes="classes"
        :exam-rooms="examRooms"
        :loading="loading"
        @submit="handleCreateSchedule"
      />
    </v-card>

    <!-- Generated Schedule Display -->
    <ScheduleResults 
      v-if="generatedSchedule && generatedSchedule.room_assignments"
      :schedule="generatedSchedule"
      @export-summary-pdf="handleExportSummaryPdf"
      @export-detailed-pdf="handleExportDetailedPdf"
      @clear="handleClearSchedule"
    />
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useScheduleStore } from '@/stores/schedule'
import { useClassesStore } from '@/stores/classes'
import { useExamRoomsStore } from '@/stores/examRooms'
import ScheduleHeader from './ScheduleHeader.vue'
import ScheduleForm from './ScheduleForm.vue'
import ScheduleResults from './ScheduleResults.vue'

const scheduleStore = useScheduleStore()
const classesStore = useClassesStore()
const examRoomsStore = useExamRoomsStore()

// Reactive data
const scheduleData = ref({
  date: null,
  title: '',
  session: '',
  classes: [],
  exam_rooms: [],
  split: false
})

// Computed
const classes = computed(() => classesStore.classes)
const examRooms = computed(() => examRoomsStore.examRooms)
const loading = computed(() => scheduleStore.loading)
const generatedSchedule = computed(() => scheduleStore.currentSchedule)

// Methods
const handleCreateSchedule = async (formData) => {
  try {
    await scheduleStore.createSchedule(formData)
  } catch (error) {
    console.error('Failed to create schedule:', error)
    // Error handling is done in the store
  }
}

const handleExportSummaryPdf = async () => {
  await scheduleStore.exportSummaryPDF()
}

const handleExportDetailedPdf = async () => {
  await scheduleStore.exportDetailedPDF()
}

const handleClearSchedule = () => {
  scheduleStore.clearSchedule()
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    classesStore.fetchClasses(),
    examRoomsStore.fetchExamRooms()
  ])
})
</script>
