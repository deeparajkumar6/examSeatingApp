import api from './api'

export const scheduleApi = {
  // Create exam schedule
  async create(scheduleData) {
    // Transform frontend data to match backend API expectations
    const backendData = {
      date: scheduleData.date,
      classes: scheduleData.classes,
      exam_rooms: scheduleData.exam_rooms,
      split: scheduleData.split
    }
    
    const response = await api.post('/schedule', backendData)
    
    // Check if the response already includes student objects with class info (new format)
    const seatingArrangement = response.data.seating_arrangement
    const isNewFormat = Object.values(seatingArrangement)[0]?.[0]?.rollNumber !== undefined
    
    if (isNewFormat) {
      // New format: students are already objects with class information including shift
      const roomAssignments = await transformNewFormatResponse(
        response.data,
        scheduleData
      )
      
      return {
        date: response.data.date,
        title: scheduleData.title,
        session: scheduleData.session,
        room_assignments: roomAssignments,
        class_summary: response.data.class_summary,
        class_info: response.data.class_info
      }
    } else {
      // Legacy format: need to fetch additional data and transform
      const [classesResponse, roomsResponse] = await Promise.all([
        api.get('/class'),
        api.get('/examRoom')
      ])
      
      const roomAssignments = await transformLegacyResponse(
        response.data.seating_arrangement,
        classesResponse.data.classes,
        roomsResponse.data.examRooms,
        scheduleData.classes
      )
      
      return {
        date: response.data.date,
        title: scheduleData.title,
        session: scheduleData.session,
        room_assignments: roomAssignments
      }
    }
  }
}

// Transform new format response (with shift information)
async function transformNewFormatResponse(responseData, scheduleData) {
  const roomAssignments = []
  const seatingArrangement = responseData.seating_arrangement
  
  // Fetch room details for additional information
  const roomsResponse = await api.get('/examRoom')
  const allRooms = roomsResponse.data.examRooms
  
  // Transform each room's assignment
  for (const [roomNumber, students] of Object.entries(seatingArrangement)) {
    // Find the room details
    const roomData = allRooms.find(room => room.roomNumber === roomNumber)
    
    // Students are already in the correct format with className including shift
    const transformedStudents = students.map(student => ({
      rollNumber: student.rollNumber,
      studentName: student.studentName || 'Unknown Student',
      className: student.className, // This now includes shift (e.g., "Computer Science - Morning")
      classId: student.classId
    }))
    
    roomAssignments.push({
      room_id: roomData?.id || roomAssignments.length + 1,
      room_number: roomNumber,
      room_building: roomData?.roomBuilding || 'Unknown Building',
      room_floor: roomData?.roomFloor || 'Unknown Floor',
      room_capacity: roomData?.roomCapacity || 50,
      students: transformedStudents
    })
  }
  
  return roomAssignments
}

// Legacy transformation for backward compatibility
async function transformLegacyResponse(seatingArrangement, allClasses, allRooms, selectedClassIds) {
  const roomAssignments = []
  
  // Create a map of students by roll number for quick lookup
  const studentMap = new Map()
  
  // Get all students from selected classes
  selectedClassIds.forEach(classId => {
    const classData = allClasses.find(c => c.id === classId)
    if (classData && classData.students) {
      // Create display name with shift for legacy data
      const displayName = classData.shift ? 
        `${classData.className} - ${classData.shift}` : 
        classData.className
      
      classData.students.forEach(student => {
        studentMap.set(student.rollNumber, {
          rollNumber: student.rollNumber,
          studentName: student.studentName,
          className: displayName // Include shift in class name
        })
      })
    }
  })
  
  // Transform each room's assignment
  for (const [roomNumber, studentRolls] of Object.entries(seatingArrangement)) {
    // Find the room details
    const roomData = allRooms.find(room => room.roomNumber === roomNumber)
    
    // Transform student roll numbers to full student objects
    const transformedStudents = studentRolls.map(rollNumber => {
      const student = studentMap.get(rollNumber)
      return student || {
        rollNumber: rollNumber,
        studentName: 'Unknown Student',
        className: 'Unknown Class'
      }
    })
    
    roomAssignments.push({
      room_id: roomData?.id || roomAssignments.length + 1,
      room_number: roomNumber,
      room_building: roomData?.roomBuilding || 'Unknown Building',
      room_floor: roomData?.roomFloor || 'Unknown Floor',
      room_capacity: roomData?.roomCapacity || 50,
      students: transformedStudents
    })
  }
  
  return roomAssignments
}
