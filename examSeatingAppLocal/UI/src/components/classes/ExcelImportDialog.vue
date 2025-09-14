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
            
            Upload Excel files (.xlsx or .xls) containing student data in the required format.
          </v-alert>

          <v-file-input
            v-model="selectedFiles"
            label="Select Excel Files"
            accept=".xlsx,.xls"
            prepend-icon="mdi-file-excel"
            :rules="fileRules"
            :loading="validating"
            multiple
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
                    <li><strong>Row 1:</strong> Academic year (e.g., "I YEAR 2024-25")</li>
                    <li><strong>Row 2:</strong> Column headers</li>
                    <li><strong>Row 3+:</strong> Student data alternating between main row and date of birth row</li>
                  </ul>

                  <h4>Column Headers (Row 2):</h4>
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
                    <li><strong>Main Row:</strong> Serial No, Register No (can be empty), Student Name, Department, Shift, Language</li>
                    <li><strong>DOB Row:</strong> Empty, Empty, Date of Birth (DD/MM/YYYY), Empty, Empty, Empty</li>
                  </ul>
                  <h4>Important Notes:</h4>
                  <ul>
                    <li><strong>Column Structure:</strong> A=S.No, B=Register Number, C=Names/DOB, D=Dept/Class, E=Shift, F=Language</li>
                    <li><strong>Register Number:</strong> Column B can be left empty for first year students, required for 2nd/3rd year</li>
                    <li><strong>Language:</strong> Optional column (Hindi, Tamil, Sanskrit, etc.)</li>
                    <li><strong>Date Format:</strong> DD/MM/YYYY or Excel date format</li>
                    <li><strong>Multiple Sheets:</strong> Each sheet can contain different year/class data</li>
                  </ul>                </div>
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
              <h4>Classes to Import (Select/Deselect):</h4>
              <v-list>
                <v-list-item
                  v-for="(classInfo, index) in validationResult.summary.classes"
                  :key="index"
                >
                  <template #prepend>
                    <v-checkbox
                      v-model="selectedClasses"
                      :value="index"
                      color="primary"
                    />
                  </template>
                  <v-list-item-title>{{ classInfo.class_name }}</v-list-item-title>
                  <v-list-item-subtitle>
                    Shift: {{ classInfo.shift }} | Students: {{ classInfo.student_count }}
                  </v-list-item-subtitle>
                  <template #append>
                    <v-btn
                      icon="mdi-delete"
                      size="small"
                      color="error"
                      variant="text"
                      @click="removeClassFromSelection(index)"
                    />
                  </template>
                </v-list-item>
              </v-list>
              
              <v-alert 
                v-if="validationResult && validationResult.valid && selectedClasses.length === 0"
                type="warning" 
                variant="tonal" 
                class="mt-3"
              >
                Please select at least one class to import.
              </v-alert>
            </div>
          </div>
        </div>

        <!-- Import Results -->
        <div v-if="importResult">
          <v-alert type="success" variant="tonal" class="mb-4">
            
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
          v-if="selectedFiles && selectedFiles.length > 0 && !validationResult && !importResult"
          color="info"
          :loading="validating"
          @click="validateFile"
        >
          <v-icon left>mdi-check</v-icon>
          Validate Files
        </v-btn>
        
        <!-- Import button -->
        <v-btn
          v-if="validationResult && validationResult.valid && selectedClasses.length > 0 && !importResult"
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
import { ref, computed, watch } from 'vue'
import { bulkImportApi } from '@/services/bulkImportApi'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'import-success'])

// Reactive data
const selectedFiles = ref([])
const selectedClasses = ref([])
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
    if (!value || value.length === 0) return 'Please select at least one file'
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
const removeClassFromSelection = (index) => {
  // Remove from selected classes
  const selectedIndex = selectedClasses.value.indexOf(index)
  if (selectedIndex > -1) {
    selectedClasses.value.splice(selectedIndex, 1)
  }
}
const validateFile = async () => {
  if (!selectedFiles.value || selectedFiles.value.length === 0) return
  
  try {
    validating.value = true
    
    // Process all files and combine results
    let allClasses = []
    let allErrors = []
    let academicYear = null
    
    for (const file of selectedFiles.value) {
      try {
        const result = await bulkImportApi.validateExcel(file)
        if (result.valid && result.summary) {
          allClasses.push(...result.summary.classes)
          if (!academicYear) academicYear = result.summary.academic_year
        } else {
          allErrors.push(...result.errors.map(err => `${file.name}: ${err}`))
        }
      } catch (error) {
        allErrors.push(`${file.name}: ${error.response?.data?.detail || 'Validation failed'}`)
      }
    }
    
    validationResult.value = {
      valid: allErrors.length === 0,
      errors: allErrors,
      summary: allErrors.length === 0 ? {
        academic_year: academicYear,
        total_classes: allClasses.length,
        total_students: allClasses.reduce((sum, cls) => sum + cls.student_count, 0),
        classes: allClasses
      } : null
    }
    
    // Select all classes by default
    if (allErrors.length === 0) {
      selectedClasses.value = allClasses.map((_, index) => index)
    }
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
  if (!selectedFiles.value || selectedFiles.value.length === 0 || !validationResult.value?.valid) return
  
  try {
    importing.value = true
    // Import all selected files
    let allResults = []
    for (const file of selectedFiles.value) {
      try {
        let result
        
        // Check if we need selective import (not all classes selected)
        const totalClasses = validationResult.value?.summary?.classes?.length || 0
        const useSelectiveImport = selectedClasses.value.length < totalClasses && selectedClasses.value.length > 0
        
        if (useSelectiveImport) {
          // Send actual class identifiers instead of indices
          const selectedClassData = selectedClasses.value.map(index => {
            const classInfo = validationResult.value.summary.classes[index]
            return {
              class_name: classInfo.class_name,
              shift: classInfo.shift
            }
          })
          result = await bulkImportApi.selectiveImportExcel(file, selectedClassData)
        } else {
          result = await bulkImportApi.importExcel(file)
        }
        
        allResults.push({
          fileName: file.name,
          success: true,
          ...result
        })
      } catch (error) {
        allResults.push({
          fileName: file.name,
          success: false,
          error: error.response?.data?.detail || 'Import failed'
        })
      }
    }
    
    // Use the first successful result for compatibility
    const firstSuccess = allResults.find(r => r.success)
    if (firstSuccess) {
      importResult.value = firstSuccess
      emit("import-success")
    } else {
      importResult.value = { success: false, message: "All file imports failed", details: allResults }
    }
    
    // Emit success event to refresh classes
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
  selectedFiles.value = []; selectedClasses.value = []
  validationResult.value = null
  importResult.value = null
}

const cancel = () => {
  resetDialog()
  dialogModel.value = false
}

// Watch for dialog close to reset data
watch(() => props.modelValue, (newValue) => {
  if (!newValue) {
    resetDialog()
  }
})
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
