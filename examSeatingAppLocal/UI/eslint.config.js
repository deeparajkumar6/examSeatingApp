import vuetify from 'eslint-config-vuetify'

export default [
  {
    ignores: [
      'node_modules/**',
      'dist/**',
      'build/**',
      '*.d.ts',
      'auto-imports.d.ts',
      'components.d.ts',
      'typed-router.d.ts',
      'fix-indentation.js',
      '.vscode/**'
    ]
  },
  ...vuetify,
  {
    rules: {
      // Override problematic rules
      'comma-dangle': 'off',
      '@stylistic/comma-dangle': 'off',
      'semi': 'off',

      // Vue-specific indentation rules
      'vue/script-indent': ['error', 2, {
        'baseIndent': 0,
        'switchCase': 1,
        'ignores': []
      }],

      'vue/html-indent': ['error', 2, {
        'attribute': 1,
        'baseIndent': 1,
        'closeBracket': 0,
        'alignAttributesVertically': true,
        'ignores': []
      }],

      // Standard indentation
      'indent': ['error', 2, {
        'SwitchCase': 1,
        'VariableDeclarator': 1,
        'outerIIFEBody': 1,
        'MemberExpression': 1,
        'FunctionDeclaration': { 'parameters': 1, 'body': 1 },
        'FunctionExpression': { 'parameters': 1, 'body': 1 },
        'CallExpression': { 'arguments': 1 },
        'ArrayExpression': 1,
        'ObjectExpression': 1,
        'ImportDeclaration': 1,
        'flatTernaryExpressions': false,
        'ignoreComments': false,
        'offsetTernaryExpressions': false
      }],

      // Relaxed rules for development
      'no-console': 'warn',
      'no-debugger': 'warn',
      'vue/require-default-prop': 'off',
      'vue/multi-word-component-names': 'off'
    }
  },
  {
    files: ['*.vue'],
    rules: {
      // Disable indent rule for Vue files, use vue/script-indent instead
      'indent': 'off'
    }
  }
]
