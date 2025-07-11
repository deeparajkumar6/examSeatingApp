# Shahun Jain College for Women - Theme Colors

## Color Palette

### Primary Colors (from Vuetify theme)
- **Primary**: `#ab3d31` - College Burgundy/Maroon
- **Secondary**: `#000063` - Navy Blue
- **Background**: `#FFFFFF` - White
- **Surface**: `#FFFFFF` - White

### Accent Colors
- **Light Background**: `#f3e5e4` - Light Burgundy Tint
- **Surface Light**: `#EEEEEE` - Light Gray
- **Surface Variant**: `#424242` - Dark Gray

### Status Colors
- **Error**: `#B00020` - Red
- **Info**: `#2196F3` - Blue
- **Success**: `#4CAF50` - Green
- **Warning**: `#FB8C00` - Orange

## Usage in PDF Export

### Header Section
- **College Name**: `#ab3d31` (Primary Burgundy)
- **Exam Title**: `#000063` (Navy Blue)
- **Date**: `#424242` (Dark Gray)
- **Header Border**: `#000` (Black)

### Table Styling
- **Table Headers**: No background, Black borders, Bold text
- **Table Borders**: `#000` (Black)
- **Total Row**: No background, Black borders, Bold text

### Room Sections
- **Room Headers**: Background `transparent`, Border `#000`, Text `#000`
- **Room Numbers**: `#000` (Black)

### Logo Design
- **Background Circle**: `#ab3d31` (Primary Burgundy)
- **Border**: `#8b2f25` (Darker Burgundy)
- **Text/Elements**: `white` and `#f3e5e4`
- **Accent Elements**: `#000063` (Navy Blue)

## Color Accessibility

### Contrast Ratios
- **Primary on White**: `#ab3d31` on `#FFFFFF` - High contrast ✅
- **Navy on White**: `#000063` on `#FFFFFF` - High contrast ✅
- **Primary on Light**: `#ab3d31` on `#f3e5e4` - Good contrast ✅

### Print Compatibility
- All colors are print-friendly
- High contrast ensures readability in grayscale
- Professional appearance for official documents

## Customization

To modify colors, update the following files:

### 1. Vuetify Theme (`UI/src/plugins/vuetify.js`)
```javascript
colors: {
  primary: '#ab3d31',      // Main college color
  secondary: '#000063',    // Accent color
  // ... other colors
}
```

### 2. PDF Component (`UI/src/components/RoomSchedule.vue`)
```css
.college-name { color: #ab3d31; }
.exam-title { color: #000063; }
.header-divider { border-top: 2px solid #000; }
```

### 3. Logo (`UI/public/logo.png`)
- Update the PNG file with your college logo
- Maintain high resolution for crisp printing
- Use transparent or white background for best results

## Brand Guidelines

### Do's
✅ Use primary burgundy (`#ab3d31`) for main headings and borders  
✅ Use navy blue (`#000063`) for secondary text and accents  
✅ Maintain high contrast for readability  
✅ Use light burgundy (`#f3e5e4`) for subtle backgrounds  

### Don'ts
❌ Don't use colors that clash with the burgundy theme  
❌ Don't reduce contrast below accessibility standards  
❌ Don't mix with other institutional color schemes  
❌ Don't use bright or neon colors that detract from professionalism  

## College Identity

The color scheme reflects:
- **Burgundy/Maroon**: Tradition, excellence, and academic achievement
- **Navy Blue**: Trust, stability, and professionalism  
- **White**: Clarity, purity, and new beginnings
- **Light Tints**: Sophistication and elegance

This palette creates a cohesive visual identity suitable for:
- Official documents and certificates
- Examination schedules and reports
- Academic correspondence
- Digital and print materials
