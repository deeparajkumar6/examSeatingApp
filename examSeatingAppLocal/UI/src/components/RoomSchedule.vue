<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="text-h5"> Create Exam Room Schedule </v-card-title>

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
            />
          </template>
          <v-date-picker
            v-model="schedule.date"
            @update:model-value="menu = false"
          />
        </v-menu>

        <!-- Select Classes -->
        <v-select
          v-model="schedule.classes"
          chips
          item-title="classDisplayName"
          item-value="id"
          :items="classes"
          label="Select Classes"
          multiple
        >
          <template #item="{ props, item }">
            <v-list-item v-bind="props">
              <v-list-item-title>{{ item.raw.className }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ item.raw.students.length }} students
              </v-list-item-subtitle>
            </v-list-item>
          </template>
        </v-select>

        <!-- Select Exam Rooms -->
        <v-select
          v-model="schedule.exam_rooms"
          chips
          item-title="roomDisplayName"
          item-value="id"
          :items="examRooms"
          label="Select Exam Rooms"
          multiple
        >
          <template #item="{ props, item }">
            <v-list-item v-bind="props">
              <v-list-item-title>{{ item.raw.roomNumber }}</v-list-item-title>
              <v-list-item-subtitle>
                Capacity: {{ item.raw.roomCapacity }} | Floor:
                {{ item.raw.roomFloor }} | Building:
                {{ item.raw.roomBuilding }}
              </v-list-item-subtitle>
            </v-list-item>
          </template>
        </v-select>

        <!-- Split Students Switch -->
        <v-switch
          v-model="schedule.split"
          label="Split Students into Multiple Rooms"
        />

        <!-- Submit Button -->
        <v-btn
          class="mt-4"
          color="primary"
          :loading="loading"
          @click="generateSchedule"
        >
          Generate Schedule
        </v-btn>
      </v-form>

      <!-- Display Seating Arrangement as Table -->
      <div v-if="formattedSchedule.length > 0" class="mt-4">
        <div class="d-flex justify-end mb-2 no-print">
          <v-btn
            color="success"
            prepend-icon="mdi-file-export"
            @click="exportToPDF"
          >
            Export to PDF
          </v-btn>
        </div>

        <!-- PDF Content Container -->
        <div ref="scheduleTableContainer" class="pdf-content">
          <!-- College Header (will appear on all pages) -->
          <div class="college-header">
            <div class="header-content">
              <div class="logo-section">
                <img
                  v-if="!logoError"
                  alt="College Logo"
                  class="college-logo"
                  src="/logo.png"
                  @error="handleLogoError"
                >
                <div v-else class="logo-placeholder">
                  <v-icon color="#000" size="60"> mdi-school </v-icon>
                </div>
              </div>
              <div class="college-info">
                <h1 class="college-name">
                  {{ collegeName }}
                </h1>
                <h2 class="exam-title">Examination Seating Arrangement</h2>
                <div class="exam-date">DATE: {{ formattedDate }}</div>
              </div>
            </div>
            <hr class="header-divider">
          </div>

          <!-- Schedule Content -->
          <div class="schedule-content">
            <div
              v-for="(room, index) in formattedSchedule"
              :key="index"
              class="room-section"
            >
              <div class="room-header">
                <h3>{{ index + 1 }}. Room No: {{ room.roomNumber }}</h3>
              </div>

              <v-table class="schedule-table" density="compact">
                <thead>
                  <tr>
                    <th class="text-center table-header">Class</th>
                    <th class="text-center table-header">Roll Numbers</th>
                    <th class="text-center table-header">Count</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(classGroup, idx) in room.classGroups" :key="idx">
                    <td class="text-center table-cell">
                      {{ classGroup.className || "" }}
                    </td>
                    <td class="text-center table-cell">
                      {{ classGroup.rollRange }}
                    </td>
                    <td class="text-center table-cell">
                      {{ classGroup.count }}
                    </td>
                  </tr>
                  <tr class="total-row">
                    <td class="text-center table-cell font-weight-bold">
                      TOTAL
                    </td>
                    <td class="table-cell" />
                    <td class="text-center table-cell font-weight-bold">
                      {{ room.totalStudents }}
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </div>
          </div>
        </div>
      </div>

      <!-- Error Alert -->
      <v-alert
        v-if="error"
        class="mt-4"
        closable
        type="error"
        @click:close="error = ''"
      >
        {{ error }}
      </v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import axios from 'axios';
import html2pdf from 'html2pdf.js';

