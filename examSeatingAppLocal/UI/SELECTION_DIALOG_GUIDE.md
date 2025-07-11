# Selection Dialog Guide

This guide explains the new enhanced selection dialog functionality for classes and exam rooms in the scheduler.

## Overview

The new selection system provides:
- **Dialog-based selection** with search functionality
- **Multi-select capabilities** with visual feedback
- **Quick selection options** for common scenarios
- **Capacity analysis** and recommendations
- **Enhanced user experience** with better organization

## Components

### 1. SelectionDialog.vue
A reusable dialog component that provides:
- Search functionality to filter items
- Multi-select with checkboxes
- Visual selection indicators
- Apply/Cancel actions
- Dynamic content based on item type (class/room)

### 2. EnhancedClassSelector.vue
Enhanced class selection with:
- Current selection display with chips
- Total student count
- Quick selection options:
  - Select all classes
  - Select by shift (1 or 2)
  - Select large classes (30+ students)
- Clear all functionality
- Validation support

### 3. EnhancedRoomSelector.vue
Enhanced room selection with:
- Current selection display with capacity-colored chips
- Total capacity calculation
- Room details table
- Quick selection options:
  - Select all rooms
  - Select large rooms (50+ capacity)
  - Select by building
  - Auto-optimize selection
- Building-based selection dialog
- Capacity status indicators

### 4. CapacityAnalysis.vue
Provides comprehensive analysis:
- Student vs. capacity comparison
- Utilization percentage with progress bar
- Detailed breakdown by class and room
- Color-coded status indicators
- Recommendations based on capacity ratio

## Features

### Search Functionality
- **Case-insensitive search** across relevant fields
- **Real-time filtering** as you type
- **Multiple field search**:
  - **For Classes**: class name, shift, and language
  - **For Rooms**: room number, building, and floor

### Multi-Select Options
- **Individual selection** by clicking items or checkboxes
- **Bulk selection** with quick action buttons
- **Visual feedback** with selected item highlighting
- **Selection counter** in dialog and summary

### Quick Actions

#### For Classes:
- **Select All**: Selects all available classes
- **Select Shift 1/2**: Filters and selects classes by shift
- **Select by Language**: Dynamically shows options for each available language (e.g., "Select Hindi Classes", "Select English Classes")

#### For Rooms:
- **Select All**: Selects all available rooms
- **Select Large Rooms**: Selects rooms with 50+ capacity
- **Select by Building**: Opens building selection dialog
- **Auto-Optimize**: Automatically selects optimal room combination

### Capacity Analysis
- **Real-time calculations** as selections change
- **Color-coded indicators**:
  - Green: Excellent capacity (≤60% utilization)
  - Orange: Good capacity (61-80% utilization)
  - Red: Tight/Overcapacity (>80% utilization)
- **Smart recommendations** based on selection

## Usage

### Basic Usage
```vue
<template>
  <!-- Class Selection -->
  <EnhancedClassSelector
    v-model="selectedClasses"
    :classes="availableClasses"
  />
  
  <!-- Room Selection -->
  <EnhancedRoomSelector
    v-model="selectedRooms"
    :exam-rooms="availableRooms"
    :total-students="totalStudents"
  />
  
  <!-- Capacity Analysis -->
  <CapacityAnalysis
    :selected-classes="selectedClassesData"
    :selected-rooms="selectedRoomsData"
    :total-students="totalStudents"
    :total-capacity="totalCapacity"
  />
</template>
```

### With Validation
```vue
<template>
  <EnhancedClassSelector
    ref="classSelector"
    v-model="selectedClasses"
    :classes="availableClasses"
    :required="true"
  />
</template>

<script setup>
const classSelector = ref(null)

const validateSelection = () => {
  return classSelector.value?.validate() ?? true
}
</script>
```

## Data Structure

### Class Object
```javascript
{
  id: number,
  className: string,
  shift: number | null,
  language: string | null, // Language of instruction (e.g., "Hindi", "English")
  students: Array<{
    id: number,
    name: string,
    // ... other student properties
  }>
}
```

### Display Format
Classes are displayed with the following format:
- **Without language**: `I B.COM -CS - Shift I`
- **With language**: `I B.COM -CS - Shift I - Language Hindi`
- **No shift, with language**: `I BCA - Language English`
- **No language specified**: `I B.SC Mathematics`

The language information is only displayed when available in the class data.

### Room Object
```javascript
{
  id: number,
  roomNumber: string,
  roomBuilding: string,
  roomFloor: number,
  roomCapacity: number
}
```

## Styling

The components use Vuetify's design system with:
- **Consistent color coding** for capacity indicators
- **Responsive design** for mobile and desktop
- **Smooth animations** for dialog transitions
- **Accessible design** with proper ARIA labels

## Demo

A demo component is available at `src/components/demo/SelectionDialogDemo.vue` that showcases:
- Mock data generation
- All selection features
- Capacity analysis
- Real-time updates

## Integration

The enhanced selectors are integrated into the main scheduler form (`ScheduleForm.vue`) and provide:
- **Backward compatibility** with existing data structures
- **Enhanced validation** with visual feedback
- **Improved user experience** with better organization
- **Real-time capacity analysis** for better decision making

## Benefits

1. **Improved Usability**: Dialog-based selection is more intuitive
2. **Better Organization**: Clear separation of selected vs. available items
3. **Enhanced Search**: Quick filtering reduces selection time
4. **Smart Recommendations**: Helps users make better capacity decisions
5. **Visual Feedback**: Clear indication of selection status and capacity
6. **Flexible Selection**: Multiple ways to select items efficiently
