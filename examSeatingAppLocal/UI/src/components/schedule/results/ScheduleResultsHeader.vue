<template>
  <div class="d-flex justify-space-between align-center pa-4">
    <div>
      <v-card-title class="pa-0">
        <v-icon color="success" class="mr-2">
          mdi-check-circle
        </v-icon>
        Schedule Generated Successfully
      </v-card-title>
      <v-card-subtitle class="pa-0 mt-1">
        {{ schedule.title }} - {{ formatDate(schedule.date) }} ({{ schedule.session }})
      </v-card-subtitle>
    </div>
    
    <div class="d-flex gap-2">
      <v-btn
        color="primary"
        variant="outlined"
        @click="$emit('export-pdf')"
      >
        <v-icon left>mdi-file-pdf-box</v-icon>
        Export PDF
      </v-btn>
      
      <v-btn
        color="error"
        variant="outlined"
        @click="$emit('clear')"
      >
        <v-icon left>mdi-close</v-icon>
        Clear
      </v-btn>
    </div>
  </div>
</template>

<script setup>
defineProps({
  schedule: {
    type: Object,
    required: true
  }
})

defineEmits(['export-pdf', 'clear'])

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>
