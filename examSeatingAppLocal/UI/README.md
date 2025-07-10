# Exam Seating App - Modular Vue.js UI

## 🎯 Clean Architecture

This is a modern, modular Vue.js application built with Vuetify 3 for managing exam seating arrangements.

### 📁 Project Structure

```
src/
├── components/
│   ├── layout/              # Layout components
│   │   ├── AppNavigation.vue
│   │   ├── AppBar.vue
│   │   ├── NavigationDrawer.vue
│   │   ├── NavigationItem.vue
│   │   └── AppMain.vue
│   └── classes/             # Feature-specific components
│       ├── ClassManagement.vue
│       ├── ClassHeader.vue
│       ├── ClassTable.vue
│       ├── ClassDialog.vue
│       ├── StudentForm.vue
│       ├── StudentChips.vue
│       ├── ClassActions.vue
│       └── CsvUploadDialog.vue
├── stores/                  # Pinia state management
│   ├── app.js              # Global app state
│   ├── navigation.js       # Navigation configuration
│   └── classes.js          # Classes state management
├── services/               # API service layer
│   ├── api.js              # Base API configuration
│   ├── classesApi.js       # Classes API endpoints
│   ├── examRoomsApi.js     # Exam rooms API endpoints
│   └── scheduleApi.js      # Schedule API endpoints
├── pages/                  # Route pages
│   ├── index.vue           # Classes management page
│   ├── exam-rooms.vue      # Exam rooms page
│   └── schedule.vue        # Schedule page
└── App.vue                 # Root application component
```

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## ✨ Features

- **Modern Vue 3**: Composition API with `<script setup>`
- **Vuetify 3**: Material Design components
- **Pinia**: State management
- **Modular Architecture**: Feature-based component organization
- **API Service Layer**: Centralized HTTP client with error handling
- **Responsive Design**: Mobile-friendly interface
- **CSV Import/Export**: Bulk data operations

## 🎯 Key Benefits

- **Maintainable**: Clear separation of concerns
- **Scalable**: Easy to add new features
- **Testable**: Components can be tested independently
- **Reusable**: Modular components for consistency
- **Professional**: Follows Vue.js best practices

## 🔧 Development

### Adding New Features

1. **Components**: Add to `src/components/[feature]/`
2. **State**: Create store in `src/stores/[feature].js`
3. **API**: Add service in `src/services/[feature]Api.js`
4. **Pages**: Add route page in `src/pages/`

### Code Style

- Use Composition API with `<script setup>`
- Follow single responsibility principle
- Use TypeScript-style prop definitions
- Implement proper error handling
