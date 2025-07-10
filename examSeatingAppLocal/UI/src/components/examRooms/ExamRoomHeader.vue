<template>
  <div class="d-flex justify-space-between align-center pa-3">
    <v-card-title>Exam Room Management</v-card-title>
    <div class="d-flex gap-2">
      <v-btn color="primary" @click="$emit('add-room')">
        <v-icon left>mdi-plus</v-icon>
        Add Room
      </v-btn>
    </div>
  </div>
</template>

<script setup>
defineEmits(['add-room'])
</script>
