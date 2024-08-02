from PyPDF2 import PdfReader
import spacy
import re
import json
import os
# from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_md")

def extract_text_from_pdf(file):
    try:
        pdf_reader = PdfReader(file, strict=False)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""    
    
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
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
    # doc = get_file(filepath)
    text = extract_text_from_pdf(file)
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

    # incomplete: extract education, experience, and skills
    # for ent in doc.ents:
    #    if ent.label_ == "ORG":
    #         if "university" in ent.text.lower() or "college" in ent.text.lower() or "school" in ent.text.lower():
    #             qualification = {"institute": ent.text, "qualification": "", "period": ""}
    #             parsed_data["education"].append(qualification)
    #         else:
    #             if "inc" in ent.text.lower() or "llc" in ent.text.lower() or "corporation" in ent.text.lower() or "company" in ent.text.lower() or "corp" in ent.text.lower() or "ltd" in ent.text.lower() or "limited" in ent.text.lower() or "hospital" in ent.text.lower(): 
    #                 job = {"company": ent.text, "position": "", "period": ""}
    #                 parsed_data["experience"].append(job)

    return parsed_data

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path")
    args = parser.parse_args()

    # if os.path.isfile(args.pdf_path) and args.pdf_path.endswith('.pdf'):
    #     process_resume(args.pdf_path)
    # else:
    #     print("pdf path is invalid")
