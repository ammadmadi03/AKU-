import fitz
import docx
import spacy
import re
import json
import os
import io

nlp = spacy.load("en_core_web_lg")

def get_name(doc):
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return (ent.text).strip()

def get_email(text):
    email = re.findall(r'\S+@\S+', text)
    if email:
        return email[0]

def get_phone_number(text):
    # phone_pattern = r'(?:(?:0092|\+92)[-.\s]?|\d{1})?(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})'
    phone_pattern = r"(?:\(?\+?0{0,2}\d{1,3}\)?[-.\s]?)?(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})"
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        return phone_match.group(0).strip()

def get_skills(text):
    skills_list = [" .NET", "Angular", "Bootstrap", "C#", "C++", "CSS", "Django", "Express.js", "Flask", "Git", "HTML", "Java", "JavaScript", "jQuery", "Keras", "Kotlin", "Laravel", "LaTeX", "Matlab", "Microsoft SQL Server", "MongoDB", "MySQL", "Node.js", "NumPy", "OpenCV", "Oracle", "Pandas", "PHP", "PostgreSQL", "PyTorch", "Python", "React.js", "Ruby", "SpaCy", "SPSS", "SQL", "SQLite", "Swift", "TensorFlow", "TypeScript", "Vue.js"]
    
    skills = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            skills.append(skill)
    return ', '.join(skills)

def extract_text(file):
    file_stream = io.BytesIO(file.read())
    text = ""

    # read from pdf 
    try:
        file_stream.seek(0)
        pdf_reader = fitz.open(stream=file_stream, filetype="pdf") 
        for page in pdf_reader:
            text += page.get_text() 
    # read from docx
    except Exception as e:
        try:
            file_stream.seek(0)
            docx_reader = docx.Document(file_stream)
            for paragraph in docx_reader.paragraphs:
                text += paragraph.text + "\n"
        
        except Exception as e:
            print(f"error: {e}")
    
    # normalize text
    lines = text.split('\n')
    normalized_lines = []
    for line in lines:
        if line.isupper():
            words = line.split()
            capitalized_words = [word.capitalize() for word in words]
            normalized_lines.append(' '.join(capitalized_words))
        else:
            normalized_lines.append(line)

    # text = '\n'.join(normalized_lines)

    # find + remove unnecessary newlines 
    reformatted_text = []
    buffer = ""

    # detect possibl split lines
    possible_split = re.compile(r'^[a-z0-9]')

    for line in normalized_lines:
        # if current line is a possible continuation of previous line
        if buffer and possible_split.match(line):
            buffer += " " + line.strip()
        else:
            if buffer:
                reformatted_text.append(buffer)
            buffer = line.strip()
    
    # add remaining text in buffer
    if buffer:
        reformatted_text.append(buffer)
    text = "\n".join(reformatted_text)

    return text

def parse_resume(file):
    text = extract_text(file)

    if not text:
        print("No text extracted from PDF")
        return {}
    
    doc = nlp(text)

    parsed_data = {"name": "", "email": "", "phone": "", "education": [], "experience": [], "skills": ""}
    parsed_data["name"] = get_name(doc)
    parsed_data["email"] = get_email(text)
    parsed_data["phone"] = get_phone_number(text)
    parsed_data["skills"] = get_skills(text)
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