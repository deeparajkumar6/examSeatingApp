#!/usr/bin/env python3
"""
Script to update the schedule service with language support
"""

def update_schedule_service():
    services_file = "fastapi_app/app/services.py"
    
    # Read the current file
    with open(services_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the student fetching section
    old_student_fetch = '''            for class_id in data.classes:
                if class_id in class_info:
                    cursor.execute("SELECT rollNumber, studentName, language FROM students WHERE classId = ? ORDER BY rollNumber", (class_id,))
                    student_results = cursor.fetchall()
                    class_students = [row[0] for row in student_results]
                    students_by_class[class_id] = class_students
                    # Include class display name with shift in student data
                    all_students.extend([(student, class_id, class_info[class_id]['display_name']) for student in class_students])'''
    
    new_student_fetch = '''            for class_id in data.classes:
                if class_id in class_info:
                    # Check if language selections are specified for this class
                    selected_languages = None
                    if hasattr(data, 'language_selections') and data.language_selections and class_id in data.language_selections:
                        selected_languages = data.language_selections[class_id]
                    
                    cursor.execute("SELECT rollNumber, studentName, language FROM students WHERE classId = ? ORDER BY rollNumber", (class_id,))
                    student_results = cursor.fetchall()
                    
                    class_students = []
                    for row in student_results:
                        roll_number = row[0]
                        student_name = row[1] if len(row) > 1 else None
                        language = row[2] if len(row) > 2 else None
                        
                        # Filter by language if specified
                        if selected_languages:
                            if language and language not in selected_languages:
                                continue  # Skip students with non-matching languages
                            if not language and None not in selected_languages:
                                continue  # Skip students without language if not explicitly included
                        
                        student_data = {
                            'rollNumber': roll_number,
                            'studentName': student_name,
                            'language': language,
                            'classId': class_id,
                            'className': class_info[class_id]['display_name']
                        }
                        class_students.append(student_data)
                    
                    students_by_class[class_id] = class_students
                    # Add to all_students list with new format
                    all_students.extend(class_students)'''
    
    # Replace the content
    if old_student_fetch in content:
        content = content.replace(old_student_fetch, new_student_fetch)
        print("✅ Updated student fetching logic")
    else:
        print("❌ Could not find student fetching section to replace")
        return False
    
    # Update the sorting logic
    old_sort = "all_students.sort(key=lambda x: x[0])"
    new_sort = "all_students.sort(key=lambda x: x['rollNumber'])"
    
    if old_sort in content:
        content = content.replace(old_sort, new_sort)
        print("✅ Updated sorting logic")
    else:
        print("❌ Could not find sorting logic to replace")
    
    # Update the method call
    old_method_call = "ScheduleService._place_students_in_rooms_with_class_info(all_students, rooms, data.split, max_students_per_class)"
    new_method_call = "ScheduleService._place_students_in_rooms_with_student_info(all_students, rooms, data.split, max_students_per_class)"
    
    if old_method_call in content:
        content = content.replace(old_method_call, new_method_call)
        print("✅ Updated method call")
    
    # Write the updated content back
    with open(services_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Successfully updated services.py with language support")
    return True

if __name__ == "__main__":
    update_schedule_service()
