<template>
  <v-container>
    <v-card>
      <div class="d-flex justify-space-between align-center pa-3">
        <v-card-title>Class Management</v-card-title>
        <div class="d-flex gap-2">
          <v-btn color="secondary" @click="openCsvDialog">
            <v-icon left>
              mdi-upload
            </v-icon>
            Upload CSV
          </v-btn>
          <v-btn color="primary" @click="openAddDialog">
            Add Class
          </v-btn>
        </div>
      </div>
      <v-card-text>
        <v-data-table :headers="headers" item-key="id" :items="classes">
          <template #item.studentCount="{ item }">
            {{ item.students.length }}
          </template>
          <template #item.rollNumbers="{ item }">
            <v-chip-group>
              <v-chip
                v-for="student in item.students.slice(0, 5)"
                :key="student.id"
                size="small"
              >
                {{ student.rollNumber }}
              </v-chip>
              <v-chip
                v-if="item.students.length > 5"
                size="small"
                variant="outlined"
              >
                +{{ item.students.length - 5 }} more
              </v-chip>
            </v-chip-group>
          </template>
          <template #item.actions="{ item }">
            <v-btn icon variant="flat" @click="openEditDialog(item)">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon variant="flat" @click="deleteClass(item.id)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Add/Edit Class Dialog -->
    <v-dialog v-model="dialog" max-width="800">
      <v-card>
        <v-card-title>
          {{
            isEditing ? "Edit Class" : "Add New Class"
          }}
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="currentClass.className"
            class="mb-4"
            label="Class Name"
            variant="outlined"
          />

          <div class="d-flex justify-space-between align-center mb-3">
            <h3>Students</h3>
            <v-btn color="primary" size="small" @click="addStudent">
              <v-icon left>
                mdi-plus
              </v-icon>
              Add Student
            </v-btn>
          </div>

          <!-- Students List -->
          <v-card class="mb-4" variant="outlined">
            <v-card-text>
              <div
                v-if="currentClass.students.length === 0"
                class="text-center text-grey"
              >
                No students added yet
              </div>
              <div v-else>
                <v-row
                  v-for="(student, index) in currentClass.students"
                  :key="index"
                  class="mb-2 align-center"
                >
                  <v-col cols="5">
                    <v-text-field
                      v-model="student.rollNumber"
                      density="compact"
                      hide-details
                      label="Roll Number"
                      variant="outlined"
                    />
                  </v-col>
                  <v-col cols="5">
                    <v-text-field
                      v-model="student.studentName"
                      density="compact"
                      hide-details
                      label="Student Name (Optional)"
                      variant="outlined"
                    />
                  </v-col>
                  <v-col cols="2">
                    <v-btn
                      color="error"
                      icon
                      size="small"
                      variant="flat"
                      @click="removeStudent(index)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </div>
            </v-card-text>
          </v-card>

          <!-- Bulk Add Students -->
          <v-expansion-panels class="mb-4">
            <v-expansion-panel>
              <v-expansion-panel-title>
                <v-icon left>
                  mdi-format-list-numbered
                </v-icon>
                Bulk Add Students
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                <v-textarea
                  v-model="bulkStudents"
                  class="mb-3"
                  label="Enter roll numbers (one per line or comma separated)"
                  placeholder="101&#10;102&#10;105&#10;or&#10;101, 102, 105"
                  rows="4"
                  variant="outlined"
                />
                <v-btn color="primary" @click="processBulkStudents">
                  Add Students
                </v-btn>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="closeDialog">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="saveClass">
            {{
              isEditing ? "Update" : "Add"
            }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- CSV Upload Dialog -->
    <v-dialog v-model="csvDialog" max-width="700">
      <v-card>
        <v-card-title>
          <v-icon left>
            mdi-upload
          </v-icon>
          Upload Students from CSV
        </v-card-title>
        <v-card-text>
          <v-alert class="mb-4" type="info">
            <div class="text-subtitle-2 mb-2">
              CSV Format Requirements:
            </div>
            <ul class="ml-4">
              <li>
                Required columns: <strong>className</strong>,
                <strong>rollNumber</strong>, <strong>studentName</strong>
              </li>
              <li>File must be in CSV format (.csv)</li>
              <li>First row should contain column headers</li>
              <li>Missing roll numbers are allowed (non-sequential)</li>
            </ul>
          </v-alert>

          <div class="mb-4">
            <v-btn
              class="mb-3"
              color="primary"
              prepend-icon="mdi-download"
              variant="outlined"
              @click="downloadTemplate"
            >
              Download Template
            </v-btn>
          </div>

          <v-file-input
            v-model="csvFile"
            accept=".csv"
            class="mb-4"
            label="Select CSV File"
            prepend-icon="mdi-file-delimited"
            show-size
          />

          <v-progress-linear
            v-if="csvUploading"
            class="mb-4"
            color="primary"
            indeterminate
          />

          <!-- Upload Results -->
          <v-card v-if="uploadResult" class="mb-4" variant="outlined">
            <v-card-title class="text-h6">
              Upload Results
            </v-card-title>
            <v-card-text>
              <div class="mb-2">
                <v-chip class="mr-2" color="success">
                  {{ uploadResult.summary.total_students_processed }} Students
                  Processed
                </v-chip>
                <v-chip class="mr-2" color="info">
                  {{ uploadResult.summary.classes_created }} Classes Created
                </v-chip>
                <v-chip class="mr-2" color="warning">
                  {{ uploadResult.summary.classes_updated }} Classes Updated
                </v-chip>
                <v-chip
                  v-if="uploadResult.summary.errors_count > 0"
                  color="error"
                >
                  {{ uploadResult.summary.errors_count }} Errors
                </v-chip>
              </div>

              <div
                v-if="uploadResult.details.created_classes.length > 0"
                class="mb-2"
              >
                <strong>Created Classes:</strong>
                <v-chip-group>
                  <v-chip
                    v-for="className in uploadResult.details.created_classes"
                    :key="className"
                    color="success"
                    size="small"
                    variant="outlined"
                  >
                    {{ className }}
                  </v-chip>
                </v-chip-group>
              </div>

              <div
                v-if="uploadResult.details.updated_classes.length > 0"
                class="mb-2"
              >
                <strong>Updated Classes:</strong>
                <v-chip-group>
                  <v-chip
                    v-for="className in uploadResult.details.updated_classes"
                    :key="className"
                    color="warning"
                    size="small"
                    variant="outlined"
                  >
                    {{ className }}
                  </v-chip>
                </v-chip-group>
              </div>

              <div v-if="uploadResult.details.errors.length > 0">
                <strong>Errors:</strong>
                <v-list density="compact">
                  <v-list-item
                    v-for="(error, index) in uploadResult.details.errors"
                    :key="index"
                    class="text-error"
                  >
                    <v-list-item-title>{{ error }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </div>
            </v-card-text>
          </v-card>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="closeCsvDialog">
            Close
          </v-btn>
          <v-btn
            color="primary"
            :disabled="!csvFile || csvUploading"
            :loading="csvUploading"
            @click="uploadCsv"
          >
            Upload
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      classes: [],
      dialog: false,
      csvDialog: false,
      isEditing: false,
      bulkStudents: '',
      csvFile: null,
      csvUploading: false,
      uploadResult: null,
      currentClass: {
        id: null,
        className: '',
        students: [],
      },
      headers: [
        { title: 'Class Name', key: 'className' },
        { title: 'Student Count', key: 'studentCount' },
        { title: 'Roll Numbers', key: 'rollNumbers', sortable: false },
        { title: 'Actions', key: 'actions', sortable: false },
      ],
    }
  },

  mounted () {
    this.fetchClasses()
  },
  methods: {
    async fetchClasses () {
      try {
        const res = await axios.get('http://localhost:8000/class')
        this.classes = res.data.classes
      } catch (error) {
        console.error('Error fetching classes:', error)
      }
    },

    openAddDialog () {
      this.isEditing = false
      this.currentClass = {
        id: null,
        className: '',
        students: []
      };
      this.bulkStudents = ''
      this.dialog = true
    },

    openEditDialog (item) {
      this.isEditing = true
      this.currentClass = {
        ...item,
        students: [...item.students.map(s => ({ ...s }))]
      };
      this.bulkStudents = ''
      this.dialog = true
    },

    closeDialog () {
      this.dialog = false
      this.bulkStudents = ''
    },

    addStudent () {
      this.currentClass.students.push({
        rollNumber: '',
        studentName: '',
      })
    },

    removeStudent (index) {
      this.currentClass.students.splice(index, 1)
    },

    processBulkStudents () {
      if (!this.bulkStudents.trim()) return

      // Split by newlines or commas and clean up
      const rollNumbers = this.bulkStudents
        .split(/[\n,]/)
        .map(roll => roll.trim())
        .filter(roll => roll.length > 0)

      // Add unique roll numbers
      const existingRolls = new Set(
        this.currentClass.students.map(s => s.rollNumber)
      )

      rollNumbers.forEach(rollNumber => {
        if (!existingRolls.has(rollNumber)) {
          this.currentClass.students.push({
            rollNumber,
            studentName: '',
          })
          existingRolls.add(rollNumber)
        }
      })

      // Sort students by roll number
      this.currentClass.students.sort((a, b) => {
        // Try to sort numerically if possible, otherwise alphabetically
        const aNum = parseInt(a.rollNumber)
        const bNum = parseInt(b.rollNumber)
        if (!isNaN(aNum) && !isNaN(bNum)) {
          return aNum - bNum
        }
        return a.rollNumber.localeCompare(b.rollNumber)
      })

      this.bulkStudents = ''
    },

    async saveClass () {
      try {
        // Validate that all students have roll numbers
        const invalidStudents = this.currentClass.students.filter(
          s => !s.rollNumber.trim()
        )
        if (invalidStudents.length > 0) {
          alert('Please provide roll numbers for all students')
          return
        }

        // Check for duplicate roll numbers
        const rollNumbers = this.currentClass.students.map(s =>
          s.rollNumber.trim()
        )
        const uniqueRolls = new Set(rollNumbers)
        if (rollNumbers.length !== uniqueRolls.size) {
          alert(
            'Duplicate roll numbers found. Please ensure all roll numbers are unique.'
          )
          return
        }

        const classData = {
          className: this.currentClass.className,
          students: this.currentClass.students.map(s => ({
            rollNumber: s.rollNumber.trim(),
            studentName: s.studentName?.trim() || null
          }))
        };

        if (this.isEditing) {
          await axios.put(
            `http://localhost:8000/class/${this.currentClass.id}`,
            classData
          )
        } else {
          await axios.post('http://localhost:8000/class', classData)
        }

        this.closeDialog()
        this.fetchClasses()
      } catch (error) {
        console.error('Error saving class:', error)
        alert('Error saving class. Please try again.')
      }
    },

    async deleteClass (id) {
      if (
        confirm(
          'Are you sure you want to delete this class and all its students?'
        )
      ) {
        try {
          await axios.delete(`http://localhost:8000/class/${id}`)
          this.fetchClasses()
        } catch (error) {
          console.error('Error deleting class:', error)
          alert('Error deleting class. Please try again.')
        }
      }
    },

    // CSV Upload Methods
    openCsvDialog () {
      this.csvDialog = true
      this.csvFile = null
      this.uploadResult = null
    },

    closeCsvDialog () {
      this.csvDialog = false
      this.csvFile = null
      this.uploadResult = null
    },

    async downloadTemplate () {
      try {
        const response = await axios.get(
          'http://localhost:8000/download-csv-template',
          {
            responseType: 'blob',
          }
        )

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'student_upload_template.csv')
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
      } catch (error) {
        console.error('Error downloading template:', error)
        alert('Error downloading template. Please try again.')
      }
    },

    async uploadCsv () {
      if (!this.csvFile) {
        alert('Please select a CSV file')
        return
      }

      this.csvUploading = true
      this.uploadResult = null

      try {
        const formData = new FormData()
        formData.append('file', this.csvFile)

        const response = await axios.post(
          'http://localhost:8000/upload-csv',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            }
          }
        )

        this.uploadResult = response.data

        // Refresh the classes list
        await this.fetchClasses()

        // Show success message
        const summary = response.data.summary
        let message = 'Upload completed!\n'
        message += `Students processed: ${summary.total_students_processed}\n`
        message += `Classes created: ${summary.classes_created}\n`
        message += `Classes updated: ${summary.classes_updated}`

        if (summary.errors_count > 0) {
          message += `\nErrors: ${summary.errors_count} (see details below)`
        }

        alert(message)
      } catch (error) {
        console.error('Error uploading CSV:', error)
        const errorMessage =
          error.response?.data?.detail ||
          'Error uploading CSV file. Please try again.'
        alert(errorMessage)
      } finally {
        this.csvUploading = false
      }
    }
  },
}
</script>

<style scoped>
.v-expansion-panel-text {
  padding-top: 16px;
}
</style>
