# PDF Export Customization Guide

## Overview
The Exam Seating App now generates professional PDF reports with college branding, proper page numbering, and clean formatting. This guide explains how to customize the PDF output.

## Features

### ✅ What's Included
- **College Header**: Logo and college name on every page
- **Page Numbers**: Automatic page numbering at the bottom
- **Professional Layout**: Clean, print-ready formatting
- **No UI Elements**: Export button and other UI elements are hidden in PDF
- **Page Breaks**: Smart page breaks to avoid splitting tables
- **Consistent Branding**: Header appears on all pages

## Customization Options

### 1. College Name
To change the college name displayed in the PDF:

1. Open `UI/src/components/RoomSchedule.vue`
2. Find this line (around line 185):
   ```javascript
   const collegeName = ref("Shahun Jain College for Women");
   ```
3. Change the text to your college name:
   ```javascript
   const collegeName = ref("Your College Name Here");
   ```

### 2. College Logo

#### Option A: Replace the Default Logo
1. Create your logo file (recommended formats: PNG, JPG, SVG)
2. Name it `logo.png` (or `logo.jpg`, `logo.svg`)
3. Place it in the `UI/public/` folder
4. If using a different format, update the component:
   ```html
   <img src="/logo.jpg" alt="College Logo" class="college-logo" />
   ```

#### Option B: Use a Different Filename
1. Place your logo in `UI/public/` with any name (e.g., `college-logo.png`)
2. Update the image source in the component:
   ```html
   <img src="/college-logo.png" alt="College Logo" class="college-logo" />
   ```

#### Logo Requirements
- **Size**: 225x225 pixels (will be automatically resized to 80x80 for display)
- **Format**: PNG (current), SVG, JPG, or GIF
- **Background**: Transparent or white background works best
- **Quality**: High resolution for crisp printing

### 3. Header Layout
The header includes:
- College logo (left side)
- College name and exam title (center)
- Date (below title)

To modify the header layout, edit the `.college-header` section in the template.

### 4. Page Formatting

#### Margins
Current margins (in inches):
- Top: 0.5"
- Left: 0.5" 
- Bottom: 1" (includes space for page numbers)
- Right: 0.5"

To change margins, modify the `exportToPDF` function:
```javascript
margin: [0.5, 0.5, 1, 0.5], // [top, left, bottom, right]
```

#### Page Size
Current setting: A4 portrait

To change to letter size:
```javascript
jsPDF: { 
  unit: "in", 
  format: "letter", // or "a4"
  orientation: "portrait" // or "landscape"
}
```

#### Page Numbers
Page numbers appear at the bottom center of each page. To modify:

1. **Position**: Change `@bottom-center` to `@bottom-left` or `@bottom-right`
2. **Format**: Modify the content in the CSS:
   ```css
   @bottom-center {
     content: "Page " counter(page) " of " counter(pages);
   }
   ```

## Advanced Customization

### 1. Colors
Main colors used for PDF export:
- College Name: `#ab3d31` (College burgundy/maroon)
- Exam Title: `#000063` (Navy blue)
- Date: `#424242` (Dark gray)
- Header Border: `#000` (Black)
- Table Borders: `#000` (Black)
- Table Background: `transparent` (No fill)
- Text: `#000` (Black)

To change colors, update the CSS variables in the `<style>` section.

### 2. Fonts
Current font: Arial (web-safe font for consistent PDF rendering)

To change fonts:
```css
.pdf-content {
  font-family: 'Times New Roman', serif; /* or your preferred font */
}
```

### 3. Table Styling
Tables include:
- Simple black borders
- No background fills (transparent)
- Bold headers and totals row
- Clean, minimal design

Modify table styles in the `.schedule-table` CSS section.

### 4. Room Section Layout
Each room appears as a separate section with:
- Room header with number
- Table with class details
- Page break avoidance

## Troubleshooting

### Logo Not Appearing
1. **Check file path**: Ensure logo is in `UI/public/` folder
2. **Check filename**: Verify the filename matches the src attribute
3. **Check file format**: Use common web formats (PNG, JPG, SVG)
4. **Check file size**: Very large files may not load properly

### PDF Layout Issues
1. **Long tables**: Tables automatically break across pages
2. **Header overlap**: Adjust top margin if header overlaps content
3. **Page numbers missing**: Check CSS `@page` rules

### Quality Issues
1. **Blurry text**: Increase the `scale` value in html2canvas options
2. **Poor logo quality**: Use PNG format or high-resolution images
3. **Color issues**: Ensure colors are web-safe

## Sample Customizations

### Example 1: University Setup
```javascript
const collegeName = ref("State University");
// Logo: university-seal.svg in public folder
```

### Example 2: Technical Institute
```javascript
const collegeName = ref("Institute of Technology");
// Logo: tech-logo.png in public folder
```

### Example 3: Women's College
```javascript
const collegeName = ref("Shahun Jain College for Women");
// Logo: college-logo.svg in public folder (current setup)
```

## File Structure
```
UI/
├── public/
│   ├── logo.png          # Your college logo
│   └── favicon.ico
├── src/
│   └── components/
│       └── RoomSchedule.vue  # Main component to modify
```

## Testing Your Changes

1. **Start the application**:
   ```bash
   cd UI && npm run dev
   ```

2. **Generate a test schedule**:
   - Add some test classes and rooms
   - Generate a schedule
   - Click "Export to PDF"

3. **Check the PDF**:
   - Verify college name appears correctly
   - Check logo displays properly
   - Confirm page numbers are present
   - Ensure no UI elements appear in PDF

## Support

If you encounter issues:
1. Check browser console for error messages
2. Verify all file paths are correct
3. Test with different browsers
4. Ensure logo file is accessible via direct URL

For technical support, refer to the main application documentation or create an issue in the project repository.
