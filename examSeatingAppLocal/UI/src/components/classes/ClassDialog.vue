<template>
  <v-dialog v-model="dialogModel" max-width="800px" persistent>
    <v-card>
      <v-card-title>
        {{ editMode ? "Edit Class" : "Add New Class" }}
      </v-card-title>

      <v-card-text>
        <v-form ref="form" v-model="valid">
          <v-row>
            <v-col cols="12" md="8">
              <v-text-field
                v-model="formData.className"
                label="Class Name"
                variant="outlined"
                :rules="[rules.required]"
                required
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="formData.shift"
                label="Shift (Optional)"
                variant="outlined"
                placeholder="e.g., I, II, Morning, Evening"
              />
            </v-col>
          </v-row>

          <v-divider class="my-4" />

          <div class="d-flex justify-space-between align-center mb-3">
            <h3>Students</h3>
            <v-btn color="primary" size="small" @click="addStudent">
              <v-icon left>mdi-plus</v-icon>
              Add Student
            </v-btn>
          </div>

          <StudentForm
            v-for="(student, index) in formData.students"
            :key="index"
            v-model="formData.students[index]"
            @remove="removeStudent(index)"
          />

          <v-alert
            v-if="formData.students.length === 0"
            type="info"
            variant="tonal"
            class="mt-3"
          >
            No students added yet. Click "Add Student" to add students to this
            class.
          </v-alert>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="save">
          {{ editMode ? "Update" : "Create" }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import StudentForm from "./StudentForm.vue";

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  classData: {
    type: Object,
    default: null,
  },
  editMode: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["update:modelValue", "save"]);

const form = ref(null);
const valid = ref(false);

const dialogModel = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

const formData = ref({
  className: "",
  shift: "",
  students: [],
});

const rules = {
  required: (value) => !!value || "This field is required",
};

const resetForm = () => {
  formData.value = {
    className: "",
    shift: "",
    students: [],
  };
};

// Watch for prop changes
watch(
  () => props.classData,
  (newData) => {
    if (newData) {
      formData.value = {
        ...newData,
        shift: newData.shift || "",
        students: [...(newData.students || [])],
      };
    } else {
      resetForm();
    }
  },
  { immediate: true }
);

const addStudent = () => {
  formData.value.students.push({
    rollNumber: "",
    studentName: "",
    language: "",
    dateOfBirth: "",
  });
};

const removeStudent = (index) => {
  formData.value.students.splice(index, 1);
};

const save = async () => {
  const { valid: isValid } = await form.value.validate();
  if (isValid) {
    emit("save", { ...formData.value });
  }
};

const cancel = () => {
  dialogModel.value = false;
  resetForm();
};
</script>
