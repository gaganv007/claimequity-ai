"""
Generate sample insurance claim report using xAI Grok API
This creates a realistic claim denial document for testing
"""
import requests
import json
from datetime import datetime

# xAI API Configuration
import os
XAI_API_KEY = os.getenv('XAI_API_KEY', '')  # Get from environment variable
XAI_API_URL = "https://api.x.ai/v1/chat/completions"

# If no environment variable, prompt user (for command-line usage)
if not XAI_API_KEY:
    print("⚠️  XAI_API_KEY environment variable not set.")
    print("   Set it with: export XAI_API_KEY='your-key-here'")
    print("   Or run the Streamlit app which allows entering the key in the UI.")

def generate_claim_report():
    """Generate a realistic insurance claim denial report using Grok"""
    
    prompt = """Generate a realistic health insurance claim denial document in PDF-style text format. 
Include the following sections:

1. Header: Insurance company name, claim number, date, patient information
2. Claim Summary: Procedure codes (CPT), diagnosis codes (ICD-10), dates of service, provider name
3. Denial Details: Specific reason for denial (e.g., "Prior authorization required", "Not medically necessary", "Out of network")
4. Explanation: Detailed explanation of why the claim was denied
5. Appeal Information: Instructions on how to appeal

Make it realistic with:
- Medical terminology (ICD-10 codes like E11.9, I10, etc.)
- CPT procedure codes
- Insurance jargon
- Specific denial codes
- Dates, amounts, and provider information

Format it as a professional insurance document that looks like it came from a real insurance company."""

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "grok-3",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert at generating realistic healthcare insurance documents. Create detailed, professional insurance claim denial documents with all standard sections and medical codes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
    
    print("🔄 Generating claim report using xAI Grok API...")
    
    try:
        response = requests.post(XAI_API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        claim_text = result['choices'][0]['message']['content']
        
        # Save as text file
        filename = f"sample_claim_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(claim_text)
        
        print(f"✅ Claim report generated successfully!")
        print(f"📄 Saved to: {filename}")
        print(f"\n--- Preview (first 500 chars) ---\n")
        print(claim_text[:500])
        print("\n...")
        
        return filename, claim_text
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None, None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None


def generate_multiple_reports(count=3):
    """Generate multiple claim reports with different scenarios"""
    print(f"📝 Generating {count} sample claim reports...\n")
    
    scenarios = [
        "Generate a claim denial for diabetes medication (E11.9) due to missing prior authorization.",
        "Generate a claim denial for hypertension treatment (I10) because the provider was out of network.",
        "Generate a claim denial for physical therapy services because it was deemed 'not medically necessary'."
    ]
    
    files = []
    
    for i, scenario in enumerate(scenarios[:count], 1):
        print(f"\n--- Generating Report {i}/{count} ---")
        
        headers = {
            "Authorization": f"Bearer {XAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "grok-3",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert at generating realistic healthcare insurance documents. Create detailed, professional insurance claim denial documents with all standard sections, medical codes (ICD-10, CPT), dates, amounts, and denial reasons."
                },
                {
                    "role": "user",
                    "content": f"{scenario} Format it as a complete insurance claim denial document with header, claim details, denial reason, and appeal instructions."
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(XAI_API_URL, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            claim_text = result['choices'][0]['message']['content']
            
            filename = f"sample_claim_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(claim_text)
            
            files.append(filename)
            print(f"✅ Saved: {filename}")
            
        except Exception as e:
            print(f"❌ Error generating report {i}: {e}")
    
    return files


if __name__ == "__main__":
    print("=" * 60)
    print("ClaimEquity AI - Sample Claim Report Generator")
    print("Using xAI Grok API")
    print("=" * 60)
    print()
    
    # Generate a single comprehensive report
    filename, claim_text = generate_claim_report()
    
    if filename:
        print(f"\n✅ Success! You can now:")
        print(f"   1. Open '{filename}' to view the full report")
        print(f"   2. Convert it to PDF (or use as-is)")
        print(f"   3. Upload it to the ClaimEquity AI app to test")
        print()
        print("💡 Tip: You can also generate multiple reports by running:")
        print("   python generate_claim_report.py --multiple")

