<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="text-h5">Create Exam Room Schedule</v-card-title>

      <v-form>
        <!-- Select Exam Date -->
        <v-menu v-model="menu" :close-on-content-click="false">
          <template #activator="{ props }">
            <v-text-field
              v-model="schedule.date"
              label="Select Exam Date"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="props"
            ></v-text-field>
          </template>
          <v-date-picker v-model="schedule.date" @update:modelValue="menu = false"></v-date-picker>
        </v-menu>

        <!-- Select Classes -->
        <v-select
          v-model="schedule.classes"
          :items="classes"
          item-title="className"
          item-value="id"
          label="Select Classes"
          multiple
          chips
        ></v-select>

        <!-- Select Exam Rooms -->
        <v-select
          v-model="schedule.exam_rooms"
          :items="examRooms"
          item-title="roomNumber"
          item-value="id"
          label="Select Exam Rooms"
          multiple
          chips
        ></v-select>

        <!-- Split Students Switch -->
        <v-switch
          v-model="schedule.split"
          label="Split Students into Multiple Rooms"
        ></v-switch>

        <!-- Submit Button -->
        <v-btn color="primary" class="mt-4" @click="generateSchedule" :loading="loading">
          Generate Schedule
        </v-btn>
      </v-form>

      <!-- Display Seating Arrangement as Table -->
      <div ref="scheduleTableContainer" v-if="formattedSchedule.length > 0" class="mt-4">
        <div class="d-flex justify-end mb-2">
          <v-btn color="success" @click="exportToPDF" prepend-icon="mdi-file-export">
            Export to PDF
          </v-btn>
        </div>
        
        <div class="schedule-header text-center py-2">
          <div class="text-h6">DATE: {{ formattedDate }}</div>
          <!-- <div class="text-h6">SESSION: AN</div> -->
        </div>
        
        <div v-for="(room, index) in formattedSchedule" :key="index" class="mb-4">
          <div class="room-header text-center py-2">
            {{ index + 1 }}.Room No: {{ room.roomNumber }}
          </div>
          
          <v-table density="compact">
            <thead>
              <tr>
                <th class="text-center">Class</th>
                <th class="text-center">Roll Numbers</th>
                <th class="text-center">Count</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(classGroup, idx) in room.classGroups" :key="idx">
                <td class="text-center">{{ classGroup.className || '' }}</td>
                <td class="text-center">{{ classGroup.rollRange }}</td>
                <td class="text-center">{{ classGroup.count }}</td>
              </tr>
              <tr class="total-row">
                <td class="text-center font-weight-bold">TOTAL</td>
                <td></td>
                <td class="text-center font-weight-bold">{{ room.totalStudents }}</td>
              </tr>
            </tbody>
          </v-table>
        </div>
      </div>

      <!-- Error Alert -->
      <v-alert
        v-if="error"
        type="error"
        class="mt-4"
        closable
        @click:close="error = ''"
      >
        {{ error }}
      </v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import html2pdf from 'html2pdf.js';

const menu = ref(false);
const classes = ref([]);
const examRooms = ref([]);
const seatingArrangement = ref({});
const formattedSchedule = ref([]);
const loading = ref(false);
const error = ref('');
const scheduleTableContainer = ref(null);

const schedule = ref({
  date: new Date().toISOString().substr(0, 10), // Set default to today
  classes: [],
  exam_rooms: [],
  split: false
});

// Format date as DD.MM.YYYY
const formattedDate = computed(() => {
  if (!schedule.value.date) return '';
  const [year, month, day] = schedule.value.date.split('-');
  return `${day}.${month}.${year}`;
});

onMounted(async () => {
  try {
    const classRes = await axios.get('http://localhost:8000/class');
    classes.value = classRes.data.classes;

    const roomRes = await axios.get('http://localhost:8000/examRoom');
    examRooms.value = roomRes.data.examRooms;
  } catch (err) {
    error.value = 'Failed to load data: ' + (err.response?.data?.detail || err.message);
  }
});

