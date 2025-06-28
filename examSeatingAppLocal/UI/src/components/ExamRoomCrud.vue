<template>
  <v-container>
    <v-card>
      <div class="d-flex justify-space-between align-center pa-3">
        <v-card-title>Exam Room Management</v-card-title>
        <div class="d-flex gap-2">
          <v-btn color="secondary" @click="openCsvDialog">
            <v-icon left>
              mdi-upload
            </v-icon>
            Upload CSV
          </v-btn>
          <v-btn color="primary" @click="openAddDialog">
            Add Exam Room
          </v-btn>
        </div>
      </div>
      <v-card-text>
        <v-data-table :headers="headers" :items="examRooms">
          <template #item.actions="{ item }">
            <v-btn icon variant="flat" @click="openEditDialog(item)">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon variant="flat" @click="deleteExamRoom(item.id)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Add/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>
          {{
            isEditing ? "Edit Exam Room" : "Add Exam Room"
          }}
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="currentExamRoom.roomNumber"
            label="Room Number"
            variant="outlined"
          />
          <v-text-field
            v-model.number="currentExamRoom.roomCapacity"
            label="Room Capacity"
            type="number"
            variant="outlined"
          />
          <v-text-field
            v-model="currentExamRoom.roomFloor"
            label="Room Floor"
            variant="outlined"
          />
          <v-text-field
            v-model="currentExamRoom.roomBuilding"
            label="Room Building"
            variant="outlined"
          />
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="closeDialog">
            Cancel
          </v-btn>
          <v-btn color="primary" @click="saveExamRoom">
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
          Upload Exam Rooms from CSV
        </v-card-title>
        <v-card-text>
          <v-alert class="mb-4" type="info">
            <div class="text-subtitle-2 mb-2">
              CSV Format Requirements:
            </div>
            <ul class="ml-4">
              <li>
                Required columns: <strong>roomNumber</strong>,
                <strong>roomCapacity</strong>, <strong>roomFloor</strong>,
                <strong>roomBuilding</strong>
              </li>
              <li>File must be in CSV format (.csv)</li>
              <li>First row should contain column headers</li>
              <li>Room capacity must be a positive number</li>
              <li>Room numbers must be unique</li>
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
                  {{ uploadResult.summary.rooms_added }} Rooms Added
                </v-chip>
                <v-chip class="mr-2" color="warning">
                  {{ uploadResult.summary.rooms_skipped }} Rooms Skipped
                </v-chip>
                <v-chip
                  v-if="uploadResult.summary.errors_count > 0"
                  color="error"
                >
                  {{ uploadResult.summary.errors_count }} Errors
                </v-chip>
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
      examRooms: [],
      dialog: false,
      csvDialog: false,
      isEditing: false,
      csvFile: null,
      csvUploading: false,
      uploadResult: null,
      currentExamRoom: {
        id: null,
        roomNumber: '',
        roomCapacity: 30,
        roomFloor: '',
        roomBuilding: '',
      },
      headers: [
        { title: 'Room Number', key: 'roomNumber' },
        { title: 'Capacity', key: 'roomCapacity' },
        { title: 'Floor', key: 'roomFloor' },
        { title: 'Building', key: 'roomBuilding' },
        { title: 'Actions', key: 'actions', sortable: false }
      ],
    }
  },

  mounted () {
    this.fetchExamRooms()
  },
  methods: {
    async fetchExamRooms () {
      try {
        const res = await axios.get('http://localhost:8000/examRoom')
        this.examRooms = res.data.examRooms
      } catch (error) {
        console.error('Error fetching exam rooms:', error)
      }
    },

    openAddDialog () {
      this.isEditing = false
      this.currentExamRoom = {
        id: null,
        roomNumber: '',
        roomCapacity: 30,
        roomFloor: '',
        roomBuilding: ''
      }
      this.dialog = true
    },

    openEditDialog (item) {
      this.isEditing = true
      this.currentExamRoom = { ...item }
      this.dialog = true
    },

    closeDialog () {
      this.dialog = false
    },

    async saveExamRoom () {
      try {
        if (this.isEditing) {
          await axios.put(
            `http://localhost:8000/examRoom/${this.currentExamRoom.id}`,
            this.currentExamRoom
          )
        } else {
          await axios.post(
            'http://localhost:8000/examRoom',
            this.currentExamRoom
          )
        }
        this.closeDialog()
        this.fetchExamRooms()
      } catch (error) {
        console.error('Error saving exam room:', error)
        alert('Error saving exam room. Please try again.')
      }
    },

    async deleteExamRoom (id) {
      if (confirm('Are you sure you want to delete this exam room?')) {
        try {
          await axios.delete(`http://localhost:8000/examRoom/${id}`)
          this.fetchExamRooms()
        } catch (error) {
          console.error('Error deleting exam room:', error)
          alert('Error deleting exam room. Please try again.')
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
          'http://localhost:8000/download-exam-rooms-csv-template',
          {
            responseType: 'blob'
          }
        )

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'exam_rooms_upload_template.csv')
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
          'http://localhost:8000/upload-exam-rooms-csv',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        )

        this.uploadResult = response.data

        // Refresh the exam rooms list
        await this.fetchExamRooms()

        // Show success message
        const summary = response.data.summary
        let message = 'Upload completed!\n'
        message += `Rooms processed: ${summary.total_rooms_processed}\n`
        message += `Rooms added: ${summary.rooms_added}\n`
        message += `Rooms skipped: ${summary.rooms_skipped}`

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
    },
  },
}
</script>
