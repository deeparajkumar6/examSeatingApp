<template>
  <v-container>
    <v-card>
      <v-card-title>Language Selection Debug</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <h3>Original Classes Data</h3>
            <pre>{{ JSON.stringify(classes, null, 2) }}</pre>
          </v-col>
          <v-col cols="12" md="6">
            <h3>Expanded Classes</h3>
            <pre>{{ JSON.stringify(expandedClasses, null, 2) }}</pre>
          </v-col>
        </v-row>
        
        <v-divider class="my-4" />
        
        <v-row>
          <v-col cols="12">
            <h3>Class Selector</h3>
            <EnhancedClassSelector
              v-model="selectedClasses"
              :classes="classes"
            />
          </v-col>
        </v-row>
        
        <v-divider class="my-4" />
        
        <v-row>
          <v-col cols="12" md="6">
            <h3>Selected Classes (Raw)</h3>
            <pre>{{ JSON.stringify(selectedClasses, null, 2) }}</pre>
          </v-col>
          <v-col cols="12" md="6">
            <h3>Converted for API</h3>
            <pre>{{ JSON.stringify(convertedSelections, null, 2) }}</pre>
          </v-col>
        </v-row>
        
        <v-divider class="my-4" />
        
        <v-row>
          <v-col cols="12">
            <v-btn 
              color="primary" 
              @click="testApiCall"
              :disabled="selectedClasses.length === 0"
            >
              Test API Call
            </v-btn>
          </v-col>
        </v-row>
        
        <v-row v-if="apiResponse">
          <v-col cols="12">
            <h3>API Response</h3>
            <pre>{{ JSON.stringify(apiResponse, null, 2) }}</pre>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import EnhancedClassSelector from '../schedule/form/EnhancedClassSelector.vue'
import { 
  expandClassesByLanguage,
  convertExpandedSelectionsToOriginal 
} from '@/utils/classUtils'

// Mock data for testing
const classes = ref([
  {
    id: 1,
    className: 'I B.COM -CS',
    shift: 'I',
    students: [
      { id: 1, rollNumber: '001', studentName: 'Student A', language: 'Hindi' },
      { id: 2, rollNumber: '002', studentName: 'Student B', language: 'Hindi' },
      { id: 3, rollNumber: '003', studentName: 'Student C', language: 'English' },
      { id: 4, rollNumber: '004', studentName: 'Student D', language: 'English' },
      { id: 5, rollNumber: '005', studentName: 'Student E', language: 'Marathi' }
    ]
  },
  {
    id: 2,
    className: 'II B.COM -CS',
    shift: 'I',
    students: [
      { id: 6, rollNumber: '101', studentName: 'Student F', language: 'Hindi' },
      { id: 7, rollNumber: '102', studentName: 'Student G', language: 'English' },
      { id: 8, rollNumber: '103', studentName: 'Student H', language: 'English' }
    ]
  }
])

const selectedClasses = ref([])
const apiResponse = ref(null)

const expandedClasses = computed(() => {
  return expandClassesByLanguage(classes.value)
})

const convertedSelections = computed(() => {
  if (selectedClasses.value.length === 0) return null
  return convertExpandedSelectionsToOriginal(selectedClasses.value, expandedClasses.value)
})

const testApiCall = async () => {
  if (!convertedSelections.value) return
  
  const requestData = {
    date: '2025-07-11',
    classes: convertedSelections.value.classSelections,
    exam_rooms: [1],
    split: true,
    language_selections: convertedSelections.value.languageSelections
  }
  
  console.log('🚀 Making API call with:', requestData)
  
  try {
    const response = await fetch('/api/schedule', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    })
    
    const data = await response.json()
    apiResponse.value = data
    console.log('📥 API Response:', data)
  } catch (error) {
    console.error('❌ API Error:', error)
    apiResponse.value = { error: error.message }
  }
}
</script>

<style scoped>
pre {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 0.875rem;
  max-height: 300px;
  overflow-y: auto;
}
</style>
