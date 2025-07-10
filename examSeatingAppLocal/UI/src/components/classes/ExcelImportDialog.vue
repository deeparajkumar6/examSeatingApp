<template>
  <v-dialog v-model="dialogModel" max-width="800px" persistent>
    <v-card>
      <v-card-title class="d-flex align-center">
        <v-icon class="mr-2">mdi-file-excel</v-icon>
        Import Classes from Excel
      </v-card-title>

      <v-card-text>
        <!-- File Upload Section -->
        <div v-if="!validationResult && !importResult">
          <v-alert type="info" variant="tonal" class="mb-4">
            <v-icon left>mdi-information</v-icon>
            Upload an Excel file (.xlsx or .xls) containing student data in the required format.
          </v-alert>

          <v-file-input
            v-model="selectedFile"
            label="Select Excel File"
            accept=".xlsx,.xls"
            prepend-icon="mdi-file-excel"
            :rules="fileRules"
            :loading="validating"
            @change="handleFileChange"
          />

          <!-- Format Information -->
          <v-expansion-panels class="mt-4">
            <v-expansion-panel>
              <v-expansion-panel-title>
                <v-icon left>mdi-help-circle</v-icon>
                Excel File Format Requirements
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                <div class="format-info">
                  <h4>Required Structure:</h4>
                  <ul>
                    <li><strong>Row 4:</strong> Academic year (e.g., "I YEAR 2023-24")</li>
                    <li><strong>Row 5:</strong> Column headers</li>
                    <li><strong>Data rows:</strong> Student information split across two rows</li>
                  </ul>

                  <h4>Column Headers (Row 5):</h4>
                  <v-chip-group>
                    <v-chip size="small">S.No</v-chip>
                    <v-chip size="small">Register Number</v-chip>
                    <v-chip size="small">Names with Date of Birth</v-chip>
                    <v-chip size="small">Dept / Class</v-chip>
                    <v-chip size="small">Shift</v-chip>
                    <v-chip size="small">Language</v-chip>
                  </v-chip-group>

                  <h4>Student Data Format:</h4>
                  <p>Each student requires two consecutive rows:</p>
                  <ul>
                    <li><strong>Row 1:</strong> Serial No, Register No, Name, Department, Shift, Language</li>
                    <li><strong>Row 2:</strong> Empty, Empty, Date of Birth, Empty, Empty, Empty</li>
                  </ul>
                </div>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>

        <!-- Validation Results -->
        <div v-if="validationResult && !importResult">
          <v-alert 
            :type="validationResult.valid ? 'success' : 'error'" 
            variant="tonal" 
            class="mb-4"
          >
            <v-icon left>
              {{ validationResult.valid ? 'mdi-check-circle' : 'mdi-alert-circle' }}
            </v-icon>
            {{ validationResult.valid ? 'File validation successful!' : 'File validation failed!' }}
          </v-alert>

          <!-- Validation Errors -->
          <div v-if="!validationResult.valid && validationResult.errors.length > 0">
            <h4>Validation Errors:</h4>
            <v-list density="compact">
              <v-list-item
                v-for="(error, index) in validationResult.errors"
                :key="index"
                class="text-error"
              >
                <template #prepend>
                  <v-icon color="error">mdi-alert</v-icon>
                </template>
                <v-list-item-title>{{ error }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </div>

          <!-- Validation Summary -->
          <div v-if="validationResult.valid && validationResult.summary">
            <h4>Import Summary:</h4>
            <v-row>
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-text>
                    <div class="text-h6">{{ validationResult.summary.total_classes }}</div>
                    <div class="text-caption">Classes to Import</div>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card variant="outlined">
                  <v-card-text>
                    <div class="text-h6">{{ validationResult.summary.total_students }}</div>
                    <div class="text-caption">Students to Import</div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Class Details -->
            <div class="mt-4">
              <h4>Classes Preview:</h4>
              <v-list>
                <v-list-item
                  v-for="(classInfo, index) in validationResult.summary.classes"
                  :key="index"
                >
                  <template #prepend>
                    <v-icon>mdi-school</v-icon>
                  </template>
                  <v-list-item-title>{{ classInfo.class_name }}</v-list-item-title>
                  <v-list-item-subtitle>
                    Shift: {{ classInfo.shift }} | Students: {{ classInfo.student_count }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </div>
          </div>
        </div>

        <!-- Import Results -->
        <div v-if="importResult">
          <v-alert type="success" variant="tonal" class="mb-4">
            <v-icon left>mdi-check-circle</v-icon>
            {{ importResult.message }}
          </v-alert>

          <v-row>
            <v-col cols="12" md="6">
              <v-card variant="outlined">
                <v-card-text>
                  <div class="text-h6">{{ importResult.classesCreated }}</div>
                  <div class="text-caption">Classes Created</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" md="6">
              <v-card variant="outlined">
                <v-card-text>
                  <div class="text-h6">{{ importResult.studentsCreated }}</div>
                  <div class="text-caption">Students Created</div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Import Details -->
          <div class="mt-4">
            <h4>Import Details:</h4>
            <v-list>
              <v-list-item
                v-for="(detail, index) in importResult.details"
                :key="index"
              >
                <template #prepend>
                  <v-icon :color="detail.action === 'created' ? 'success' : 'warning'">
                    {{ detail.action === 'created' ? 'mdi-plus-circle' : 'mdi-update' }}
                  </v-icon>
                </template>
                <v-list-item-title>{{ detail.className }}</v-list-item-title>
                <v-list-item-subtitle>
                  Shift: {{ detail.shift }} | 
                  {{ detail.action === 'created' ? 'Created' : 'Updated' }} with {{ detail.studentsAdded }} students
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </div>
        </div>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        
        <!-- Back button (when showing validation results) -->
        <v-btn 
          v-if="validationResult && !importResult"
          @click="resetDialog"
        >
          <v-icon left>mdi-arrow-left</v-icon>
          Back
        </v-btn>
        
        <!-- Cancel button -->
        <v-btn @click="cancel">
          {{ importResult ? 'Close' : 'Cancel' }}
        </v-btn>
        
        <!-- Validate button -->
        <v-btn
          v-if="selectedFile && !validationResult && !importResult"
          color="info"
          :loading="validating"
          @click="validateFile"
        >
          <v-icon left>mdi-check</v-icon>
          Validate File
        </v-btn>
        
        <!-- Import button -->
        <v-btn
          v-if="validationResult && validationResult.valid && !importResult"
          color="primary"
          :loading="importing"
          @click="importFile"
        >
          <v-icon left>mdi-upload</v-icon>
          Import Data
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { bulkImportApi } from '@/services/bulkImportApi'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'import-success'])

