<template>
  <div class="d-flex gap-1">
    <v-btn 
      icon 
      variant="flat" 
      size="small"
      @click="$emit('edit')"
    >
      <v-icon>mdi-pencil</v-icon>
      <v-tooltip activator="parent" location="top">
        Edit Class
      </v-tooltip>
    </v-btn>
    
    <v-btn 
      icon 
      variant="flat" 
      size="small"
      color="error"
      @click="$emit('delete')"
    >
      <v-icon>mdi-delete</v-icon>
      <v-tooltip activator="parent" location="top">
        Delete Class
      </v-tooltip>
    </v-btn>
  </div>
</template>

<script setup>
defineEmits(['edit', 'delete'])
</script>
