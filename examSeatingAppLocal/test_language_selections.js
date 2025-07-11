// Test script to verify language selections functionality
const API_BASE_URL = 'http://localhost:8000';

async function testLanguageSelections() {
  console.log('Testing Language Selections Functionality');
  console.log('=========================================');
  
  // Test data similar to what the UI would send
  const testData = {
    date: '2025-07-11',
    classes: [1, 3],
    exam_rooms: [1],
    split: true,
    language_selections: {
      1: ['HINDI'],
      3: ['HINDI']
    }
  };
  
  console.log('Sending request with data:', JSON.stringify(testData, null, 2));
  
  try {
    const response = await fetch(`${API_BASE_URL}/schedule`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(testData)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    
    console.log('\nAPI Response:');
    console.log('=============');
    console.log(`Date: ${result.date}`);
    
    // Count total students
    const totalStudents = Object.values(result.seating_arrangement)
      .reduce((total, students) => total + students.length, 0);
    console.log(`Total students scheduled: ${totalStudents}`);
    
    // Show students by room
    console.log('\nStudents by room:');
    for (const [roomNumber, students] of Object.entries(result.seating_arrangement)) {
      console.log(`  Room ${roomNumber}: ${students.length} students`);
      students.forEach(student => {
        console.log(`    ${student.rollNumber} - ${student.studentName} - ${student.language} (Class ${student.classId})`);
      });
    }
    
    // Show language summary
    if (result.language_summary) {
      console.log('\nLanguage Summary:');
      for (const [roomNumber, languages] of Object.entries(result.language_summary)) {
        console.log(`  Room ${roomNumber}:`, languages);
      }
    }
    
    // Verify filtering worked correctly
    const allLanguages = Object.values(result.seating_arrangement)
      .flat()
      .map(student => student.language)
      .filter(lang => lang);
    
    const uniqueLanguages = [...new Set(allLanguages)];
    console.log(`\nUnique languages in result: ${uniqueLanguages.join(', ')}`);
    
    if (uniqueLanguages.length === 1 && uniqueLanguages[0] === 'HINDI') {
      console.log('✅ SUCCESS: Language filtering is working correctly!');
      console.log('   Only HINDI students were included in the schedule.');
    } else {
      console.log('❌ ISSUE: Language filtering may not be working as expected.');
      console.log(`   Expected only HINDI students, but got: ${uniqueLanguages.join(', ')}`);
    }
    
  } catch (error) {
    console.error('❌ Error testing language selections:', error.message);
  }
}

// Test without language selections for comparison
async function testWithoutLanguageSelections() {
  console.log('\n\nTesting WITHOUT Language Selections (for comparison)');
  console.log('===================================================');
  
  const testData = {
    date: '2025-07-11',
    classes: [1, 3],
    exam_rooms: [1],
    split: true
    // No language_selections
  };
  
  try {
    const response = await fetch(`${API_BASE_URL}/schedule`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(testData)
    });
    
    const result = await response.json();
    
    const totalStudents = Object.values(result.seating_arrangement)
      .reduce((total, students) => total + students.length, 0);
    console.log(`Total students without filtering: ${totalStudents}`);
    
    const allLanguages = Object.values(result.seating_arrangement)
      .flat()
      .map(student => student.language)
      .filter(lang => lang);
    
    const languageCounts = {};
    allLanguages.forEach(lang => {
      languageCounts[lang] = (languageCounts[lang] || 0) + 1;
    });
    
    console.log('Language distribution without filtering:', languageCounts);
    
  } catch (error) {
    console.error('❌ Error testing without language selections:', error.message);
  }
}

// Run tests
async function runTests() {
  await testLanguageSelections();
  await testWithoutLanguageSelections();
}

// Check if running in Node.js environment
if (typeof window === 'undefined') {
  // Node.js environment
  const fetch = require('node-fetch');
  runTests();
} else {
  // Browser environment
  runTests();
}
