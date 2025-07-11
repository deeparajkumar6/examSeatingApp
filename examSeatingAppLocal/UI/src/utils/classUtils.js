/**
 * Utility functions for class-related operations
 * Note: Language is stored at student level, not class level
 */

/**
 * Gets all unique languages from students in a class
 * @param {Object} cls - The class object with students array
 * @returns {Array} Array of unique languages in the class
 */
export function getClassLanguages(cls) {
  if (!cls || !cls.students || !Array.isArray(cls.students)) {
    return []
  }
  
  const languages = cls.students
    .map(student => student.language)
    .filter(lang => lang && lang.trim())
    .map(lang => lang.trim())
  
  return [...new Set(languages)].sort()
}

/**
 * Gets language distribution for a class
 * @param {Object} cls - The class object with students array
 * @returns {Object} Object with language counts
 */
export function getClassLanguageDistribution(cls) {
  if (!cls || !cls.students || !Array.isArray(cls.students)) {
    return {}
  }
  
  const distribution = {}
  cls.students.forEach(student => {
    if (student.language && student.language.trim()) {
      const lang = student.language.trim()
      distribution[lang] = (distribution[lang] || 0) + 1
    }
  })
  
  return distribution
}

/**
 * Generates a display name for a class including shift information
 * Since students can have different languages, we don't include language at class level
 * @param {Object} cls - The class object
 * @param {string} cls.className - The base class name
 * @param {number|string|null} cls.shift - The shift number (I, II, 1, 2, etc.)
 * @returns {string} The formatted display name
 */
export function getClassDisplayName(cls) {
  if (!cls || !cls.className) return ''
  
  let displayName = cls.className
  
  // Add shift information if available
  if (cls.shift) {
    // Handle both numeric (1, 2) and Roman numeral (I, II) formats
    const shiftText = typeof cls.shift === 'number' 
      ? (cls.shift === 1 ? 'I' : cls.shift === 2 ? 'II' : cls.shift.toString())
      : cls.shift.toString()
    displayName += ` - Shift ${shiftText}`
  }
  
  return displayName
}

/**
 * Generates a display name with language summary for informational purposes
 * @param {Object} cls - The class object
 * @returns {string} The formatted display name with language info
 */
export function getClassDisplayNameWithLanguageInfo(cls) {
  const baseName = getClassDisplayName(cls)
  const languages = getClassLanguages(cls)
  
  if (languages.length === 0) {
    return baseName
  } else if (languages.length === 1) {
    return `${baseName} (${languages[0]})`
  } else {
    return `${baseName} (${languages.join(', ')})`
  }
}

/**
 * Generates a short display name for chips and compact views
 * @param {Object} cls - The class object
 * @returns {string} The formatted short display name
 */
export function getClassShortDisplayName(cls) {
  if (!cls || !cls.className) return ''
  
  let displayName = cls.className
  
  // Add shift as a shorter format
  if (cls.shift) {
    const shiftText = typeof cls.shift === 'number' 
      ? (cls.shift === 1 ? 'I' : cls.shift === 2 ? 'II' : cls.shift.toString())
      : cls.shift.toString()
    displayName += ` (${shiftText})`
  }
  
  return displayName
}

/**
 * Expands classes into language-based entries for selection
 * Each class with multiple languages becomes multiple selectable entries
 * @param {Array} classes - Array of class objects
 * @returns {Array} Array of language-based class entries
 */
