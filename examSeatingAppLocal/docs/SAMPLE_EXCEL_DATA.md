# Sample Excel Data Files

This directory contains comprehensive sample Excel files for testing the exam seating arrangement system with various class configurations.

## 📁 File Structure

All sample Excel files are located in the `sample_data/` folder:

```
sample_data/
├── sample_I_B.COM_Shift_I.xlsx      # 1st Year BCOM Shift I (25 students) ✅ With Language
├── sample_I_B.COM_Shift_II.xlsx     # 1st Year BCOM Shift II (28 students) ✅ With Language
├── sample_II_B.COM_Shift_I.xlsx     # 2nd Year BCOM Shift I (22 students)
├── sample_II_B.COM_Shift_II.xlsx    # 2nd Year BCOM Shift II (26 students)
├── sample_III_B.COM_Shift_I.xlsx    # 3rd Year BCOM Shift I (20 students)
├── sample_III_B.COM_Shift_II.xlsx   # 3rd Year BCOM Shift II (24 students)
├── sample_I_BSC_CS_Shift_I.xlsx     # 1st Year BSC CS Shift I (30 students) ✅ With Language
├── sample_I_BSC_CS_Shift_II.xlsx    # 1st Year BSC CS Shift II (27 students) ✅ With Language
├── sample_II_BSC_CS_Shift_I.xlsx    # 2nd Year BSC CS Shift I (23 students)
├── sample_II_BSC_CS_Shift_II.xlsx   # 2nd Year BSC CS Shift II (25 students)
├── sample_III_BSC_CS_Shift_I.xlsx   # 3rd Year BSC CS Shift I (21 students)
├── sample_III_BSC_CS_Shift_II.xlsx  # 3rd Year BSC CS Shift II (29 students)
├── sample_I_MSC_CS_Shift_I.xlsx     # 1st Year MSC CS Shift I (18 students)
├── sample_I_MSC_CS_Shift_II.xlsx    # 1st Year MSC CS Shift II (20 students)
├── sample_II_MSC_CS_Shift_I.xlsx    # 2nd Year MSC CS Shift I (16 students)
└── sample_II_MSC_CS_Shift_II.xlsx   # 2nd Year MSC CS Shift II (19 students)
```

## 📊 Data Specifications

### Class Categories

#### 1. **B.COM (Bachelor of Commerce)**
- **1st Year**: 25-28 students per shift ✅ **With Language Column**
- **2nd Year**: 22-26 students per shift
- **3rd Year**: 20-24 students per shift

#### 2. **BSC CS (Bachelor of Science - Computer Science)**
- **1st Year**: 27-30 students per shift ✅ **With Language Column**
- **2nd Year**: 23-25 students per shift
- **3rd Year**: 21-29 students per shift

#### 3. **MSC CS (Master of Science - Computer Science)**
- **1st Year**: 18-20 students per shift
- **2nd Year**: 16-19 students per shift

### Language Distribution (1st Year Only)

For 1st year students, the language column includes:
- **Hindi**: ~40% of students
- **Sanskrit**: ~30% of students  
- **Tamil**: ~30% of students

### Student Data Format

#### With Language Column (1st Year Classes)
| S.No | Register Number | Student Name | Department | Shift | Language |
|------|----------------|--------------|------------|-------|----------|
| 1    | 12230001001    | Myra Mishra  | I B.COM    | I     | Sanskrit |
| 2    | 12230001002    | Krishna Pandey| I B.COM   | I     | Tamil    |

#### Without Language Column (2nd/3rd Year Classes)
| S.No | Register Number | Student Name | Department | Shift |
|------|----------------|--------------|------------|-------|
| 1    | 22230001001    | Reyansh Jain | II B.COM   | I     |
| 2    | 22230001002    | Shlok Gupta  | II B.COM   | I     |

## 🎯 Usage Instructions

### For Testing Excel Import

1. **Test Language-Based Filtering**:
   - Use 1st year files (I_B.COM, I_BSC_CS)
   - These have language columns for testing language-based scheduling

2. **Test Without Language Column**:
   - Use 2nd/3rd year files or MSC files
   - These test the fixed import functionality for missing language columns

3. **Test Mixed Scenarios**:
   - Import multiple files with different language configurations
   - Test scheduling with some classes having language data, others not

### For Exam Scheduling

1. **Language-Based Exams**:
   - Schedule exams for 1st year classes
   - Filter by specific languages (Hindi, Sanskrit, Tamil)

2. **General Exams**:
   - Schedule exams for 2nd/3rd year classes
   - No language filtering required

3. **Mixed Scheduling**:
   - Combine different year classes in same exam
   - Test capacity management across different class sizes

## 📋 Register Number Format

Register numbers follow the pattern: `YYCCCCSSSS`
- **YY**: Year of study (12=1st year, 22=2nd year, 32=3rd year, 42=MSC)
- **CCCC**: Course code (3001=BCOM, 3002=BSC CS, 3003=MSC CS)
- **S**: Shift (1=Shift I, 2=Shift II)
- **SSS**: Serial number (001-999)

**Examples**:
- `12230001001`: 1st Year BCOM Shift I Student #1
- `22230002015`: 2nd Year BSC CS Shift II Student #15
- `42230003008`: MSC CS Shift I Student #8

## 🧪 Testing Scenarios

### Scenario 1: Language-Based Scheduling
```
Classes: I B.COM Shift I, I BSC CS Shift I
Language Filter: Hindi only
Expected: Only Hindi-speaking students from both classes
```

### Scenario 2: Mixed Year Scheduling
```
Classes: I B.COM Shift I (with language), II B.COM Shift I (without language)
Language Filter: Tamil for I B.COM
Expected: Tamil students from I B.COM + All students from II B.COM
```

### Scenario 3: Capacity Testing
```
Classes: I BSC CS Shift I (30 students), II BSC CS Shift II (25 students)
Room Capacity: 40 seats
Expected: Room splitting or capacity warning
```

## 🔧 Data Generation Details

- **Names**: Realistic Indian names with variety
- **Ages**: Age-appropriate for each year of study
- **Dates of Birth**: Realistic birth dates in DD/MM/YYYY format
- **Languages**: Random distribution among Hindi, Sanskrit, Tamil
- **Register Numbers**: Systematic numbering based on class and shift

## ✅ Quality Assurance

All sample files have been tested for:
- ✅ Proper Excel format compatibility
- ✅ Correct column structure
- ✅ Valid data types and formats
- ✅ Language column presence/absence as specified
- ✅ Realistic student counts per class
- ✅ Date format consistency
- ✅ Register number uniqueness

These sample files provide comprehensive test data for all features of the exam seating arrangement system, including language-based filtering, capacity management, and mixed class scheduling scenarios.
