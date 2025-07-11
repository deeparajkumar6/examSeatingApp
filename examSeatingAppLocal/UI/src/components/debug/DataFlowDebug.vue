<template>
  <v-expansion-panels class="mb-4">
    <v-expansion-panel>
      <v-expansion-panel-title>
        <v-icon icon="mdi-bug" class="mr-2" />
        Debug: Data Flow Analysis
      </v-expansion-panel-title>
      <v-expansion-panel-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-card variant="outlined">
              <v-card-title>Original Classes ({{ classes.length }})</v-card-title>
              <v-card-text>
                <div v-for="cls in classes" :key="cls.id" class="mb-2">
                  <strong>{{ cls.className }} - {{ cls.shift }}</strong>
                  <div class="text-caption">
                    Students: {{ cls.students?.length || 0 }}
                    <span v-if="cls.students?.length > 0">
                      | Languages: {{ getClassLanguages(cls).join(', ') || 'None' }}
                    </span>
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card variant="outlined">
              <v-card-title>Expanded Classes ({{ expandedClasses.length }})</v-card-title>
              <v-card-text>
                <div v-for="expanded in expandedClasses" :key="expanded.id" class="mb-2">
                  <strong>{{ expanded.displayName }}</strong>
                  <div class="text-caption">
                    ID: {{ expanded.id }} | Students: {{ expanded.students?.length || 0 }}
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        
        <v-row class="mt-4">
          <v-col cols="12" md="6">
            <v-card variant="outlined">
              <v-card-title>Selected IDs</v-card-title>
              <v-card-text>
                <pre>{{ JSON.stringify(selectedClasses, null, 2) }}</pre>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card variant="outlined">
              <v-card-title>Converted for API</v-card-title>
              <v-card-text>
                <pre>{{ JSON.stringify(convertedSelections, null, 2) }}</pre>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup>
import { computed } from 'vue'
import { 
  getClassLanguages,
  expandClassesByLanguage,
  convertExpandedSelectionsToOriginal 
} from '@/utils/classUtils'

const props = defineProps({
  classes: {
    type: Array,
    default: () => []
  },
  selectedClasses: {
    type: Array,
    default: () => []
  }
})

const expandedClasses = computed(() => {
  return expandClassesByLanguage(props.classes)
})

const convertedSelections = computed(() => {
  if (props.selectedClasses.length === 0) return null
  return convertExpandedSelectionsToOriginal(props.selectedClasses, expandedClasses.value)
})
</script>

<style scoped>
pre {
  background: #f5f5f5;
  padding: 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  max-height: 200px;
  overflow-y: auto;
}
</style>