export function expandClassesByLanguage(classes) {
  if (!Array.isArray(classes)) return []
  
  const expandedClasses = []
  
  classes.forEach(cls => {
    const languages = getClassLanguages(cls)
    
    if (languages.length === 0) {
      // Class with no language info - add as single entry
      const expandedEntry = {
        ...cls,
        originalId: cls.id,
        id: `${cls.id}_no_lang`,
        displayName: getClassDisplayName(cls),
        language: null,
        languageLabel: 'No Language Specified',
        students: cls.students?.filter(s => !s.language || !s.language.trim()) || []
      }
      expandedClasses.push(expandedEntry)
    } else if (languages.length === 1) {
      // Single language class - add as single entry with language
      const language = languages[0]
      const languageStudents = getStudentsByLanguage(cls, language)
      const expandedEntry = {
        ...cls,
        originalId: cls.id,
        id: `${cls.id}_${language.toLowerCase().replace(/\s+/g, '_')}`,
        displayName: `${getClassDisplayName(cls)} - ${language}`,
        language: language,
        languageLabel: language,
        students: languageStudents
      }
      expandedClasses.push(expandedEntry)
    } else {
      // Multiple languages - create separate entries for each language
      languages.forEach(language => {
        const languageStudents = getStudentsByLanguage(cls, language)
        if (languageStudents.length > 0) {
          const expandedEntry = {
            ...cls,
            originalId: cls.id,
            id: `${cls.id}_${language.toLowerCase().replace(/\s+/g, '_')}`,
            displayName: `${getClassDisplayName(cls)} - ${language}`,
            language: language,
            languageLabel: language,
            students: languageStudents
          }
          expandedClasses.push(expandedEntry)
        }
      })
      
      // Also add entry for students without language info if any
      const noLanguageStudents = cls.students?.filter(s => !s.language || !s.language.trim()) || []
      if (noLanguageStudents.length > 0) {
        const expandedEntry = {
          ...cls,
          originalId: cls.id,
          id: `${cls.id}_no_lang`,
          displayName: `${getClassDisplayName(cls)} - No Language Specified`,
          language: null,
          languageLabel: 'No Language Specified',
          students: noLanguageStudents
        }
        expandedClasses.push(expandedEntry)
      }
    }
  })
  
  const sortedClasses = expandedClasses.sort((a, b) => {
    // Sort by class name, then shift, then language
    const nameComparison = a.className.localeCompare(b.className)
    if (nameComparison !== 0) return nameComparison
    
    const shiftA = a.shift || ''
    const shiftB = b.shift || ''
    const shiftComparison = shiftA.localeCompare(shiftB)
    if (shiftComparison !== 0) return shiftComparison
    
    const langA = a.language || 'zzz' // Put no language at end
    const langB = b.language || 'zzz'
    return langA.localeCompare(langB)
  })
  
  return sortedClasses
}

/**
 * Converts expanded class selections back to original format for API
 * @param {Array} expandedSelections - Array of expanded class IDs
 * @param {Array} expandedClasses - Array of expanded class objects
 * @returns {Object} Object with class selections grouped by original class ID
 */
export function convertExpandedSelectionsToOriginal(expandedSelections, expandedClasses) {
  const result = {
    classSelections: [], // For backward compatibility
    languageSelections: {} // New format: { originalClassId: [languages] }
  }
  
  const groupedByOriginal = {}
  
  expandedSelections.forEach(expandedId => {
    const expandedClass = expandedClasses.find(c => c.id === expandedId)
    if (expandedClass) {
      const originalId = expandedClass.originalId
      
      if (!groupedByOriginal[originalId]) {
        groupedByOriginal[originalId] = {
          classId: originalId,
          languages: [],
          students: []
        }
      }
      
      if (expandedClass.language) {
        groupedByOriginal[originalId].languages.push(expandedClass.language)
      } else {
        groupedByOriginal[originalId].languages.push(null) // No language specified
      }
      
      groupedByOriginal[originalId].students.push(...expandedClass.students)
    }
  })
  
  // Convert to arrays and clean up language selections
  Object.values(groupedByOriginal).forEach(group => {
    result.classSelections.push(group.classId)
    
    // Filter out null values and only include classes with valid languages
    const validLanguages = group.languages.filter(lang => lang !== null && lang !== undefined)
    
    // Only add to language_selections if there are valid languages
    if (validLanguages.length > 0) {
      result.languageSelections[group.classId] = validLanguages
    }
    // If no valid languages, don't include this class in language_selections at all
  })
  
  return result
}

/**
 * Gets display information for expanded class selection
 * @param {Array} expandedSelections - Array of expanded class IDs
 * @param {Array} expandedClasses - Array of expanded class objects
 * @returns {Object} Summary information
 */
export function getExpandedSelectionSummary(expandedSelections, expandedClasses) {
  let totalStudents = 0
  let totalLanguages = new Set()
  let classCount = new Set()
  
  const selectionDetails = []
  
  expandedSelections.forEach(expandedId => {
    const expandedClass = expandedClasses.find(c => c.id === expandedId)
    if (expandedClass) {
      totalStudents += expandedClass.students.length
      classCount.add(expandedClass.originalId)
      
      if (expandedClass.language) {
        totalLanguages.add(expandedClass.language)
      }
      
      selectionDetails.push({
        className: expandedClass.className,
        shift: expandedClass.shift,
        language: expandedClass.language,
        studentCount: expandedClass.students.length,
        displayName: expandedClass.displayName
      })
    }
  })
  
  return {
    totalStudents,
    totalLanguages: totalLanguages.size,
    totalClasses: classCount.size,
    totalSelections: expandedSelections.length,
    languages: Array.from(totalLanguages).sort(),
    details: selectionDetails
  }
}

