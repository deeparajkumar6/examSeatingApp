import jsPDF from 'jspdf'
import 'jspdf-autotable'
import { loadLogoAsBase64 } from '@/utils/logoUtils'

export class PDFService {
  // Store logo data to reuse across pages
  static logoData = null

  /**
   * Generate Summary PDF with room-wise class distribution (matching the provided format)
   */
  static async generateSummaryPDF(scheduleData) {
    const doc = new jsPDF()
    
    // Load logo once for all pages
    this.logoData = await loadLogoAsBase64()
    
    // Set up document properties
    doc.setProperties({
      title: `${scheduleData.title} - Summary`,
      subject: 'Exam Room Summary',
      author: 'Exam Seating System',
      creator: 'Exam Seating System'
    })

    // Add header with college branding and logo
    await this.addSummaryHeader(doc, scheduleData)
    
    // Process room data for summary
    const summaryData = this.processSummaryData(scheduleData.room_assignments)
    
    // Create the main summary table
    this.createSummaryTable(doc, summaryData, scheduleData)
    
    // Add footer
    this.addFooter(doc, scheduleData)
    
    // Save the PDF
    const fileName = `${scheduleData.title.replace(/\s+/g, '_')}_Summary_${scheduleData.date}.pdf`
    doc.save(fileName)
  }

  /**
   * Generate Detailed PDF with complete student lists - each room on separate pages for individual printing
   */
  static async generateDetailedPDF(scheduleData) {
    const doc = new jsPDF()
    
    // Load logo once for all pages
    this.logoData = await loadLogoAsBase64()
    
    // Set up document properties
    doc.setProperties({
      title: `${scheduleData.title} - Detailed`,
      subject: 'Exam Room Details',
      author: 'Exam Seating System',
      creator: 'Exam Seating System'
    })

    // Process each room separately for individual printing
    scheduleData.room_assignments.forEach((room, index) => {
      // Add new page for each room (except first)
      if (index > 0) {
        doc.addPage()
      }
      
      // Add header with logo for each room's starting page
      this.addDetailedHeaderSync(doc, scheduleData)
      
      // Add room details starting right after header
      this.addRoomDetailedSectionForPrinting(doc, room, 60)
    })
    
    // Add footer only to pages with headers (room starting pages)
    this.addDetailedFooterForPrinting(doc, scheduleData)
    
    // Save the PDF
    const fileName = `${scheduleData.title.replace(/\s+/g, '_')}_Detailed_${scheduleData.date}.pdf`
    doc.save(fileName)
  }

  /**
   * Add logo to PDF using cached logo data
   */
  static addLogoToPDF(doc, x, y, width, height) {
    if (this.logoData) {
      try {
        doc.addImage(this.logoData, 'PNG', x, y, width, height)
        return true
      } catch (error) {
        console.warn('Could not add logo:', error)
        this.addLogoPlaceholder(doc, x, y, width, height)
        return false
      }
    } else {
      this.addLogoPlaceholder(doc, x, y, width, height)
      return false
    }
  }

  /**
   * Add summary header matching the college format with logo
   */
  static async addSummaryHeader(doc, scheduleData) {
    // Add logo
    this.addLogoToPDF(doc, 25, 12, 20, 16)
    
    // College name
    doc.setFontSize(18)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(0, 0, 0)
    doc.text('SHASUN', 105, 18, { align: 'center' })
    
    doc.setFontSize(14)
    doc.setFont('helvetica', 'normal')
    doc.text('JAIN COLLEGE FOR WOMEN', 105, 26, { align: 'center' })
    
    // Exam title with red background (#FF2222) and border
    doc.setFillColor(255, 34, 34) // #FF2222
    doc.rect(20, 35, 170, 12, 'F')
    
    // Add border to exam title
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.5)
    doc.rect(20, 35, 170, 12)
    
    doc.setFontSize(14)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(255, 255, 255) // White text
    doc.text(scheduleData.title.toUpperCase(), 105, 43, { align: 'center' })
    
    // Date and Session row with light background and border
    doc.setFillColor(248, 249, 250) // Light gray background
    doc.rect(20, 47, 170, 10, 'F')
    
