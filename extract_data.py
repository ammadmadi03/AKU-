import PyPDF2
import spacy
import re
import json
import os
# from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_md")
# def get_file(pdf_path):
#     return pymupdf.open(pdf_path)

def extract_text_from_pdf(doc):
    pdf_reader = PyPDF2.PdfFileReader(doc)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extract_text()
    return text
    

def parse_resume(doc):
    # doc = get_file(filepath)
    text = extract_text_from_pdf(doc)

    parsed_data = {
        "name": "",
        "email": "",
        "phone": "",
        "education": [],
        "experience": [],
        "skills": []
    }
       
    # name
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            parsed_data["name"] = ent.text
            break
    
    # email
    email = re.findall(r'\S+@\S+', text)
    if email:
        parsed_data["email"] = email[0]
    
    # phone number 
    phone_pattern = r'(?:(?:0092|\+92)?[-.\s]?|\d{1})(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        parsed_data["phone"] = phone_match.group(0).strip()

    # incomplete: extract education, experience, and skills
    for ent in doc.ents:
       if ent.label_ == "ORG":
            if "university" in ent.text.lower() or "college" in ent.text.lower() or "school" in ent.text.lower():
                qualification = {"institute": ent.text, "qualification": "", "period": ""}
                parsed_data["education"].append(qualification)
            else:
                if "inc" in ent.text.lower() or "llc" in ent.text.lower() or "corporation" in ent.text.lower() or "company" in ent.text.lower() or "corp" in ent.text.lower() or "ltd" in ent.text.lower() or "limited" in ent.text.lower() or "hospital" in ent.text.lower(): 
                    job = {"company": ent.text, "position": "", "period": ""}
                    parsed_data["experience"].append(job)

    return parsed_data

def process_resume(pdf_path):
    doc = get_file(pdf_path)
    parsed_data = parse_resume(doc)
    json_path = pdf_path.replace('.pdf', '_md.json')
    # json_path = json_path.replace('resumes', 'parsed_data')
    with open(json_path, 'w') as json_file:
        json.dump(parsed_data, json_file, indent=4)
    print(f"Processed {pdf_path} and saved as {json_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path")
    args = parser.parse_args()

    if os.path.isfile(args.pdf_path) and args.pdf_path.endswith('.pdf'):
        process_resume(args.pdf_path)
    else:
        print("pdf path is invalid")
