<template>
  <v-card>
    <ScheduleResultsHeader 
      :schedule="schedule"
      @export-summary-pdf="$emit('export-summary-pdf')"
      @export-detailed-pdf="$emit('export-detailed-pdf')"
      @clear="$emit('clear')"
    />
    
    <v-card-text>
      <!-- Schedule Summary -->
      <ScheduleSummary :schedule="schedule" />
      
      <!-- Room Assignments -->
      <div class="mt-6">
        <h3 class="text-h6 mb-4">Room Assignments</h3>
        <div v-if="!schedule.room_assignments || schedule.room_assignments.length === 0">
          <v-alert type="info" variant="tonal">
            No room assignments available.
          </v-alert>
        </div>
        <v-row v-else>
          <v-col
            v-for="room in schedule.room_assignments"
            :key="room.room_id"
            cols="12"
            lg="6"
          >
            <RoomAssignmentCard :room="room" />
          </v-col>
        </v-row>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import ScheduleResultsHeader from './results/ScheduleResultsHeader.vue'
import ScheduleSummary from './results/ScheduleSummary.vue'
import RoomAssignmentCard from './results/RoomAssignmentCard.vue'

defineProps({
  schedule: {
    type: Object,
    required: true
  }
})

defineEmits(['export-summary-pdf', 'export-detailed-pdf', 'clear'])
</script>
