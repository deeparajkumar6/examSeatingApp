import pandas as pd
from typing import List, Dict, Optional, Tuple
from fastapi import HTTPException
import io
from datetime import datetime

class ExcelParser:
    """Utility class for parsing Excel files with student data"""
    
    @staticmethod
    def parse_student_excel(file_content: bytes) -> Dict:
        """
        Parse Excel file with student data from all sheets:
        - Each sheet represents different years/classes
        - Row with academic year info
        - Header row with columns
        - Student data split across two rows (main data + date of birth)
        
        Returns:
        {
            'academic_year': str,
            'classes': [
                {
                    'class_name': str,
                    'shift': str,
                    'students': [
                        {
                            'serial_no': int,
                            'register_number': str,
                            'name': str,
                            'language': str,
                            'date_of_birth': str
                        }
                    ]
                }
            ]
        }
        """
        try:
            # Read all sheet names
            excel_file = pd.ExcelFile(io.BytesIO(file_content))
            sheet_names = excel_file.sheet_names
            
            all_classes = []
            academic_year = None
            
            # Process each sheet
            for sheet_name in sheet_names:
                try:
                    # Read sheet data
                    df_raw = pd.read_excel(io.BytesIO(file_content), sheet_name=sheet_name, header=None)
                    
                    # Extract academic year from first sheet if not already found
                    if academic_year is None:
                        academic_year = ExcelParser._extract_academic_year(df_raw)
                    
                    # Find header row
                    header_row = ExcelParser._find_header_row(df_raw)
                    if header_row is None:
                        continue  # Skip sheets without proper headers
                    
                    # Read data with proper header
                    df = pd.read_excel(io.BytesIO(file_content), sheet_name=sheet_name, header=header_row)
                    
                    # Extract students from this sheet
                    students = ExcelParser._extract_students(df)
                    
                    if students:
                        # Group students by class and shift for this sheet
                        sheet_classes = ExcelParser._group_students_by_class(students)
                        all_classes.extend(sheet_classes)
                        
                except Exception as sheet_error:
                    # Continue processing other sheets if one fails
                    print(f"Warning: Error processing sheet '{sheet_name}': {str(sheet_error)}")
                    continue
            
            if not all_classes:
                raise HTTPException(status_code=400, detail="No student data found in any sheet of the Excel file")
            
            return {
                'academic_year': academic_year,
                'classes': all_classes
            }
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=400, detail=f"Error parsing Excel file: {str(e)}")
    
    @staticmethod
    def _extract_academic_year(df_raw: pd.DataFrame) -> Optional[str]:
        """Extract academic year from the first few rows"""
        for i, row in df_raw.iterrows():
            if i > 10:  # Only check first 10 rows
                break
            row_str = ' '.join([str(x) for x in row if pd.notna(x)])
            if 'YEAR' in row_str and ('20' in row_str):
                return row_str.strip()
        return None
    
    @staticmethod
    def _find_header_row(df_raw: pd.DataFrame) -> Optional[int]:
        """Find the row containing column headers"""
        for i, row in df_raw.iterrows():
            row_values = [str(x).upper() for x in row if pd.notna(x)]
            if any('S.NO' in val or 'REGISTER' in val for val in row_values):
                return i
        return None
    
    @staticmethod
    def _extract_students(df: pd.DataFrame) -> List[Dict]:
        """Extract student data from the DataFrame"""
        students = []
        df_clean = df.dropna(how='all')  # Remove completely empty rows
        
        # Check how many columns we have
        num_columns = len(df_clean.columns)
        
        # Determine column structure based on available columns
        has_language_column = num_columns > 5
        
        i = 0
        while i < len(df_clean):
            try:
                row = df_clean.iloc[i]
                
                # Check if this is a student data row (has serial number)
                if pd.notna(row.iloc[0]) and str(row.iloc[0]).replace('.0', '').isdigit():
                    student = {
                        'serial_no': int(float(row.iloc[0])),
                        'register_number': str(int(float(row.iloc[1]))) if pd.notna(row.iloc[1]) else '',
                        'name': str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else '',
                        'department': str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else '',
                        'shift': str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else '',
                        'date_of_birth': None
                    }
                    
                    # Handle language column - it might not exist
                    if has_language_column:
                        # Language column exists at index 5
                        try:
                            student['language'] = str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else ''
                        except IndexError:
                            student['language'] = ''
                    else:
                        # Language column doesn't exist
                        student['language'] = ''
                    
                    # Check next row for date of birth
                    if i + 1 < len(df_clean):
                        next_row = df_clean.iloc[i + 1]
                        if pd.notna(next_row.iloc[2]) and pd.isna(next_row.iloc[0]):
                            # This is likely the date of birth row
                            dob = next_row.iloc[2]
                            if isinstance(dob, pd.Timestamp):
                                student['date_of_birth'] = dob.strftime('%Y-%m-%d')
                            else:
                                try:
                                    # Try to parse as date string
                                    parsed_date = pd.to_datetime(str(dob))
                                    student['date_of_birth'] = parsed_date.strftime('%Y-%m-%d')
                                except:
                                    student['date_of_birth'] = str(dob)
                            i += 1  # Skip the date row
                    
                    students.append(student)
                    
            except Exception as e:
                # Continue processing other rows if one fails
                pass
            
            i += 1
        
        return students
    
    @staticmethod
    def _group_students_by_class(students: List[Dict]) -> List[Dict]:
        """Group students by class and shift"""
        class_groups = {}
        
        for student in students:
            class_name = student['department']
            shift = student['shift']
            
            # Create a unique key for class + shift combination
            class_key = f"{class_name}_{shift}" if shift else class_name
            
            if class_key not in class_groups:
                class_groups[class_key] = {
                    'class_name': class_name,
                    'shift': shift,
                    'students': []
                }
            
            # Handle language - convert empty string to None for consistency
            language = student.get('language', '')
            if not language or language.strip() == '':
                language = None
            
            # Add student to the class group
            class_groups[class_key]['students'].append({
                'serial_no': student['serial_no'],
                'register_number': student['register_number'],
                'name': student['name'],
                'language': language,
                'date_of_birth': student['date_of_birth']
            })
        
        return list(class_groups.values())

