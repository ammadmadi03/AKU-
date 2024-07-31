import fitz # pymupdf as pymu
import spacy
import re
import json
import os
# from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_md")

def extract_text_from_pdf(pdf_path):
    print(f"Extract function: pdf path = {pdf_path}")
    try:
        pdf_reader = fitz.open(pdf_path)  
    except Exception as e:
        print(f"Error opening PDF (pymupdf): {e}")
        return ""
    
    text = ""
    try:
        for page in pdf_reader:
            text += page.get_text()
    except Exception as e:
        print(f"Error extracting text from PDF (pymupdf): {e}")
        return ""
    
    return text

def get_name(doc):
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return (ent.text).strip()

def get_email(text):
    email = re.findall(r'\S+@\S+', text)
    if email:
        return email[0]

def get_phone_number(text):
    phone_pattern = r'(?:(?:0092|\+92)[-.\s]?|\d{1})(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        return phone_match.group(0).strip()

def parse_resume(file):
    text = extract_text_from_pdf(file)
    if not text:
        print("No text extracted from PDF")
        return {}
    
    doc = nlp(text)

    parsed_data = {
        "name": "",
        "email": "",
        "phone": "",
        "education": [],
        "experience": [],
        "skills": []
    }
       
    # name
    parsed_data["name"] = get_name(doc)
    
    # email
    parsed_data["email"] = get_email(text)
    
    # phone number 
    parsed_data["phone"] = get_phone_number(text)

    return parsed_data

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path")
    args = parser.parse_args()

    if os.path.isfile(args.pdf_path) and args.pdf_path.endswith(".pdf"):
        parsed_data = parse_resume(args.pdf_path)
        print(json.dumps(parsed_data, indent=4))
    else:
        print("Invalid PDF file path")