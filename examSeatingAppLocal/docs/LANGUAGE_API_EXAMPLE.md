# Language-Based Scheduling API Example

This document shows how the updated API handles language-based class selections.

## API Request Format

### Before (Original)
```json
{
  "date": "2025-07-11",
  "classes": [1, 3],
  "exam_rooms": [1],
  "split": true
}
```

### After (With Language Support)
```json
{
  "date": "2025-07-11",
  "classes": [1, 3],
  "exam_rooms": [1],
  "split": true,
  "language_selections": {
    "1": ["Hindi", "English"],
    "3": ["Hindi"]
  }
}
```

## How Language Selections Work

### Example Scenario
**Class 1 (I B.COM -CS - Shift I)** has students with:
- 25 Hindi-speaking students
- 20 English-speaking students  
- 5 Marathi-speaking students

**Class 3 (II B.COM -CS - Shift I)** has students with:
- 30 Hindi-speaking students
- 15 English-speaking students

### UI Selection
User selects in the UI:
- ✅ I B.COM -CS - Shift I - Hindi (25 students)
- ✅ I B.COM -CS - Shift I - English (20 students)
- ❌ I B.COM -CS - Shift I - Marathi (5 students) [Not selected]
- ✅ II B.COM -CS - Shift I - Hindi (30 students)
- ❌ II B.COM -CS - Shift I - English (15 students) [Not selected]

### API Conversion
The UI converts this to:
```json
{
  "classes": [1, 3],
  "language_selections": {
    "1": ["Hindi", "English"],  // Only Hindi and English from Class 1
    "3": ["Hindi"]              // Only Hindi from Class 3
  }
}
```

### Backend Processing
The backend will:
1. Fetch students from Class 1 WHERE language IN ('Hindi', 'English')
2. Fetch students from Class 3 WHERE language IN ('Hindi')
3. Total students: 25 + 20 + 30 = 75 students (instead of all 95)

## API Response Format

### Enhanced Response
```json
{
  "date": "2025-07-11",
  "seating_arrangement": {
    "A101": [
      {
        "rollNumber": "001",
        "studentName": "Student A",
        "language": "Hindi",
        "classId": 1,
        "className": "I B.COM -CS - Shift I"
      },
      {
        "rollNumber": "002", 
        "studentName": "Student B",
        "language": "English",
        "classId": 1,
        "className": "I B.COM -CS - Shift I"
      },
      {
        "rollNumber": "101",
        "studentName": "Student C", 
        "language": "Hindi",
        "classId": 3,
        "className": "II B.COM -CS - Shift I"
      }
    ]
  },
  "class_summary": {
    "A101": {
      "I B.COM -CS - Shift I": 45,
      "II B.COM -CS - Shift I": 30
    }
  },
  "language_summary": {
    "A101": {
      "Hindi": 55,
      "English": 20
    }
  },
  "class_info": {
    "1": {
      "name": "I B.COM -CS",
      "shift": "I",
      "display_name": "I B.COM -CS - Shift I"
    },
    "3": {
      "name": "II B.COM -CS", 
      "shift": "I",
      "display_name": "II B.COM -CS - Shift I"
    }
  }
}
```

## Benefits

### 1. Precise Student Selection
- Only students with selected languages are included
- No need to process unwanted language groups
- Exact control over exam participation

### 2. Language-Aware Scheduling
- Backend knows exactly which languages are involved
- Can optimize seating based on language distribution
- Enables language-specific resource planning

### 3. Enhanced Reporting
- Language summary shows distribution per room
- Clear visibility of language groups in each room
- Better planning for language-specific materials

### 4. Backward Compatibility
- `language_selections` is optional
- If not provided, all students from selected classes are included
- Existing API calls continue to work

## Implementation Details

### Database Query Enhancement
```sql
-- Without language selection (original)
SELECT rollNumber, studentName, language 
FROM students 
WHERE classId = ?

-- With language selection (new)
SELECT rollNumber, studentName, language 
FROM students 
WHERE classId = ? AND language IN ('Hindi', 'English')
```

### UI to API Mapping
```javascript
// UI Selection (expanded class IDs)
selectedClasses: ['1_hindi', '1_english', '3_hindi']

// API Request (converted)
{
  classes: [1, 3],
  language_selections: {
    1: ['Hindi', 'English'],
    3: ['Hindi']
  }
}
```

### Error Handling
- Invalid language selections are ignored
- Students without language info can be included with `null` in language array
- Empty language selections default to all students

## Testing the API

### Test Request
```bash
curl -X POST "http://localhost:8000/schedule" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-07-11",
    "classes": [1, 3],
    "exam_rooms": [1],
    "split": true,
    "language_selections": {
      "1": ["Hindi", "English"],
      "3": ["Hindi"]
    }
  }'
```

### Expected Behavior
1. Only Hindi and English students from Class 1 are scheduled
2. Only Hindi students from Class 3 are scheduled
3. Marathi students from Class 1 are excluded
4. English students from Class 3 are excluded
5. Response includes language distribution summary

This enhancement provides the granular control needed for language-based exam scheduling while maintaining full backward compatibility with existing API usage.
