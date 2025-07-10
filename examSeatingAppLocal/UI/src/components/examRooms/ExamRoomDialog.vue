<template>
  <v-dialog v-model="dialogModel" max-width="600px" persistent>
    <v-card>
      <v-card-title>
        {{ editMode ? "Edit Exam Room" : "Add New Exam Room" }}
      </v-card-title>

      <v-card-text>
        <v-form ref="form" v-model="valid">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.roomNumber"
                label="Room Number"
                variant="outlined"
                :rules="[rules.required]"
                prepend-inner-icon="mdi-door"
                required
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model.number="formData.roomCapacity"
                label="Room Capacity"
                variant="outlined"
                type="number"
                :rules="[rules.required, rules.positiveNumber]"
                prepend-inner-icon="mdi-account-group"
                required
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.roomFloor"
                label="Floor"
                variant="outlined"
                :rules="[rules.required]"
                prepend-inner-icon="mdi-stairs"
                required
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.roomBuilding"
                label="Building"
                variant="outlined"
                :rules="[rules.required]"
                prepend-inner-icon="mdi-office-building"
                required
              />
            </v-col>
          </v-row>

          <v-alert
            v-if="formData.roomCapacity && formData.roomCapacity < 20"
            type="warning"
            variant="tonal"
            class="mt-3"
          >
            Room capacity is quite low. Consider if this is suitable for exams.
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

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  roomData: {
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
  roomNumber: "",
  roomCapacity: null,
  roomFloor: "",
  roomBuilding: "",
});

const rules = {
  required: (value) => !!value || "This field is required",
  positiveNumber: (value) => value > 0 || "Capacity must be greater than 0",
};

const resetForm = () => {
  formData.value = {
    roomNumber: "",
    roomCapacity: null,
    roomFloor: "",
    roomBuilding: "",
  };
};

// Watch for prop changes
watch(
  () => props.roomData,
  (newData) => {
    if (newData) {
      formData.value = { ...newData };
    } else {
      resetForm();
    }
  },
  { immediate: true }
);

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
