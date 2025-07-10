<template>
  <v-list-item
    :to="item.to"
    :active-class="activeClass"
    class="nav-item"
  >
    <template #prepend>
      <v-icon :color="item.color || 'primary'">
        {{ item.icon }}
      </v-icon>
    </template>
    <v-list-item-title>{{ item.title }}</v-list-item-title>
  </v-list-item>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true
  }
})

const activeClass = 'active-item'
</script>

<style scoped>
.nav-item {
  border-radius: 6px;
  margin: 4px 8px;
}

.nav-item:hover {
  background-color: #f5f5f5;
}

:deep(.active-item) {
  background-color: #e3f2fd !important;
  border-radius: 8px;
}
</style>
