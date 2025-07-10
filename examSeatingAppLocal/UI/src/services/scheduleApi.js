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
    
    // We need to fetch additional data to create a complete response
    const [classesResponse, roomsResponse] = await Promise.all([
      api.get('/class'),
      api.get('/examRoom')
    ])
    
    // Transform backend response to match frontend expectations
    const transformedResponse = {
      date: response.data.date,
      title: scheduleData.title, // Keep the title from frontend
      session: scheduleData.session, // Keep the session from frontend
      room_assignments: await transformSeatingArrangement(
        response.data.seating_arrangement,
        classesResponse.data.classes,
        roomsResponse.data.examRooms,
        scheduleData.classes
      )
    }
    
    return transformedResponse
  }
}

// Helper function to transform backend seating arrangement to frontend format
async function transformSeatingArrangement(seatingArrangement, allClasses, allRooms, selectedClassIds) {
  const roomAssignments = []
  
  // Create a map of students by roll number for quick lookup
  const studentMap = new Map()
  
  // Get all students from selected classes
  selectedClassIds.forEach(classId => {
    const classData = allClasses.find(c => c.id === classId)
    if (classData && classData.students) {
      classData.students.forEach(student => {
        studentMap.set(student.rollNumber, {
          rollNumber: student.rollNumber,
          studentName: student.studentName,
          className: classData.className
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
