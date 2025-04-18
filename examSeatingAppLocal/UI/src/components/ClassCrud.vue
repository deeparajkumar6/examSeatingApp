<template>
    <v-container>
      <v-card>
        <div class="d-flex justify-space-between align-center pa-3">
        <v-card-title>Class Management</v-card-title>
        <v-btn color="primary" @click="openAddDialog">Add Class</v-btn>
      </div>
        <v-card-text>
          
          <v-data-table :items="classes" :headers="headers">
            <template #item.actions="{ item }">
              <v-btn variant="flat" icon @click="openEditDialog(item)">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon  variant="flat" @click="deleteClass(item.id)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
  
      <!-- Add/Edit Class Dialog -->
      <v-dialog v-model="dialog" max-width="500">
        <v-card>
          <v-card-title>{{ isEditing ? 'Edit Class' : 'Add New Class' }}</v-card-title>
          <v-card-text>
            <v-text-field variant="outlined" v-model="currentClass.className" label="Class Name"></v-text-field>
            <v-text-field variant="outlined" v-model.number="currentClass.startRollNumber" label="Start Roll No" type="number"></v-text-field>
            <v-text-field variant="outlined" v-model.number="currentClass.endRollNumber" label="End Roll No" type="number"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="closeDialog">Cancel</v-btn>
            <v-btn color="primary" @click="saveClass">{{ isEditing ? 'Update' : 'Add' }}</v-btn>
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
        classes: [],
        dialog: false,
        isEditing: false,
        currentClass: {
          id: null,
          className: '',
          startRollNumber: 1,
          endRollNumber: 10
        },
        headers: [
          // { title: 'ID', key: 'id' },
          { title: 'Class Name', key: 'className' },
          { title: 'Start Roll No', key: 'startRollNumber' },
          { title: 'End Roll No', key: 'endRollNumber' },
          { title: 'Actions', key: 'actions', sortable: false }
        ]
      }
    },
    methods: {
      async fetchClasses() {
        const res = await axios.get('http://localhost:8000/class')
        this.classes = res.data.classes
      },
      openAddDialog() {
        this.isEditing = false
        this.currentClass = { id: null, className: '', startRollNumber: 1, endRollNumber: 10 }
        this.dialog = true
      },
      openEditDialog(item) {
        this.isEditing = true
        this.currentClass = { ...item }
        this.dialog = true
      },
      closeDialog() {
        this.dialog = false
      },
      async saveClass() {
        if (this.isEditing) {
          await axios.put(`http://localhost:8000/class/${this.currentClass.id}`, this.currentClass)
        } else {
          await axios.post('http://localhost:8000/class', this.currentClass)
        }
        this.closeDialog()
        this.fetchClasses()
      },
      async deleteClass(id) {
        if (confirm('Are you sure you want to delete this class?')) {
          await axios.delete(`http://localhost:8000/class/${id}`)
          this.fetchClasses()
        }
      }
    },
    mounted() {
      this.fetchClasses()
    }
  }
  </script>
  