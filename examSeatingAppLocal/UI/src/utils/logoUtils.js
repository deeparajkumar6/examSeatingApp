/**
 * Utility functions for handling logo in PDF generation
 */

/**
 * Load logo image and convert to base64 for PDF embedding
 */
export const loadLogoAsBase64 = () => {
  return new Promise((resolve) => {
    try {
      const img = new Image()
      img.crossOrigin = 'anonymous'
      
      img.onload = () => {
        try {
          const canvas = document.createElement('canvas')
          const ctx = canvas.getContext('2d')
          
          // Set canvas size to match image
          canvas.width = img.width
          canvas.height = img.height
          
          // Draw image on canvas
          ctx.drawImage(img, 0, 0)
          
          // Convert to base64
          const dataURL = canvas.toDataURL('image/png')
          resolve(dataURL)
        } catch (error) {
          console.warn('Could not process logo image:', error)
          resolve(null)
        }
      }
      
      img.onerror = () => {
        console.warn('Could not load logo image')
        resolve(null)
      }
      
      // Try to load logo from public folder
      img.src = '/logo.png'
    } catch (error) {
      console.warn('Logo loading failed:', error)
      resolve(null)
    }
  })
}

/**
 * Add logo to PDF document
 */
export const addLogToPDF = async (doc, x, y, width, height) => {
  try {
    const logoBase64 = await loadLogoAsBase64()
    
    if (logoBase64) {
      doc.addImage(logoBase64, 'PNG', x, y, width, height)
      return true
    } else {
      // Add placeholder if logo couldn't be loaded
      addLogoPlaceholder(doc, x, y, width, height)
      return false
    }
  } catch (error) {
    console.warn('Could not add logo to PDF:', error)
    addLogoPlaceholder(doc, x, y, width, height)
    return false
  }
}

/**
 * Add logo placeholder when actual logo can't be loaded
 */
const addLogoPlaceholder = (doc, x, y, width, height) => {
  // Draw a circle placeholder
  const centerX = x + width / 2
  const centerY = y + height / 2
  const radius = Math.min(width, height) / 2
  
  doc.setFillColor(220, 220, 220)
  doc.setDrawColor(180, 180, 180)
  doc.setLineWidth(1)
  doc.circle(centerX, centerY, radius, 'FD')
  
  // Add "LOGO" text
  doc.setFontSize(8)
  doc.setTextColor(120, 120, 120)
  doc.setFont('helvetica', 'normal')
  doc.text('LOGO', centerX, centerY + 1, { align: 'center' })
}

export default {
  loadLogoAsBase64,
  addLogToPDF
}