const menu = ref(false);
const classes = ref([]);
const examRooms = ref([]);
const seatingArrangement = ref({});
const formattedSchedule = ref([]);
const loading = ref(false);

// College configuration - you can modify these values
const collegeName = ref('Shahun Jain College for Women');
const logoError = ref(false);

// You can customize these values:
// - Change collegeName.value to your college name
// - Replace /logo.png with your college logo file
// - Logo should be placed in the public folder
const error = ref('');
const scheduleTableContainer = ref(null);

const schedule = ref({
  date: new Date().toISOString().substr(0, 10), // Set default to today
  classes: [],
  exam_rooms: [],
  split: false,
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
    classes.value = classRes.data.classes.map(cls => ({
      ...cls,
      classDisplayName: `${cls.className} (${cls.students.length} students)`,
    }));

    const roomRes = await axios.get('http://localhost:8000/examRoom');
    examRooms.value = roomRes.data.examRooms.map(room => ({
      ...room,
      roomDisplayName: `${room.roomNumber} (Capacity: ${room.roomCapacity})`,
    }));
  } catch (err) {
    error.value =
      'Failed to load data: ' + (err.response?.data?.detail || err.message);
  }
});

// Helper function to group consecutive roll numbers
const groupConsecutiveNumbers = rollNumbers => {
  if (!rollNumbers || rollNumbers.length === 0) return [];

  // Sort roll numbers - handle both numeric and string roll numbers
  const sortedRolls = rollNumbers.sort((a, b) => {
    const aNum = parseInt(a);
    const bNum = parseInt(b);
    if (!isNaN(aNum) && !isNaN(bNum)) {
      return aNum - bNum;
    }
    return a.toString().localeCompare(b.toString());
  });

  // For non-numeric roll numbers, just return them as individual items
  const firstRoll = sortedRolls[0];
  if (isNaN(parseInt(firstRoll))) {
    return sortedRolls.map(roll => ({ start: roll, end: roll }));
  }

  // Group consecutive numeric roll numbers
  const ranges = [];
  let rangeStart = parseInt(sortedRolls[0]);
  let rangeEnd = parseInt(sortedRolls[0]);

  for (let i = 1; i < sortedRolls.length; i++) {
    const current = parseInt(sortedRolls[i]);
    if (current === rangeEnd + 1) {
      rangeEnd = current;
    } else {
      ranges.push({ start: rangeStart, end: rangeEnd });
      rangeStart = current;
      rangeEnd = current;
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

    const payload = {
      date: schedule.value.date,
      classes: schedule.value.classes,
      exam_rooms: schedule.value.exam_rooms,
      split: schedule.value.split,
    };

    const res = await axios.post('http://localhost:8000/schedule', payload);

    if (res.data.seating_arrangement) {
      seatingArrangement.value = res.data.seating_arrangement;

      // Create class lookup map
      const classMap = {};
      classes.value.forEach(cls => {
        classMap[cls.id] = cls;
        // Create a map of roll numbers to class for quick lookup
        cls.students.forEach(student => {
          classMap[student.rollNumber] = cls;
        });
      });

      // Process the seating arrangement to create formatted display
      const formattedRooms = [];

      for (const [roomNumber, students] of Object.entries(
        res.data.seating_arrangement
      )) {
        const roomData = {
          roomNumber,
          totalStudents: students.length,
          classGroups: [],
        };

        // Group students by class
        const studentsByClass = {};

        students.forEach(rollNumber => {
          // Find which class this student belongs to
          const studentClass = classMap[rollNumber];
          if (studentClass) {
            if (!studentsByClass[studentClass.id]) {
              studentsByClass[studentClass.id] = {
                classId: studentClass.id,
                className: studentClass.className,
                students: [],
              };
            }
            studentsByClass[studentClass.id].students.push(rollNumber);
          }
        });

        // Format each class group
        for (const classGroup of Object.values(studentsByClass)) {
          const ranges = groupConsecutiveNumbers(classGroup.students);
          const rollRange = ranges
            .map(range => {
              if (range.start === range.end) {
                return range.start.toString();
              } else {
                return `${range.start}-${range.end}`;
              }
            })
            .join(', ');

          roomData.classGroups.push({
            className: classGroup.className,
            rollRange,
            count: classGroup.students.length,
          });
        }

        // Sort class groups by class name
        roomData.classGroups.sort((a, b) =>
          a.className.localeCompare(b.className)
        );

        formattedRooms.push(roomData);
      }

      // Sort rooms by room number
      formattedRooms.sort((a, b) => a.roomNumber.localeCompare(b.roomNumber));
      formattedSchedule.value = formattedRooms;
    }
  } catch (err) {
    error.value =
      'Failed to generate schedule: ' +
      (err.response?.data?.detail || err.message);
  } finally {
    loading.value = false;
  }
};

const exportToPDF = () => {
  const element = scheduleTableContainer.value;
  const opt = {
    margin: [0.5, 0.5, 1, 0.5], // top, left, bottom, right margins in inches
    filename: `exam-schedule-${schedule.value.date}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: {
      scale: 2,
      useCORS: true,
      allowTaint: true,
    },
    jsPDF: {
      unit: 'in',
      format: 'a4',
      orientation: 'portrait',
    },
    pagebreak: {
      mode: ['avoid-all', 'css', 'legacy'],
      before: '.room-section',
      after: '.room-section',
    },
  };

  // Add custom CSS for PDF generation
  const style = document.createElement('style');
  style.textContent = `
    @media print {
      .no-print { display: none !important; }
      .pdf-content { 
        font-family: Arial, sans-serif;
        color: #000;
      }
      .college-header {
        position: running(header);
        border-bottom: 2px solid #333;
        margin-bottom: 20px;
      }
      @page {
        @bottom-center {
          content: "Page " counter(page) " of " counter(pages);
          font-size: 10px;
          color: #666;
        }
        @top-center {
          content: element(header);
        }
        margin-top: 120px;
        margin-bottom: 40px;
      }
    }
  `;
  document.head.appendChild(style);

  html2pdf()
    .set(opt)
    .from(element)
    .save()
    .then(() => {
      // Clean up the added style
      document.head.removeChild(style);
    });
};

const handleLogoError = () => {
  logoError.value = true;
};
</script>

<style scoped>
/* Screen styles */
.schedule-header {
  background-color: transparent;
  border: 1px solid #000;
  font-weight: bold;
}

.room-header {
  background-color: transparent;
  border: 1px solid #000;
  font-weight: bold;
  padding: 12px;
  margin: 16px 0 8px 0;
}

.room-header h3 {
  margin: 0;
  font-size: 1.2em;
  color: #000;
}

.total-row {
  background-color: transparent;
  font-weight: bold;
}

.total-row .table-cell {
  background-color: transparent !important;
  color: #000 !important;
  font-weight: bold !important;
}

.v-table {
  border: 1px solid #000;
}

.v-table th,
.v-table td {
  border: 1px solid #000 !important;
  padding: 8px !important;
}

/* PDF-specific styles */
.pdf-content {
  background: white;
  color: black;
}

.college-header {
  margin-bottom: 30px;
  page-break-inside: avoid;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
  gap: 20px;
}

.logo-section {
  flex-shrink: 0;
}

.college-logo {
  width: 80px;
  height: 80px;
  object-fit: contain;
}

.logo-placeholder {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #000;
  border-radius: 50%;
  background-color: transparent;
}

.college-info {
  text-align: center;
  flex-grow: 1;
}

.college-name {
  font-size: 24px;
  font-weight: bold;
  margin: 0 0 8px 0;
  color: #ab3d31;
  text-transform: uppercase;
}

.exam-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #000063;
}

.exam-date {
  font-size: 16px;
  font-weight: 500;
  color: #424242;
}

.header-divider {
  border: none;
  border-top: 2px solid #000;
  margin: 10px 0 0 0;
}

.room-section {
  margin-bottom: 30px;
  page-break-inside: avoid;
}

.schedule-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.table-header {
  background-color: transparent !important;
  font-weight: bold !important;
  border: 1px solid #000 !important;
  padding: 10px !important;
  color: #000 !important;
}

.table-cell {
  border: 1px solid #000 !important;
  padding: 8px !important;
  background-color: transparent !important;
}

/* Print-specific styles */
@media print {
  .no-print {
    display: none !important;
  }

  .pdf-content {
    font-family: Arial, sans-serif;
    color: #000 !important;
    background: white !important;
  }

  .college-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: white;
    z-index: 1000;
  }

  .schedule-content {
    margin-top: 140px;
  }

  .room-section {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  .schedule-table {
    page-break-inside: auto;
  }

  .schedule-table tr {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  @page {
    margin: 0.5in;
    @bottom-center {
      content: "Page " counter(page);
      font-size: 10px;
      color: #666;
    }
  }
}

/* Hide logo if it fails to load */
.college-logo[src=""] {
  display: none;
}
</style>
