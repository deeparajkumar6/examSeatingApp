<template>
  <v-container>
    <v-card>
      <ClassHeader 
        @add-class="openAddDialog" 
        @import-excel="openImportDialog"
      />
      <ClassTable 
        :classes="classes"
        :loading="loading"
        @edit-class="openEditDialog"
        @delete-class="handleDeleteClass"
      />
    </v-card>

    <!-- Dialogs -->
    <ClassDialog
      v-model="classDialog.show"
      :class-data="classDialog.data"
      :edit-mode="classDialog.editMode"
      @save="handleSaveClass"
    />

    <ExcelImportDialog
      v-model="importDialog.show"
      @import-success="handleImportSuccess"
    />
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useClassesStore } from '@/stores/classes'
import { useAppStore } from '@/stores/app'
import ClassHeader from './ClassHeader.vue'
import ClassTable from './ClassTable.vue'
import ClassDialog from './ClassDialog.vue'
import ExcelImportDialog from './ExcelImportDialog.vue'

const classesStore = useClassesStore()
const appStore = useAppStore()

// Reactive data
const classDialog = ref({
  show: false,
  data: null,
  editMode: false
})

const importDialog = ref({
  show: false
})

// Computed
const classes = computed(() => classesStore.classes)
const loading = computed(() => classesStore.loading)

// Methods
const openAddDialog = () => {
  classDialog.value = {
    show: true,
    data: null,
    editMode: false
  }
}

const openEditDialog = (classData) => {
  classDialog.value = {
    show: true,
    data: { ...classData },
    editMode: true
  }
}

const openImportDialog = () => {
  importDialog.value.show = true
}

const handleSaveClass = async (classData) => {
  try {
    if (classDialog.value.editMode) {
      await classesStore.updateClass(classData.id, classData)
    } else {
      await classesStore.createClass(classData)
    }
    classDialog.value.show = false
  } catch (error) {
    // Error handling is done in the store
  }
}

const handleDeleteClass = async (classId) => {
  if (confirm('Are you sure you want to delete this class?')) {
    await classesStore.deleteClass(classId)
  }
}

const handleImportSuccess = async () => {
  // Refresh classes after successful import
  await classesStore.fetchClasses()
  importDialog.value.show = false
  appStore.showSuccess('Classes imported successfully!')
}

// Lifecycle
onMounted(() => {
  classesStore.fetchClasses()
})
</script>
