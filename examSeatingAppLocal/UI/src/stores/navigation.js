import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNavigationStore = defineStore('navigation', () => {
  const items = ref([
    {
      title: 'Classes',
      icon: 'mdi-school',
      to: '/',
      color: 'primary'
    },
    {
      title: 'Exam Rooms',
      icon: 'mdi-door',
      to: '/exam-rooms',
      color: 'primary'
    },
    {
      title: 'Room Schedule',
      icon: 'mdi-calendar-check',
      to: '/schedule',
      color: 'primary'
    }
  ])

  return {
    items
  }
})