/**
 * Sorts classes by name, then shift
 * @param {Array} classes - Array of class objects
 * @returns {Array} Sorted classes array
 */
export function sortClasses(classes) {
  if (!Array.isArray(classes)) return []
  
  return [...classes].sort((a, b) => {
    // First sort by class name
    const nameComparison = a.className.localeCompare(b.className)
    if (nameComparison !== 0) return nameComparison
    
    // Then by shift
    const shiftA = a.shift || 0
    const shiftB = b.shift || 0
    return shiftA - shiftB
  })
}

/**
 * Filters classes that have students with a specific language
 * @param {Array} classes - Array of class objects
 * @param {string} language - Language to filter by
 * @returns {Array} Filtered classes array
 */
export function filterClassesByLanguage(classes, language) {
  if (!Array.isArray(classes)) return []
  if (!language) return classes
  
  return classes.filter(cls => {
    if (!cls.students || !Array.isArray(cls.students)) return false
    
    return cls.students.some(student => 
      student.language && 
      student.language.toLowerCase() === language.toLowerCase()
    )
  })
}

/**
 * Gets unique languages from all classes (based on students' languages)
 * @param {Array} classes - Array of class objects
 * @returns {Array} Array of unique languages
 */
export function getUniqueLanguages(classes) {
  if (!Array.isArray(classes)) return []
  
  const allLanguages = new Set()
  
  classes.forEach(cls => {
    if (cls.students && Array.isArray(cls.students)) {
      cls.students.forEach(student => {
        if (student.language && student.language.trim()) {
          allLanguages.add(student.language.trim())
        }
      })
    }
  })
  
  return Array.from(allLanguages).sort()
}

/**
 * Gets classes that have students with a specific language
 * @param {Array} classes - Array of class objects
 * @param {string} language - Language to search for
 * @returns {Array} Classes that have students with the specified language
 */
export function getClassesWithLanguage(classes, language) {
  if (!Array.isArray(classes) || !language) return []
  
  return classes.filter(cls => {
    if (!cls.students || !Array.isArray(cls.students)) return false
    
    return cls.students.some(student => 
      student.language && 
      student.language.toLowerCase() === language.toLowerCase()
    )
  })
}

/**
 * Gets detailed language information for a class
 * @param {Object} cls - The class object
 * @returns {Object} Detailed language information
 */
export function getClassLanguageInfo(cls) {
  if (!cls || !cls.students || !Array.isArray(cls.students)) {
    return {
      languages: [],
      distribution: {},
      totalStudents: 0,
      studentsWithLanguage: 0,
      languageCount: 0
    }
  }
  
  const distribution = getClassLanguageDistribution(cls)
  const languages = Object.keys(distribution)
  const totalStudents = cls.students.length
  const studentsWithLanguage = Object.values(distribution).reduce((sum, count) => sum + count, 0)
  
  return {
    languages,
    distribution,
    totalStudents,
    studentsWithLanguage,
    languageCount: languages.length
  }
}

/**
 * Formats language information for display
 * @param {Object} cls - The class object
 * @returns {string} Formatted language information
 */
export function formatClassLanguageInfo(cls) {
  const info = getClassLanguageInfo(cls)
  
  if (info.languageCount === 0) {
    return 'No language specified'
  } else if (info.languageCount === 1) {
    return `${info.languages[0]} (${info.studentsWithLanguage} students)`
  } else {
    const langSummary = info.languages.map(lang => 
      `${lang} (${info.distribution[lang]})`
    ).join(', ')
    return `Mixed: ${langSummary}`
  }
}

/**
 * Gets students by language from a class
 * @param {Object} cls - The class object
 * @param {string} language - Language to filter by
 * @returns {Array} Students with the specified language
 */
export function getStudentsByLanguage(cls, language) {
  if (!cls || !cls.students || !Array.isArray(cls.students) || !language) {
    return []
  }
  
  return cls.students.filter(student => 
    student.language && 
    student.language.toLowerCase() === language.toLowerCase()
  )
}
