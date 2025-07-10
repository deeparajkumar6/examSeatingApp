<template>
  <v-card variant="outlined">
    <v-card-title class="text-subtitle-1">
      <v-icon left>mdi-cog</v-icon>
      Scheduling Options
    </v-card-title>
    
    <v-card-text>
      <v-switch
        :model-value="modelValue"
        label="Split Students into Multiple Rooms"
        color="primary"
        @update:model-value="$emit('update:modelValue', $event)"
      />
      
      <v-alert
        :type="modelValue ? 'info' : 'warning'"
        variant="tonal"
        class="mt-3"
      >
        <div v-if="modelValue">
          <strong>Split Mode:</strong> Students from the same class will be distributed across multiple rooms to prevent cheating.
        </div>
        <div v-else>
          <strong>Keep Together:</strong> Students from the same class will be kept in the same room when possible.
        </div>
      </v-alert>
    </v-card-text>
  </v-card>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

defineEmits(['update:modelValue'])
</script>