    // Add border to date/session row
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.5)
    doc.rect(20, 47, 170, 10)
    
    doc.setFontSize(12)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(255, 34, 34) // #FF2222 for date and session text
    doc.text(`DATE: ${this.formatDate(scheduleData.date)}`, 30, 54)
    doc.text(`SESSION: ${scheduleData.session}`, 130, 54)
    
    // Reset text color for content
    doc.setTextColor(0, 0, 0)
  }

  /**
   * Add summary header for continuation pages (synchronous)
   */
  static addSummaryHeaderSync(doc, scheduleData) {
    // Add logo using cached data
    this.addLogoToPDF(doc, 25, 12, 20, 16)
    
    // College name
    doc.setFontSize(18)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(0, 0, 0)
    doc.text('SHASUN', 105, 18, { align: 'center' })
    
    doc.setFontSize(14)
    doc.setFont('helvetica', 'normal')
    doc.text('JAIN COLLEGE FOR WOMEN', 105, 26, { align: 'center' })
    
    // Exam title with red background and border (no CONTINUED text)
    doc.setFillColor(255, 34, 34) // #FF2222
    doc.rect(20, 35, 170, 12, 'F')
    
    // Add border to exam title
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.5)
    doc.rect(20, 35, 170, 12)
    
    doc.setFontSize(14)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(255, 255, 255)
    doc.text(scheduleData.title.toUpperCase(), 105, 43, { align: 'center' })
    
    // Date and Session row with border
    doc.setFillColor(248, 249, 250)
    doc.rect(20, 47, 170, 10, 'F')
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.5)
    doc.rect(20, 47, 170, 10)
    
    doc.setFontSize(12)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(255, 34, 34) // #FF2222
    doc.text(`DATE: ${this.formatDate(scheduleData.date)}`, 30, 54)
    doc.text(`SESSION: ${scheduleData.session}`, 130, 54)
    
    doc.setTextColor(0, 0, 0)
  }

  /**
   * Add detailed header for first page (with DETAILED REPORT text)
   */
  static addDetailedHeaderFirstPage(doc, scheduleData) {
    // Add logo using cached data
    this.addLogoToPDF(doc, 25, 12, 20, 16)
    
    // College name
    doc.setFontSize(18)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(0, 0, 0)
    doc.text('SHASUN', 105, 18, { align: 'center' })
    
    doc.setFontSize(14)
    doc.setFont('helvetica', 'normal')
    doc.text('JAIN COLLEGE FOR WOMEN', 105, 26, { align: 'center' })
    
    // Exam title with red background (#FF2222) and border (with DETAILED REPORT)
    doc.setFillColor(255, 34, 34) // #FF2222
    doc.rect(20, 35, 170, 12, 'F')
    
    // Add border to exam title
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.5)
    doc.rect(20, 35, 170, 12)
    
    doc.setFontSize(14)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(255, 255, 255)
    doc.text(`${scheduleData.title.toUpperCase()} - DETAILED REPORT`, 105, 43, { align: 'center' })
    
    // Date and Session row with border
    doc.setFillColor(248, 249, 250)
    doc.rect(20, 47, 170, 10, 'F')
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.5)
    doc.rect(20, 47, 170, 10)
    
    doc.setFontSize(12)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(255, 34, 34) // #FF2222
    doc.text(`DATE: ${this.formatDate(scheduleData.date)}`, 30, 54)
    doc.text(`SESSION: ${scheduleData.session}`, 130, 54)
    
    doc.setTextColor(0, 0, 0)
  }

  /**
   * Add detailed header matching the college format (async version - delegates to sync)
   */
  static async addDetailedHeader(doc, scheduleData) {
    // For the first page, use the first page header with DETAILED REPORT
    this.addDetailedHeaderFirstPage(doc, scheduleData)
  }

  /**
   * Add detailed header for continuation pages (synchronous - no DETAILED REPORT text)
   */
  static addDetailedHeaderSync(doc, scheduleData) {
    // Add logo using cached data
    this.addLogoToPDF(doc, 25, 12, 20, 16)
    
    // College name
    doc.setFontSize(18)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(0, 0, 0)
    doc.text('SHASUN', 105, 18, { align: 'center' })
    
    doc.setFontSize(14)
    doc.setFont('helvetica', 'normal')
    doc.text('JAIN COLLEGE FOR WOMEN', 105, 26, { align: 'center' })
    
    // Exam title with red background (#FF2222) and border (no DETAILED REPORT text)
    doc.setFillColor(255, 34, 34) // #FF2222
    doc.rect(20, 35, 170, 12, 'F')
    
    // Add border to exam title
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.5)
    doc.rect(20, 35, 170, 12)
    
    doc.setFontSize(14)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(255, 255, 255)
    doc.text(scheduleData.title.toUpperCase(), 105, 43, { align: 'center' })
    
    // Date and Session row with border
    doc.setFillColor(248, 249, 250)
    doc.rect(20, 47, 170, 10, 'F')
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.5)
    doc.rect(20, 47, 170, 10)
    
    doc.setFontSize(12)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(255, 34, 34) // #FF2222
    doc.text(`DATE: ${this.formatDate(scheduleData.date)}`, 30, 54)
    doc.text(`SESSION: ${scheduleData.session}`, 130, 54)
    
    doc.setTextColor(0, 0, 0)
  }

  /**
   * Add logo placeholder when actual logo can't be loaded
   */
  static addLogoPlaceholder(doc, x, y, width, height) {
    const centerX = x + width / 2
    const centerY = y + height / 2
    const radius = Math.min(width, height) / 2
    
    doc.setFillColor(220, 220, 220)
    doc.setDrawColor(180, 180, 180)
    doc.setLineWidth(1)
    doc.circle(centerX, centerY, radius, 'FD')
    
    doc.setFontSize(8)
    doc.setTextColor(120, 120, 120)
    doc.setFont('helvetica', 'normal')
    doc.text('LOGO', centerX, centerY + 1, { align: 'center' })
  }

  /**
   * Create the main summary table with exact styling matching the image
   */
  static createSummaryTable(doc, summaryData, scheduleData) {
    let startY = 70 // Increased to avoid overlap with header
    
    summaryData.forEach((roomData, roomIndex) => {
      // Room header with purple background (#B09FC6)
      doc.setFillColor(176, 159, 198) // #B09FC6
      doc.rect(20, startY, 170, 10, 'F')
      
      // Add uniform border to room header
      doc.setDrawColor(0, 0, 0)
      doc.setLineWidth(0.5)
      doc.rect(20, startY, 170, 10)
      
      doc.setFontSize(12)
      doc.setFont('helvetica', 'bold')
      doc.setTextColor(0, 0, 0) // Black text on purple background
      doc.text(`${roomIndex + 1}.Room No : ${roomData.roomNumber}(${roomData.roomBuilding})`, 25, startY + 6)
      
      startY += 10
      
      // Class rows with uniform borders and white background
      roomData.classData.forEach((classInfo, classIndex) => {
        // White background for all class rows
        doc.setFillColor(255, 255, 255) // White background
        doc.rect(20, startY, 170, 8, 'F')
        
        // Add uniform borders for all sides
        doc.setDrawColor(0, 0, 0)
        doc.setLineWidth(0.5)
        doc.rect(20, startY, 170, 8) // Full border around the row
        
        // Vertical separator between class info and count
        doc.line(150, startY, 150, startY + 8)
        
        // Class name and roll range
        doc.setFontSize(10)
        doc.setFont('helvetica', 'bold')
        doc.setTextColor(0, 0, 0) // Black text
        doc.text(classInfo.className, 25, startY + 5)
        
        // Roll range
        doc.setFont('helvetica', 'normal')
        doc.text(classInfo.rollRange, 80, startY + 5)
        
        // Count (right aligned)
        doc.setFont('helvetica', 'bold')
        doc.text(classInfo.count.toString(), 170, startY + 5, { align: 'center' })
        
        startY += 8
      })
      
      // Total row with white background and uniform border
      doc.setFillColor(255, 255, 255) // White background for total
      doc.rect(20, startY, 170, 10, 'F')
      
      // Total row uniform borders
      doc.setLineWidth(0.5)
      doc.rect(20, startY, 170, 10)
      doc.line(150, startY, 150, startY + 10) // Vertical separator
      
      doc.setFontSize(12)
      doc.setFont('helvetica', 'bold')
      doc.setTextColor(0, 0, 0) // Black text
      doc.text('TOTAL', 25, startY + 6)
      doc.text(roomData.totalStudents.toString(), 170, startY + 6, { align: 'center' })
      
      startY += 10 // No extra space between tables - directly connect
      
      // Check if we need a new page
      if (startY > 240 && roomIndex < summaryData.length - 1) {
        doc.addPage()
        // Add header to new page
        this.addSummaryHeaderSync(doc, scheduleData)
        startY = 70 // Increased to avoid overlap
      }
    })
  }

  /**
   * Add room detailed section for individual printing (no capacity info, proper overflow handling)
   */
  static addRoomDetailedSectionForPrinting(doc, room, startY) {
    // Room header with purple background (#B09FC6) - directly after exam title
    doc.setFillColor(176, 159, 198) // #B09FC6
    doc.rect(20, startY, 170, 10, 'F')
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.5)
    doc.rect(20, startY, 170, 10)
    
    doc.setFontSize(12)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(0, 0, 0) // Black text on purple background
    const roomTitle = `${room.room_number} - ${room.room_building} (${room.room_floor})`
    doc.text(roomTitle, 25, startY + 6)
    
    // Sort students by class first, then by roll number
    const sortedStudents = [...room.students].sort((a, b) => {
      // First sort by class name
      const classComparison = a.className.localeCompare(b.className)
      if (classComparison !== 0) return classComparison
      
      // Then sort by roll number
      return a.rollNumber.localeCompare(b.rollNumber)
    })
    
    // Students table directly below room header (no capacity info)
    const tableData = sortedStudents.map(student => [
      student.rollNumber,
      student.studentName,
      student.className
    ])
    
    // Store current page number to track overflow
    const startPage = doc.internal.getNumberOfPages()
    
    doc.autoTable({
      head: [['Roll Number', 'Student Name', 'Class']],
      body: tableData,
      startY: startY + 10, // Start immediately after room header
      margin: { left: 20, right: 20 },
      styles: {
        fontSize: 9,
        cellPadding: 4,
        lineColor: [0, 0, 0], // Black borders
        lineWidth: 0.5,
        textColor: [0, 0, 0], // Black text
        fillColor: [255, 255, 255] // White background for all cells
      },
      headStyles: {
        fillColor: [176, 159, 198], // #B09FC6 for header - same as room header
        textColor: [0, 0, 0], // Black text on purple background
        fontStyle: 'bold',
        fontSize: 10
      },
      columnStyles: {
        0: { cellWidth: 40, halign: 'center' },
        1: { cellWidth: 80, halign: 'left' },
        2: { cellWidth: 50, halign: 'center' }
      },
      tableLineColor: [0, 0, 0], // Black table borders
      tableLineWidth: 0.5,
      showHead: 'everyPage', // Show header on every page
      pageBreak: 'auto', // Allow automatic page breaks
      pageBreakBefore: function(cursor, doc) {
        // Don't add header to overflow pages - they should be plain continuation
        return false;
      }
    })
    
    // Check if table overflowed to additional pages
    const endPage = doc.internal.getNumberOfPages()
    
    // If table overflowed, the continuation pages should not have headers
    // This is handled by the autoTable configuration above
    
    return doc.lastAutoTable.finalY
  }

  /**
   * Add room detailed section with no spacing between elements (legacy method)
   */
  static addRoomDetailedSection(doc, room, startY) {
    // Room header with purple background (#B09FC6) - directly after exam title
    doc.setFillColor(176, 159, 198) // #B09FC6
    doc.rect(20, startY, 170, 10, 'F')
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.5)
    doc.rect(20, startY, 170, 10)
    
    doc.setFontSize(12)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(0, 0, 0) // Black text on purple background
    const roomTitle = `${room.room_number} - ${room.room_building} (${room.room_floor})`
    doc.text(roomTitle, 25, startY + 6)
    
    // Room capacity info directly below room header (no spacing)
    doc.setFillColor(255, 255, 255) // White background
    doc.rect(20, startY + 10, 170, 8, 'F')
    doc.setLineWidth(0.5)
    doc.rect(20, startY + 10, 170, 8)
    
    doc.setFontSize(10)
    doc.setFont('helvetica', 'normal')
    doc.setTextColor(0, 0, 0) // Black text
    doc.text(`Capacity: ${room.room_capacity} | Assigned: ${room.students.length}`, 25, startY + 15)
    
    // Students table directly below capacity info (no spacing)
    const tableData = room.students.map(student => [
      student.rollNumber,
      student.studentName,
      student.className
    ])
    
    doc.autoTable({
      head: [['Roll Number', 'Student Name', 'Class']],
      body: tableData,
      startY: startY + 18, // Start immediately after capacity info
      margin: { left: 20, right: 20 },
      styles: {
        fontSize: 9,
        cellPadding: 4,
        lineColor: [0, 0, 0], // Black borders
        lineWidth: 0.5,
        textColor: [0, 0, 0], // Black text
        fillColor: [255, 255, 255] // White background for all cells
      },
      headStyles: {
        fillColor: [176, 159, 198], // #B09FC6 for header - same as room header
        textColor: [0, 0, 0], // Black text on purple background
        fontStyle: 'bold',
        fontSize: 10
      },
      columnStyles: {
        0: { cellWidth: 40, halign: 'center' },
        1: { cellWidth: 80, halign: 'left' },
        2: { cellWidth: 50, halign: 'center' }
      },
      tableLineColor: [0, 0, 0], // Black table borders
      tableLineWidth: 0.5
    })
    
    return doc.lastAutoTable.finalY // Return end position for next room
  }

  /**
   * Add footer for individual room printing (only on pages with headers)
   */
  static addDetailedFooterForPrinting(doc, scheduleData) {
    const pageCount = doc.internal.getNumberOfPages()
    const roomCount = scheduleData.room_assignments.length
    
    // Track which pages have headers (room starting pages)
    const headerPages = []
    for (let i = 0; i < roomCount; i++) {
      headerPages.push(i + 1) // Pages 1, 2, 3, etc. for each room start
    }
    
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i)
      
      // Only add footer to pages that have headers (room starting pages)
      // Overflow pages should be plain without any header/footer
      const isHeaderPage = headerPages.includes(i) || 
                          (i <= roomCount); // First few pages are room starting pages
      
      if (isHeaderPage) {
        // Add line separator
        doc.setDrawColor(0, 0, 0)
        doc.setLineWidth(0.5)
        doc.line(20, 280, 190, 280)
        
        // Footer text
        doc.setFontSize(9)
        doc.setFont('helvetica', 'normal')
        doc.setTextColor(108, 117, 125) // Bootstrap text-muted color
        doc.text(`Generated on: ${new Date().toLocaleString()}`, 20, 290)
        
        // Find which room this page belongs to
        const roomIndex = Math.min(i - 1, roomCount - 1)
        const room = scheduleData.room_assignments[roomIndex]
        if (room) {
          doc.text(`Room: ${room.room_number}`, 190, 290, { align: 'right' })
        }
      }
    }
  }

  /**
   * Add footer with consistent styling to all pages for detailed PDF (legacy method)
   */
  static addDetailedFooter(doc, scheduleData) {
    const pageCount = doc.internal.getNumberOfPages()
    
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i)
      
      // Add header to each page if not the first page
      if (i > 1) {
        this.addDetailedHeaderSync(doc, scheduleData)
      }
      
      // Add line separator
      doc.setDrawColor(0, 0, 0)
      doc.setLineWidth(0.5)
      doc.line(20, 280, 190, 280)
      
      // Footer text
      doc.setFontSize(9)
      doc.setFont('helvetica', 'normal')
      doc.setTextColor(108, 117, 125) // Bootstrap text-muted color
      doc.text(`Generated on: ${new Date().toLocaleString()}`, 20, 290)
      doc.text(`Page ${i} of ${pageCount}`, 190, 290, { align: 'right' })
    }
  }

  /**
   * Add footer with consistent styling to all pages for summary PDF
   */
  static addFooter(doc, scheduleData) {
    const pageCount = doc.internal.getNumberOfPages()
    
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i)
      
      // Add header to each page if not the first page
      if (i > 1) {
        this.addSummaryHeaderSync(doc, scheduleData)
      }
      
      // Add line separator
      doc.setDrawColor(0, 0, 0)
      doc.setLineWidth(0.5)
      doc.line(20, 280, 190, 280)
      
      // Footer text
      doc.setFontSize(9)
      doc.setFont('helvetica', 'normal')
      doc.setTextColor(108, 117, 125) // Bootstrap text-muted color
      doc.text(`Generated on: ${new Date().toLocaleString()}`, 20, 290)
      doc.text(`Page ${i} of ${pageCount}`, 190, 290, { align: 'right' })
    }
  }

  /**
   * Process room assignments into summary format
   */
  static processSummaryData(roomAssignments) {
    return roomAssignments.map(room => {
      // Group students by class
      const classSummary = {}
      
      room.students.forEach(student => {
        if (!classSummary[student.className]) {
          classSummary[student.className] = {
            className: student.className,
            students: [],
            count: 0
          }
        }
        classSummary[student.className].students.push(student.rollNumber)
        classSummary[student.className].count++
      })
      
      // Sort roll numbers and get range for each class
      const classData = Object.values(classSummary).map(classInfo => {
        const sortedRolls = classInfo.students.sort()
        return {
          className: classInfo.className,
          rollRange: sortedRolls.length > 0 ? 
            `${sortedRolls[0]}-${sortedRolls[sortedRolls.length - 1]}` : 'N/A',
          count: classInfo.count
        }
      })
      
      return {
        roomNumber: room.room_number,
        roomBuilding: room.room_building,
        roomFloor: room.room_floor,
        totalCapacity: room.room_capacity,
        classData: classData,
        totalStudents: room.students.length
      }
    })
  }

  /**
   * Format date for display (DD.MM.YYYY format)
   */
  static formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-GB', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    }).replace(/\//g, '.')
  }
}

export default PDFService
