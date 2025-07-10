// Sample data for testing PDF generation
export const sampleScheduleData = {
  title: "Mid-Term Examination - November 2024",
  date: "2024-11-15",
  session: "FN",
  room_assignments: [
    {
      room_id: 1,
      room_number: "2003",
      room_building: "BUILDING II",
      room_floor: "Second Floor",
      room_capacity: 60,
      students: [
        // III B.Sc MATHS S-I students
        { rollNumber: "222210475", studentName: "Arun Kumar", className: "III B.Sc MATHS S-I" },
        { rollNumber: "222210476", studentName: "Priya Sharma", className: "III B.Sc MATHS S-I" },
        { rollNumber: "222210477", studentName: "Rajesh Patel", className: "III B.Sc MATHS S-I" },
        { rollNumber: "222210478", studentName: "Sneha Reddy", className: "III B.Sc MATHS S-I" },
        { rollNumber: "222210479", studentName: "Vikram Singh", className: "III B.Sc MATHS S-I" },
        { rollNumber: "222210480", studentName: "Kavya Nair", className: "III B.Sc MATHS S-I" },
        { rollNumber: "222210481", studentName: "Arjun Menon", className: "III B.Sc MATHS S-I" },
        { rollNumber: "222210482", studentName: "Deepika Joshi", className: "III B.Sc MATHS S-I" },
        { rollNumber: "222210483", studentName: "Rohit Gupta", className: "III B.Sc MATHS S-I" },
        { rollNumber: "222210484", studentName: "Ananya Das", className: "III B.Sc MATHS S-I" },
        { rollNumber: "222210485", studentName: "Karthik Raj", className: "III B.Sc MATHS S-I" },
        { rollNumber: "222210486", studentName: "Meera Iyer", className: "III B.Sc MATHS S-I" },
        { rollNumber: "222210489", studentName: "Suresh Babu", className: "III B.Sc MATHS S-I" },
        
        // I BCOM CS SI students
        { rollNumber: "122402292", studentName: "Amit Verma", className: "I BCOM CS SI" },
        { rollNumber: "122402293", studentName: "Pooja Agarwal", className: "I BCOM CS SI" },
        { rollNumber: "122402294", studentName: "Ravi Kumar", className: "I BCOM CS SI" },
        { rollNumber: "122402295", studentName: "Sita Devi", className: "I BCOM CS SI" },
        { rollNumber: "122402296", studentName: "Manoj Tiwari", className: "I BCOM CS SI" },
        { rollNumber: "122402297", studentName: "Geeta Rani", className: "I BCOM CS SI" },
        { rollNumber: "122402298", studentName: "Sunil Yadav", className: "I BCOM CS SI" },
        { rollNumber: "122402299", studentName: "Rekha Sharma", className: "I BCOM CS SI" },
        { rollNumber: "122402300", studentName: "Dinesh Kumar", className: "I BCOM CS SI" },
        { rollNumber: "122402301", studentName: "Sunita Singh", className: "I BCOM CS SI" },
        { rollNumber: "122402302", studentName: "Ramesh Gupta", className: "I BCOM CS SI" },
        { rollNumber: "122402303", studentName: "Kavita Jain", className: "I BCOM CS SI" },
        { rollNumber: "122402304", studentName: "Ashok Pandey", className: "I BCOM CS SI" },
        { rollNumber: "122402305", studentName: "Nisha Agrawal", className: "I BCOM CS SI" },
        { rollNumber: "122402306", studentName: "Vijay Mishra", className: "I BCOM CS SI" },
        { rollNumber: "122402307", studentName: "Shanti Devi", className: "I BCOM CS SI" },
        { rollNumber: "122402308", studentName: "Prakash Soni", className: "I BCOM CS SI" },
        { rollNumber: "122402309", studentName: "Usha Rani", className: "I BCOM CS SI" },
        { rollNumber: "122402310", studentName: "Mohan Lal", className: "I BCOM CS SI" },
        { rollNumber: "122402311", studentName: "Radha Krishna", className: "I BCOM CS SI" }
      ]
    },
    {
      room_id: 2,
      room_number: "1005",
      room_building: "MAIN BUILDING",
      room_floor: "Ground Floor",
      room_capacity: 50,
      students: [
        // II B.Sc PHYSICS students
        { rollNumber: "212110201", studentName: "Arjun Reddy", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110202", studentName: "Lakshmi Priya", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110203", studentName: "Kiran Kumar", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110204", studentName: "Swathi Nair", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110205", studentName: "Naveen Chandra", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110206", studentName: "Divya Sree", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110207", studentName: "Harish Babu", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110208", studentName: "Madhavi Latha", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110209", studentName: "Srinivas Rao", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110210", studentName: "Padmavathi", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110211", studentName: "Venkat Rao", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110212", studentName: "Sailaja Devi", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110213", studentName: "Ramesh Babu", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110214", studentName: "Jyothi Kumari", className: "II B.Sc PHYSICS" },
        { rollNumber: "212110215", studentName: "Suresh Kumar", className: "II B.Sc PHYSICS" },
        
        // I BBA students
        { rollNumber: "122501001", studentName: "Rahul Sharma", className: "I BBA" },
        { rollNumber: "122501002", studentName: "Priyanka Joshi", className: "I BBA" },
        { rollNumber: "122501003", studentName: "Abhishek Gupta", className: "I BBA" },
        { rollNumber: "122501004", studentName: "Neha Agarwal", className: "I BBA" },
        { rollNumber: "122501005", studentName: "Sanjay Patel", className: "I BBA" },
        { rollNumber: "122501006", studentName: "Ritu Singh", className: "I BBA" },
        { rollNumber: "122501007", studentName: "Akash Verma", className: "I BBA" },
        { rollNumber: "122501008", studentName: "Shreya Malhotra", className: "I BBA" },
        { rollNumber: "122501009", studentName: "Varun Kapoor", className: "I BBA" },
        { rollNumber: "122501010", studentName: "Anjali Rao", className: "I BBA" },
        { rollNumber: "122501011", studentName: "Nikhil Jain", className: "I BBA" },
        { rollNumber: "122501012", studentName: "Pooja Bansal", className: "I BBA" }
      ]
    }
  ]
}

export default sampleScheduleData
