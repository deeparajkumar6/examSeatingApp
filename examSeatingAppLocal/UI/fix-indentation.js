#!/usr/bin/env node

/**
 * Simple script to fix indentation issues in Vue files
 * Run with: node fix-indentation.js
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

function fixIndentation(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8')
    
    // Split content into lines
    const lines = content.split('\n')
    const fixedLines = []
    
    let inScriptSection = false
    let inTemplateSection = false
    let indentLevel = 0
    
    for (let i = 0; i < lines.length; i++) {
      let line = lines[i]
      const trimmedLine = line.trim()
      
      // Track sections
      if (trimmedLine.startsWith('<script')) {
        inScriptSection = true
        inTemplateSection = false
        indentLevel = 0
      } else if (trimmedLine.startsWith('</script>')) {
        inScriptSection = false
        indentLevel = 0
      } else if (trimmedLine.startsWith('<template')) {
        inTemplateSection = true
        inScriptSection = false
        indentLevel = 0
      } else if (trimmedLine.startsWith('</template>')) {
        inTemplateSection = false
        indentLevel = 0
      }
      
      // Skip empty lines and comments
      if (trimmedLine === '' || trimmedLine.startsWith('//') || trimmedLine.startsWith('/*')) {
        fixedLines.push(line)
        continue
      }
      
      // Fix indentation in script sections
      if (inScriptSection && !trimmedLine.startsWith('<script') && !trimmedLine.startsWith('</script>')) {
        // Calculate proper indentation based on brackets and keywords
        const openBrackets = (trimmedLine.match(/[{[(]/g) || []).length
        const closeBrackets = (trimmedLine.match(/[}\])]/g) || []).length
        
        // Adjust indent level for closing brackets at start of line
        if (trimmedLine.startsWith('}') || trimmedLine.startsWith(']') || trimmedLine.startsWith(')'))) {
          indentLevel = Math.max(0, indentLevel - 1)
        }
        
        // Apply indentation
        const spaces = '  '.repeat(indentLevel)
        line = spaces + trimmedLine
        
        // Adjust indent level for next line
        indentLevel += openBrackets - closeBrackets
        indentLevel = Math.max(0, indentLevel)
      }
      
      fixedLines.push(line)
    }
    
    const fixedContent = fixedLines.join('\n')
    
    // Only write if content changed
    if (fixedContent !== content) {
      fs.writeFileSync(filePath, fixedContent, 'utf8')
      console.log(`Fixed indentation in: ${path.relative(__dirname, filePath)}`)
      return true
    }
    
    return false
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error.message)
    return false
  }
}

function findVueFiles(dir) {
  const files = []
  
  function traverse(currentDir) {
    const items = fs.readdirSync(currentDir)
    
    for (const item of items) {
      const fullPath = path.join(currentDir, item)
      const stat = fs.statSync(fullPath)
      
      if (stat.isDirectory() && !item.startsWith('.') && item !== 'node_modules') {
        traverse(fullPath)
      } else if (stat.isFile() && item.endsWith('.vue')) {
        files.push(fullPath)
      }
    }
  }
  
  traverse(dir)
  return files
}

// Main execution
const srcDir = path.join(__dirname, 'src')
const vueFiles = findVueFiles(srcDir)

console.log(`Found ${vueFiles.length} Vue files`)

let fixedCount = 0
for (const file of vueFiles) {
  if (fixIndentation(file)) {
    fixedCount++
  }
}

console.log(`Fixed indentation in ${fixedCount} files`)

if (fixedCount > 0) {
  console.log('\nRun "npm run lint" to apply ESLint fixes')
}
