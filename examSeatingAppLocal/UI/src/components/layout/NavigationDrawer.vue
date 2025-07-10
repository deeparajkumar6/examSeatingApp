<template>
  <v-navigation-drawer v-model="drawerModel">
    <v-list dense nav>
      <NavigationItem
        v-for="item in navigationItems"
        :key="item.to"
        :item="item"
      />
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { computed } from 'vue'
import NavigationItem from './NavigationItem.vue'
import { useNavigationStore } from '@/stores/navigation'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue'])

const drawerModel = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const navigationStore = useNavigationStore()
const navigationItems = computed(() => navigationStore.items)
</script>
