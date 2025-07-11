// Test to verify UI language selection fix - omit classes without language selections
const path = require('path');

function testConvertExpandedSelectionsToOriginal() {
  console.log('Testing convertExpandedSelectionsToOriginal function...');
  
  // Mock expanded classes data
  const expandedClasses = [
    {
      id: '1_hindi',
      originalId: 1,
      language: 'HINDI',
      students: [{ id: 1, name: 'Student 1' }]
    },
    {
      id: '3_hindi',
      originalId: 3,
      language: 'HINDI',
      students: [{ id: 2, name: 'Student 2' }]
    },
    {
      id: '4_no_lang',
      originalId: 4,
      language: null, // This class should be omitted from language_selections
      students: [{ id: 3, name: 'Student 3' }]
    }
  ];
  
  const expandedSelections = ['1_hindi', '3_hindi', '4_no_lang'];
  
  // Simulate the fixed logic
  const result = {
    classSelections: [],
    languageSelections: {}
  };
  
  const groupedByOriginal = {};
  
  expandedSelections.forEach(expandedId => {
    const expandedClass = expandedClasses.find(c => c.id === expandedId);
    if (expandedClass) {
      const originalId = expandedClass.originalId;
      
      if (!groupedByOriginal[originalId]) {
        groupedByOriginal[originalId] = {
          classId: originalId,
          languages: [],
          students: []
        };
      }
      
      if (expandedClass.language) {
        groupedByOriginal[originalId].languages.push(expandedClass.language);
      }
      // Note: We don't push null anymore
      
      groupedByOriginal[originalId].students.push(...expandedClass.students);
    }
  });
  
  // Convert to arrays and clean up language selections
  Object.values(groupedByOriginal).forEach(group => {
    result.classSelections.push(group.classId);
    
    // Filter out null values and only include classes with valid languages
    const validLanguages = group.languages.filter(lang => lang !== null && lang !== undefined);
    
    // Only add to language_selections if there are valid languages
    if (validLanguages.length > 0) {
      result.languageSelections[group.classId] = validLanguages;
    }
    // If no valid languages, don't include this class in language_selections at all
  });
  
  console.log('Result:', JSON.stringify(result, null, 2));
  
  // Verify the fix
  const hasClass4InLanguageSelections = 4 in result.languageSelections;
  if (!hasClass4InLanguageSelections) {
    console.log('✅ SUCCESS: Class 4 is omitted from language_selections (no language specified)');
  } else {
    console.log('❌ ISSUE: Class 4 is still in language_selections:', result.languageSelections[4]);
  }
  
  // Check that other classes still work correctly
  const class1Languages = result.languageSelections[1];
  const class3Languages = result.languageSelections[3];
  
  if (class1Languages && class1Languages.includes('HINDI') && 
      class3Languages && class3Languages.includes('HINDI')) {
    console.log('✅ SUCCESS: Classes with languages are correctly included');
  } else {
    console.log('❌ ISSUE: Classes with languages are missing or incorrect');
  }
  
  // Verify all classes are still in classSelections
  if (result.classSelections.includes(1) && 
      result.classSelections.includes(3) && 
      result.classSelections.includes(4)) {
    console.log('✅ SUCCESS: All classes are included in classSelections');
  } else {
    console.log('❌ ISSUE: Some classes are missing from classSelections');
  }
  
  return result;
}

// Run the test
const testResult = testConvertExpandedSelectionsToOriginal();

console.log('\nExpected API call format:');
console.log(JSON.stringify({
  date: '2025-07-11',
  classes: testResult.classSelections,
  exam_rooms: [1],
  split: true,
  language_selections: testResult.languageSelections
}, null, 2));

console.log('\nNote: Class 4 is in classes array but NOT in language_selections');
console.log('This means: Class 1 & 3 will be filtered by language, Class 4 will include all students');