// Helper function to group consecutive roll numbers
const groupConsecutiveNumbers = (numbers) => {
  if (!numbers || numbers.length === 0) return [];
  
  numbers.sort((a, b) => a - b);
  
  const ranges = [];
  let rangeStart = numbers[0];
  let rangeEnd = numbers[0];
  
  for (let i = 1; i < numbers.length; i++) {
    if (numbers[i] === rangeEnd + 1) {
      rangeEnd = numbers[i];
    } else {
      ranges.push({ start: rangeStart, end: rangeEnd });
      rangeStart = numbers[i];
      rangeEnd = numbers[i];
    }
  }
  
  ranges.push({ start: rangeStart, end: rangeEnd });
  return ranges;
};

const generateSchedule = async () => {
  error.value = '';
  seatingArrangement.value = {}; // Clear previous results
  formattedSchedule.value = []; // Clear formatted schedule
  
  // Validation
  if (!schedule.value.date) {
    error.value = 'Please select an exam date';
    return;
  }
  
  if (schedule.value.classes.length === 0) {
    error.value = 'Please select at least one class';
    return;
  }
  
  if (schedule.value.exam_rooms.length === 0) {
    error.value = 'Please select at least one exam room';
    return;
  }
  
  try {
    loading.value = true;
    
    // Make sure the field names match exactly what your API expects
    const payload = {
      date: schedule.value.date,
      classes: schedule.value.classes,
      exam_rooms: schedule.value.exam_rooms,
      split: schedule.value.split
    };
    
    const res = await axios.post('http://localhost:8000/schedule', payload);
    
    if (res.data.seating_arrangement) {
      seatingArrangement.value = res.data.seating_arrangement;
      
      // Process the seating arrangement to create formatted display
      const classMap = {};
      classes.value.forEach(cls => {
        classMap[cls.id] = cls;
      });
      
      const roomMap = {};
      examRooms.value.forEach(room => {
        roomMap[room.id] = room;
      });
      
      // Group students by class for each room
      const formattedRooms = [];
      
      for (const [roomNumber, students] of Object.entries(res.data.seating_arrangement)) {
        const roomData = {
          roomNumber,
          totalStudents: students.length,
          classGroups: []
        };
        
        // Group students by class
        const studentsByClass = {};
        
        students.forEach(student => {
          // Find which class this student belongs to
          for (const cls of classes.value) {
            if (student >= cls.startRollNumber && student <= cls.endRollNumber) {
              if (!studentsByClass[cls.id]) {
                studentsByClass[cls.id] = {
                  classId: cls.id,
                  className: cls.className,
                  students: []
                };
              }
              studentsByClass[cls.id].students.push(student);
              break;
            }
          }
        });
        
        // Create class groups with roll number ranges
        for (const classGroup of Object.values(studentsByClass)) {
          const ranges = groupConsecutiveNumbers(classGroup.students);
          
          ranges.forEach(range => {
            roomData.classGroups.push({
              className: classGroup.className,
              rollRange: `${range.start}-${range.end}`,
              count: range.end - range.start + 1
            });
          });
        }
        
        formattedRooms.push(roomData);
      }
      
      formattedSchedule.value = formattedRooms;
    } else {
      throw new Error('No seating arrangement data in response');
    }
  } catch (err) {
    console.error('Error:', err);
    error.value = 'Failed to generate schedule: ' + (err.response?.data?.detail || err.message);
  } finally {
    loading.value = false;
  }
};

const exportToPDF = () => {
  if (!scheduleTableContainer.value) return;
  
  const element = scheduleTableContainer.value;
  const opt = {
    margin: 10,
    filename: `exam_schedule_${schedule.value.date}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  };
  
  html2pdf().set(opt).from(element).save();
};
</script>

<style scoped>
.schedule-header {
  background-color: #ffffff;
  border: 1px solid #000;
  border-bottom: none;
  color: #ff0000;
  font-weight: bold;
}

.room-header {
  background-color: #b8b5e0;
  border: 1px solid #000;
  border-bottom: none;
  font-weight: bold;
}

.v-table {
  border: 1px solid #000;
}

.total-row {
  background-color: #f5f5f5;
}

@media print {
  .v-btn {
    display: none !important;
  }
}
</style>