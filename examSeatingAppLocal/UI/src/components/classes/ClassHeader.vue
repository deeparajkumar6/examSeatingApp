<template>
  <div class="d-flex justify-space-between align-center pa-3">
    <v-card-title>Class Management</v-card-title>
    <div class="d-flex gap-2">
      <v-btn color="info" variant="outlined" @click="$emit('download-template')" :loading="downloadingTemplate">
        <v-icon left>mdi-download</v-icon>
        Download Template
      </v-btn>
      <v-btn color="success" variant="outlined" @click="$emit('import-excel')">
        <v-icon left>mdi-file-excel</v-icon>
        Import from Excel
      </v-btn>
      <v-btn color="primary" @click="$emit('add-class')">
        <v-icon left>mdi-plus</v-icon>
        Add Class
      </v-btn>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const downloadingTemplate = ref(false)

defineEmits(['add-class', 'import-excel', 'download-template'])
defineExpose({ downloadingTemplate })
</script>