class ExcelValidator:
    """Utility class for validating Excel data"""
    
    @staticmethod
    def validate_parsed_data(parsed_data: Dict) -> List[str]:
        """Validate the parsed Excel data and return list of errors"""
        errors = []
        
        if not parsed_data.get('classes'):
            errors.append("No classes found in the Excel file")
            return errors
        
        for class_idx, class_data in enumerate(parsed_data['classes']):
            class_name = class_data.get('class_name', '')
            if not class_name:
                errors.append(f"Class {class_idx + 1}: Missing class name")
            
            # Validate shift is provided and not empty
            shift = class_data.get('shift', '')
            if not shift or not shift.strip():
                errors.append(f"Class '{class_name}': Shift is required and cannot be empty")
            
            students = class_data.get('students', [])
            if not students:
                errors.append(f"Class '{class_name}': No students found")
                continue
            
            # Validate students
            register_numbers = set()
            for student_idx, student in enumerate(students):
                student_errors = ExcelValidator._validate_student(student, student_idx + 1, class_name)
                errors.extend(student_errors)
                
                # Check for duplicate register numbers within the same class
                reg_num = student.get('register_number')
                if reg_num:
                    if reg_num in register_numbers:
                        errors.append(f"Class '{class_name}': Duplicate register number '{reg_num}'")
                    register_numbers.add(reg_num)
        
        return errors
    
    @staticmethod
    def _validate_student(student: Dict, student_idx: int, class_name: str) -> List[str]:
        """Validate individual student data"""
        errors = []
        
        if not student.get('register_number'):
            errors.append(f"Class '{class_name}', Student {student_idx}: Missing register number")
        
        if not student.get('name'):
            errors.append(f"Class '{class_name}', Student {student_idx}: Missing student name")
        
        # Validate date of birth format if provided
        dob = student.get('date_of_birth')
        if dob:
            try:
                datetime.strptime(dob, '%Y-%m-%d')
            except ValueError:
                errors.append(f"Class '{class_name}', Student {student_idx}: Invalid date of birth format")
        
        return errors
