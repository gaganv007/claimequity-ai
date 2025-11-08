"""
Convert text claim reports to PDF format
Requires: pip install reportlab (optional, or use system print-to-PDF)
"""
import os
from datetime import datetime

def convert_text_to_pdf_simple(text_file):
    """
    Simple conversion using reportlab if available,
    otherwise provides instructions for manual conversion
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        
        # Read text file
        with open(text_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create PDF
        pdf_file = text_file.replace('.txt', '.pdf')
        doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=14,
            spaceAfter=12,
            alignment=1  # Center
        )
        normal_style = styles['Normal']
        normal_style.fontSize = 10
        normal_style.leading = 12
        
        # Split content into lines and create paragraphs
        lines = content.split('\n')
        for line in lines:
            if line.strip():
                if line.startswith('='):
                    # Header line
                    para = Paragraph(line.replace('=', '').strip(), title_style)
                else:
                    para = Paragraph(line, normal_style)
                elements.append(para)
                elements.append(Spacer(1, 6))
            else:
                elements.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(elements)
        print(f"✅ PDF created: {pdf_file}")
        return pdf_file
        
    except ImportError:
        print("⚠️  reportlab not installed. Using alternative method...")
        print("\n📄 To convert to PDF, you can:")
        print("   1. Open the text file in a text editor")
        print("   2. Print to PDF (File > Print > Save as PDF)")
        print("   3. Or use an online converter")
        print("\n💡 To install reportlab for automatic conversion:")
        print("   pip install reportlab")
        return None
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        print("\n📄 Manual conversion options:")
        print("   1. Open the text file")
        print("   2. Print to PDF using your system's print dialog")
        print("   3. Or use: https://www.ilovepdf.com/txt-to-pdf")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("Claim Report Text to PDF Converter")
    print("=" * 60)
    print()
    
    # Find all sample claim report text files
    text_files = [f for f in os.listdir('.') if f.startswith('sample_claim') and f.endswith('.txt')]
    
    if not text_files:
        print("❌ No sample claim report text files found.")
        print("   Run generate_claim_report.py first, or use the existing sample files.")
    else:
        print(f"Found {len(text_files)} text file(s):")
        for i, f in enumerate(text_files, 1):
            print(f"   {i}. {f}")
        print()
        
        # Try to convert each
        for text_file in text_files:
            print(f"Converting {text_file}...")
            pdf_file = convert_text_to_pdf_simple(text_file)
            if pdf_file:
                print(f"✅ Success! PDF saved as: {pdf_file}")
            print()

