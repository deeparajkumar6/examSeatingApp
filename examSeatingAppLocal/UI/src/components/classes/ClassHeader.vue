<template>
  <div class="d-flex justify-space-between align-center pa-3">
    <v-card-title>Class Management</v-card-title>
    <div class="d-flex gap-2">
      <v-btn color="primary" @click="$emit('add-class')">
        <v-icon left>mdi-plus</v-icon>
        Add Class
      </v-btn>
    </div>
  </div>
</template>

<script setup>
defineEmits(['add-class'])
</script>