// Reactive data
const selectedFile = ref(null)
const validating = ref(false)
const importing = ref(false)
const validationResult = ref(null)
const importResult = ref(null)

// Computed
const dialogModel = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Validation rules
const fileRules = [
  (value) => {
    if (!value || value.length === 0) return 'Please select a file'
    const file = Array.isArray(value) ? value[0] : value
    if (!file.name.match(/\.(xlsx|xls)$/i)) {
      return 'Please select an Excel file (.xlsx or .xls)'
    }
    return true
  }
]

// Methods
const handleFileChange = () => {
  // Reset validation and import results when file changes
  validationResult.value = null
  importResult.value = null
}

const validateFile = async () => {
  if (!selectedFile.value) return
  
  try {
    validating.value = true
    const file = Array.isArray(selectedFile.value) ? selectedFile.value[0] : selectedFile.value
    const result = await bulkImportApi.validateExcel(file)
    validationResult.value = result
  } catch (error) {
    console.error('Validation failed:', error)
    validationResult.value = {
      valid: false,
      errors: [error.response?.data?.detail || 'Validation failed'],
      summary: null
    }
  } finally {
    validating.value = false
  }
}

const importFile = async () => {
  if (!selectedFile.value || !validationResult.value?.valid) return
  
  try {
    importing.value = true
    const file = Array.isArray(selectedFile.value) ? selectedFile.value[0] : selectedFile.value
    const result = await bulkImportApi.importExcel(file)
    importResult.value = result
    
    // Emit success event to refresh classes
    emit('import-success')
  } catch (error) {
    console.error('Import failed:', error)
    // Show error in validation result format
    validationResult.value = {
      valid: false,
      errors: [error.response?.data?.detail || 'Import failed'],
      summary: null
    }
  } finally {
    importing.value = false
  }
}

const resetDialog = () => {
  selectedFile.value = null
  validationResult.value = null
  importResult.value = null
}

const cancel = () => {
  resetDialog()
  dialogModel.value = false
}
</script>

<style scoped>
.format-info {
  font-size: 0.875rem;
}

.format-info h4 {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.format-info ul {
  margin-left: 1rem;
  margin-bottom: 1rem;
}

.format-info li {
  margin-bottom: 0.25rem;
}
</style>
