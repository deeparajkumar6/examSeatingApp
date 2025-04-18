<template>
  <v-container>
    <v-card>
      <div class="d-flex justify-space-between align-center pa-3">
        
      
        <v-card-title>Exam Room Management</v-card-title>
      
      <v-btn color="primary" @click="openAddDialog">Add Exam Room</v-btn></div>
      <v-card-text>
        
        <v-data-table :items="examRooms" :headers="headers">
          <template #item.actions="{ item }">
            <v-btn variant="flat" icon @click="openEditDialog(item)">
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
        <v-card-title>{{ isEditing ? 'Edit Exam Room' : 'Add Exam Room' }}</v-card-title>
        <v-card-text>
          <v-text-field variant="outlined" v-model="currentExamRoom.roomNumber" label="Room Number"></v-text-field>
          <v-text-field variant="outlined" v-model.number="currentExamRoom.roomCapacity" label="Room Capacity" type="number"></v-text-field>
          <v-text-field variant="outlined" v-model="currentExamRoom.roomFloor" label="Room Floor"></v-text-field>
          <v-text-field variant="outlined" v-model="currentExamRoom.roomBuilding" label="Room Building"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="closeDialog">Cancel</v-btn>
          <v-btn color="primary" @click="saveExamRoom">{{ isEditing ? 'Update' : 'Add' }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      examRooms: [],
      dialog: false,
      isEditing: false,
      currentExamRoom: {
        id: null,
        roomNumber: '',
        roomCapacity: 0,
        roomFloor: '',
        roomBuilding: ''
      },
      headers: [
        // { title: 'ID', key: 'id' },
        { title: 'Room Number', key: 'roomNumber' },
        { title: 'Capacity', key: 'roomCapacity' },
        { title: 'Floor', key: 'roomFloor' },
        { title: 'Building', key: 'roomBuilding' },
        { title: 'Actions', key: 'actions', sortable: false }
      ]
    }
  },
  methods: {
    async fetchExamRooms() {
      const res = await axios.get('http://localhost:8000/examRoom')
      this.examRooms = res.data.examRooms
    },
    openAddDialog() {
      this.isEditing = false
      this.currentExamRoom = {
        id: null,
        roomNumber: '',
        roomCapacity: 0,
        roomFloor: '',
        roomBuilding: ''
      }
      this.dialog = true
    },
    openEditDialog(item) {
      this.isEditing = true
      this.currentExamRoom = { ...item }
      this.dialog = true
    },
    closeDialog() {
      this.dialog = false
    },
    async saveExamRoom() {
      if (this.isEditing) {
        await axios.put(`http://localhost:8000/examRoom/${this.currentExamRoom.id}`, this.currentExamRoom)
      } else {
        await axios.post('http://localhost:8000/examRoom', this.currentExamRoom)
      }
      this.closeDialog()
      this.fetchExamRooms()
    },
    async deleteExamRoom(id) {
      if (confirm('Are you sure you want to delete this exam room?')) {
        await axios.delete(`http://localhost:8000/examRoom/${id}`)
        this.fetchExamRooms()
      }
    }
  },
  mounted() {
    this.fetchExamRooms()
  }
}
</script>
