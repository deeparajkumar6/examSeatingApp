# Language-Based Class Selection Guide

This guide explains the new language-based class selection feature that allows you to select specific language groups from classes rather than entire classes.

## Overview

The system now expands classes into separate selectable entries based on the languages of students within each class. This provides granular control over which language groups participate in exams.

## How It Works

### Class Expansion
Each class is automatically expanded into multiple selectable entries based on student languages:

**Original Class:**
```javascript
{
  id: 1,
  className: 'I B.COM -CS',
  shift: 'I',
  students: [
    { rollNumber: '001', name: 'Student A', language: 'Hindi' },
    { rollNumber: '002', name: 'Student B', language: 'Hindi' },
    { rollNumber: '003', name: 'Student C', language: 'English' },
    { rollNumber: '004', name: 'Student D', language: 'English' },
    { rollNumber: '005', name: 'Student E', language: 'Marathi' }
  ]
}
```

**Expanded Entries:**
```javascript
[
  {
    id: '1_hindi',
    originalId: 1,
    displayName: 'I B.COM -CS - Shift I - Hindi',
    language: 'Hindi',
    students: [
      { rollNumber: '001', name: 'Student A', language: 'Hindi' },
      { rollNumber: '002', name: 'Student B', language: 'Hindi' }
    ]
  },
  {
    id: '1_english',
    originalId: 1,
    displayName: 'I B.COM -CS - Shift I - English',
    language: 'English',
    students: [
      { rollNumber: '003', name: 'Student C', language: 'English' },
      { rollNumber: '004', name: 'Student D', language: 'English' }
    ]
  },
  {
    id: '1_marathi',
    originalId: 1,
    displayName: 'I B.COM -CS - Shift I - Marathi',
    language: 'Marathi',
    students: [
      { rollNumber: '005', name: 'Student E', language: 'Marathi' }
    ]
  }
]
```

## Selection Interface

### Class Selection Dialog
The selection dialog now shows:
- **Separate rows** for each language group within a class
- **Student count** for each language group
- **Language indicator** in the subtitle
- **Search functionality** across class names, shifts, and languages

### Example Display
```
☐ I B.COM -CS - Shift I - Hindi
  2 students • Hindi

☐ I B.COM -CS - Shift I - English  
  2 students • English

☐ I B.COM -CS - Shift I - Marathi
  1 student • Marathi

☐ I B.COM -CS - Shift II - Hindi
  3 students • Hindi
```

## Selection Benefits

### 1. Granular Control
- Select only specific language groups from classes
- Mix and match language groups as needed
- Exclude certain language groups if required

### 2. Flexible Exam Planning
- Create language-specific exam sessions
- Accommodate different language requirements
- Plan resources based on actual language needs

### 3. Better Resource Allocation
- Know exact student counts per language
- Plan for language-specific materials
- Optimize room assignments

## Usage Examples

### Scenario 1: Hindi-Only Exam
Select only Hindi language groups:
- ✅ I B.COM -CS - Shift I - Hindi (25 students)
- ✅ I B.COM -CS - Shift II - Hindi (30 students)
- ✅ II B.COM -CS - Shift I - Hindi (20 students)

**Result:** 75 Hindi-speaking students across 3 language groups

### Scenario 2: Mixed Language Exam
Select multiple language groups:
- ✅ I B.COM -CS - Shift I - Hindi (25 students)
- ✅ I B.COM -CS - Shift I - English (20 students)
- ✅ II BCA - Shift I - Marathi (15 students)

**Result:** 60 students across 3 languages (Hindi, English, Marathi)

### Scenario 3: Class-Specific Language Selection
From "I B.COM -CS - Shift I", select only:
- ✅ Hindi group (25 students)
- ❌ English group (20 students) - excluded

## Selection Summary

The interface provides comprehensive selection information:

### Summary Statistics
- **Total Students:** 85 students
- **Languages:** 3 languages (Hindi, English, Marathi)
- **Selections:** 4 language groups
- **Classes:** 2 original classes

### Detailed Breakdown
| Class | Language | Students |
|-------|----------|----------|
| I B.COM -CS - Shift I | Hindi | 25 |
| I B.COM -CS - Shift I | English | 20 |
| II B.COM -CS - Shift I | Hindi | 20 |
| II BCA - Shift I | Marathi | 20 |

## Quick Selection Options

### By Language
- **Select Hindi Classes:** Selects all Hindi language groups
- **Select English Classes:** Selects all English language groups
- **Select Marathi Classes:** Selects all Marathi language groups

### By Shift
- **Select Shift I:** Selects all language groups from Shift I classes
- **Select Shift II:** Selects all language groups from Shift II classes

### By Class
- **Select All:** Selects all available language groups

## Search Functionality

### Search Examples
- **"Hindi"** → Shows all Hindi language groups
- **"I B.COM"** → Shows all language groups from I B.COM classes
- **"Shift I"** → Shows all language groups from Shift I
- **"English"** → Shows all English language groups

## API Integration

### Request Format
The system converts expanded selections back to API-compatible format:

```javascript
// UI Selection (expanded IDs)
selectedClasses: ['1_hindi', '1_english', '2_marathi']

// API Request (converted)
{
  classes: [1, 2], // Original class IDs
  languageSelections: {
    1: ['Hindi', 'English'], // Languages selected from class 1
    2: ['Marathi']           // Languages selected from class 2
  }
}
```

### Backend Processing
The backend can use this information to:
1. Fetch only students with selected languages from each class
2. Generate seating arrangements with language considerations
3. Create language-specific reports and documents

## Benefits Summary

### 1. **Precision**
- Select exactly the student groups you need
- No more including unwanted language groups
- Fine-grained control over exam participation

### 2. **Flexibility**
- Mix languages across different classes
- Create custom language combinations
- Adapt to specific exam requirements

### 3. **Efficiency**
- Reduce unnecessary student processing
- Optimize resource allocation
- Streamline exam management

### 4. **Clarity**
- Clear visibility of language distribution
- Easy identification of selected groups
- Comprehensive selection summaries

This language-based selection system provides the flexibility needed to manage diverse student populations while maintaining clear control over exam participation at the language group level.
