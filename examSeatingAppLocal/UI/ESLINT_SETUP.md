# ESLint Setup Guide

## Overview
This guide explains how to fix ESLint indentation errors in your Vue.js project.

## What Was Fixed

### 1. ESLint Configuration
- **Updated `eslint.config.js`** with proper Vue.js indentation rules
- **Removed conflicting rules** that caused circular fixes
- **Added proper ignores** for auto-generated files

### 2. VS Code Settings
- **Created `.vscode/settings.json`** for consistent editor behavior
- **Configured ESLint integration** with proper formatting
- **Set tab size to 2 spaces** for all relevant file types

### 3. File Ignores
- **Created `.eslintignore`** to exclude auto-generated files
- **Added TypeScript declaration files** to ignores
- **Excluded build and node_modules directories**

## Key ESLint Rules

### Indentation Rules
```javascript
// For regular JavaScript/TypeScript
'indent': ['error', 2, {
  'SwitchCase': 1,
  'VariableDeclarator': 1,
  // ... other options
}]

// For Vue script sections
'vue/script-indent': ['error', 2, {
  'baseIndent': 0,
  'switchCase': 1,
  'ignores': []
}]

// For Vue templates
'vue/html-indent': ['error', 2, {
  'attribute': 1,
  'baseIndent': 1,
  'closeBracket': 0,
  'alignAttributesVertically': true
}]
```

### Disabled Conflicting Rules
```javascript
// These rules were causing conflicts
'comma-dangle': 'off',
'@stylistic/comma-dangle': 'off',
'semi': 'off'
```

## How to Use

### 1. Automatic Fixing
```bash
# Fix all ESLint issues automatically
npm run lint

# Check for issues without fixing
npx eslint . --no-fix
```

### 2. VS Code Integration
- **Install ESLint extension** in VS Code
- **Enable format on save** (already configured in settings)
- **Use Ctrl+Shift+P → "ESLint: Fix all auto-fixable Problems"**

### 3. Manual Indentation Fix
```bash
# Run the custom indentation fixer
node fix-indentation.js
```

## File Structure
```
UI/
├── .vscode/
│   └── settings.json          # VS Code ESLint settings
├── .eslintignore             # Files to ignore
├── eslint.config.js          # Main ESLint configuration
├── fix-indentation.js        # Custom indentation fixer
└── src/
    └── components/           # Your Vue components
```

## Common Issues & Solutions

### 1. "Expected indentation of 2 spaces but found 0"
**Solution**: This is now fixed with proper `vue/script-indent` rule

### 2. "Circular fixes detected"
**Solution**: Removed conflicting rules (`comma-dangle`, `semi`, etc.)

### 3. VS Code not applying ESLint fixes
**Solution**: 
- Restart VS Code
- Check that ESLint extension is installed
- Verify `.vscode/settings.json` is present

### 4. TypeScript declaration file errors
**Solution**: Added `*.d.ts` files to ignores

## Best Practices

### 1. Consistent Indentation
- **Use 2 spaces** for indentation (not tabs)
- **Be consistent** across all files
- **Let ESLint auto-fix** most issues

### 2. Vue.js Specific
- **Use `vue/script-indent`** for `<script>` sections
- **Use `vue/html-indent`** for `<template>` sections
- **Disable regular `indent`** rule for `.vue` files

### 3. Development Workflow
```bash
# Before committing
npm run lint

# If there are issues
npm run lint  # This auto-fixes most issues

# For manual review
npx eslint . --no-fix
```

## Configuration Files

### eslint.config.js
Main ESLint configuration using the new flat config format.

### .vscode/settings.json
VS Code specific settings for ESLint integration and formatting.

### .eslintignore
Files and directories to exclude from ESLint checking.

## Troubleshooting

### ESLint Not Working in VS Code
1. **Check ESLint extension** is installed and enabled
2. **Restart VS Code** after configuration changes
3. **Check output panel** (View → Output → ESLint) for errors
4. **Verify file paths** in configuration

### Still Getting Indentation Errors
1. **Run the custom fixer**: `node fix-indentation.js`
2. **Check for mixed tabs/spaces**: Use "Convert Indentation to Spaces"
3. **Manually fix problematic lines** and run `npm run lint`

### Performance Issues
1. **Add more ignores** to `.eslintignore` if needed
2. **Exclude large directories** like `node_modules`
3. **Use ESLint cache**: `npx eslint . --cache`

## Support

If you continue to have issues:
1. **Check the ESLint output** for specific error messages
2. **Verify your VS Code settings** match the provided configuration
3. **Run `npm run lint`** to see all current issues
4. **Use the custom indentation fixer** for Vue-specific problems

The configuration is now optimized for Vue.js development with Vuetify and should handle most common indentation scenarios automatically.
