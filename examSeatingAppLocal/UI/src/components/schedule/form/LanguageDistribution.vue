<template>
  <v-card variant="outlined" class="mb-4" v-if="selectedClasses.length > 0">
    <v-card-title class="d-flex align-center">
      <v-icon icon="mdi-translate" class="mr-2" />
      Language Distribution
      <v-spacer />
      <v-chip size="small" color="info" variant="tonal">
        {{ totalLanguages }} languages
      </v-chip>
    </v-card-title>

    <v-card-text>
      <!-- Overall Summary -->
      <v-row class="mb-4">
        <v-col cols="12" md="4">
          <v-card variant="tonal" color="primary">
            <v-card-text class="text-center">
              <v-icon icon="mdi-account-group" size="24" class="mb-1" />
              <div class="text-h6 font-weight-bold">{{ totalStudents }}</div>
              <div class="text-caption">Total Students</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card variant="tonal" color="secondary">
            <v-card-text class="text-center">
              <v-icon icon="mdi-translate" size="24" class="mb-1" />
              <div class="text-h6 font-weight-bold">{{ studentsWithLanguage }}</div>
              <div class="text-caption">With Language Info</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card variant="tonal" color="success">
            <v-card-text class="text-center">
              <v-icon icon="mdi-percent" size="24" class="mb-1" />
              <div class="text-h6 font-weight-bold">{{ languagePercentage }}%</div>
              <div class="text-caption">Coverage</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Language Breakdown -->
      <div v-if="Object.keys(overallDistribution).length > 0">
        <div class="text-subtitle-1 mb-3">
          <v-icon icon="mdi-chart-donut" class="mr-1" />
          Language Breakdown
        </div>
        
        <v-row>
          <v-col 
            v-for="(count, language) in overallDistribution" 
            :key="language"
            cols="12" 
            sm="6" 
            md="4"
          >
            <v-card variant="outlined">
              <v-card-text class="text-center">
                <div class="text-h6 font-weight-bold" :style="{ color: getLanguageColor(language) }">
                  {{ count }}
                </div>
                <div class="text-body-2">{{ language }}</div>
                <v-progress-linear
                  :model-value="(count / studentsWithLanguage) * 100"
                  :color="getLanguageColor(language)"
                  height="4"
                  rounded
                  class="mt-2"
                />
                <div class="text-caption text-grey">
                  {{ Math.round((count / studentsWithLanguage) * 100) }}%
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>

      <!-- Class-wise Language Distribution -->
      <v-expansion-panels class="mt-4">
        <v-expansion-panel>
          <v-expansion-panel-title>
            <v-icon icon="mdi-school" class="mr-2" />
            Class-wise Language Distribution
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-simple-table density="compact">
              <thead>
                <tr>
                  <th>Class</th>
                  <th>Total Students</th>
                  <th>Languages</th>
                  <th>Distribution</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="cls in selectedClasses" :key="cls.id">
                  <td>
                    <div class="font-weight-medium">{{ getClassDisplayName(cls) }}</div>
                  </td>
                  <td>{{ cls.students?.length || 0 }}</td>
                  <td>
                    <v-chip-group>
                      <v-chip
                        v-for="lang in getClassLanguages(cls)"
                        :key="lang"
                        size="x-small"
                        :color="getLanguageColor(lang)"
                        variant="tonal"
                      >
                        {{ lang }}
                      </v-chip>
                    </v-chip-group>
                  </td>
                  <td>
                    <div class="text-caption">
                      {{ formatClassLanguageDistribution(cls) }}
                    </div>
                  </td>
                </tr>
              </tbody>
            </v-simple-table>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'
import { 
  getClassDisplayName, 
  getClassLanguages, 
  getClassLanguageDistribution,
  getUniqueLanguages 
} from '@/utils/classUtils'

const props = defineProps({
  selectedClasses: {
    type: Array,
    default: () => []
  }
})

// Computed properties
const totalStudents = computed(() => {
  return props.selectedClasses.reduce((total, cls) => {
    return total + (cls.students?.length || 0)
  }, 0)
})

const overallDistribution = computed(() => {
  const distribution = {}
  
  props.selectedClasses.forEach(cls => {
    if (cls.students && Array.isArray(cls.students)) {
      cls.students.forEach(student => {
        if (student.language && student.language.trim()) {
          const lang = student.language.trim()
          distribution[lang] = (distribution[lang] || 0) + 1
        }
      })
    }
  })
  
  return distribution
})

const studentsWithLanguage = computed(() => {
  return Object.values(overallDistribution.value).reduce((sum, count) => sum + count, 0)
})

const languagePercentage = computed(() => {
  if (totalStudents.value === 0) return 0
  return Math.round((studentsWithLanguage.value / totalStudents.value) * 100)
})

const totalLanguages = computed(() => {
  return Object.keys(overallDistribution.value).length
})

// Helper methods
const getLanguageColor = (language) => {
  const colors = {
    'Hindi': 'orange',
    'English': 'blue',
    'Marathi': 'green',
    'Tamil': 'purple',
    'Telugu': 'teal',
    'Gujarati': 'indigo',
    'Bengali': 'pink'
  }
  return colors[language] || 'grey'
}

const formatClassLanguageDistribution = (cls) => {
  const distribution = getClassLanguageDistribution(cls)
  const entries = Object.entries(distribution)
  
  if (entries.length === 0) return 'No language info'
  if (entries.length === 1) return `${entries[0][1]} ${entries[0][0]}`
  
  return entries.map(([lang, count]) => `${count} ${lang}`).join(', ')
}
</script>

<style scoped>
.v-progress-linear {
  border-radius: 2px;
}
</style>
