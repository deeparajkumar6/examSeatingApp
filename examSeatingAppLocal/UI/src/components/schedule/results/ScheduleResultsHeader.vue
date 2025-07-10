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
      <!-- PDF Export Menu -->
      <v-menu>
        <template #activator="{ props }">
          <v-btn
            color="primary"
            variant="outlined"
            v-bind="props"
          >
            <v-icon left>mdi-file-pdf-box</v-icon>
            Export PDF
            <v-icon right>mdi-chevron-down</v-icon>
          </v-btn>
        </template>
        
        <v-list>
          <v-list-item @click="$emit('export-summary-pdf')">
            <template #prepend>
              <v-icon>mdi-file-document-outline</v-icon>
            </template>
            <v-list-item-title>Summary PDF</v-list-item-title>
            <v-list-item-subtitle>Room-wise class summary</v-list-item-subtitle>
          </v-list-item>
          
          <v-list-item @click="$emit('export-detailed-pdf')">
            <template #prepend>
              <v-icon>mdi-file-document-multiple</v-icon>
            </template>
            <v-list-item-title>Detailed PDF</v-list-item-title>
            <v-list-item-subtitle>Complete student lists</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-menu>
      
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

defineEmits(['export-summary-pdf', 'export-detailed-pdf', 'clear'])

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>
