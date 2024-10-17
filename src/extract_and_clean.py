import fitz  # PyMuPDF for extracting text from PDFs
import os
from PIL import Image  # For working with images used in OCR
import io
import pytesseract  # For OCR
import re
import json  # For working with JSON

# Precompiled regular expressions for reuse
pattern_digit_start = re.compile(r'^\d')
pattern_seite = re.compile(r'Seite \d+')
pattern_minus = re.compile(r'^-+')
pattern_letter_or_dot = re.compile(r'^(\d+)([a-zA-Z]|\.)\s?')
pattern_roman_numerals = re.compile(r'^[IVXLCDM]+\.\s?')
pattern_letter_dot = re.compile(r'^[a-z]{1,2}\)\s?')
pattern_bracketed_number = re.compile(r'^\(\d+\)\s?')

# Function to extract text using OCR
def extract_text_with_ocr(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()  # Get the page as an image
                img = Image.open(io.BytesIO(pix.tobytes()))  # Convert to an image
                text += pytesseract.image_to_string(img, lang="deu")  # Use OCR to extract text
    except Exception as e:
        print(f"Error using OCR for file {pdf_path}: {e}")
    return text

# Function to extract text from PDFs
def extract_text_from_pdfs(pdf_folder):
    extracted_data = {}
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            try:
                doc = fitz.open(pdf_path)
                text = ""
                for page in doc:
                    text += page.get_text()  # Standard text extraction
                if not text.strip():  # If no text was extracted, run OCR
                    print(f"Failed to read text using the standard method for {filename}. Trying OCR.")
                    text = extract_text_with_ocr(pdf_path)
                
                # Split the text into lines
                lines = text.splitlines()
                extracted_data[filename] = lines  # Save the text line by line
            except Exception as e:
                print(f"File {filename} is corrupted and cannot be read: {e}")
    return extracted_data

# Helper function to check whether a line matches certain patterns
def should_skip_line(text):
    if pattern_roman_numerals.match(text):
        return True
    if pattern_letter_dot.match(text):
        return True
    if pattern_bracketed_number.match(text):
        return True
    return False

# Function to clean text
def clean_text(text, skip_until_number):
    # Check for None
    if text is None:
        return None, skip_until_number
    
    # Strip once at the beginning to avoid multiple calls later
    text = text.strip()
    
    # If the flag is active, skip lines until a line starting with an Arabic numeral is found
    if skip_until_number:
        if pattern_digit_start.match(text):
            skip_until_number = False  # Reset flag
        else:
            return None, skip_until_number  # Skip the line

    # Remove phrases in the format "Seite {number}"
    text = pattern_seite.sub('', text)

    # Remove minus at the start of the line
    text = pattern_minus.sub('', text)

    # Remove letter or dot after a number at the start of the line
    text = pattern_letter_or_dot.sub(r'\1 ', text)

    # Skip lines that match certain patterns (Roman numerals, letters with dots, etc.)
    if should_skip_line(text):
        skip_until_number = True
        return None, skip_until_number

    # Return cleaned text and flag
    return text or None, skip_until_number

# Function to combine lines into paragraphs in chronological order
def combine_sentences_into_paragraphs_with_keys(lines):
    paragraphs = {}
    current_paragraph = []
    current_number = 1

    for line in lines:
        # Check if the line starts with the current sequential number
        match = re.match(r'^(\d+)', line)
        if match:
            number = int(match.group(1))
            
            # If the number matches the current paragraph number
            if number == current_number:
                if current_paragraph:
                    # Save the current paragraph as a key-value pair with leading spaces removed
                    paragraphs[current_number] = ' '.join(current_paragraph).strip()
                current_paragraph = [re.sub(r'^\d+\s*', '', line)]  # Remove the number from the line
                current_number += 1  # Move to the next paragraph number
            else:
                current_paragraph.append(re.sub(r'^\d+\s*', '', line))  # Add the line to the paragraph without the number
        else:
            current_paragraph.append(line)  # If the line doesn't start with a number, add it to the paragraph

    if current_paragraph:
        # Save the last paragraph with leading spaces removed
        paragraphs[current_number] = ' '.join(current_paragraph).strip()

    return paragraphs

# Function to apply text cleaning to extracted data
def apply_text_cleaning_with_anlage(extracted_data):
    cleaned_data = {}
    for filename, lines in extracted_data.items():
        cleaned_lines = []
        found_cut = False
        found_inhaltsubersicht = False
        skip_until_number = False
        
        for line in lines:
            # Check for "Inhaltsübersicht" to start processing
            if not found_inhaltsubersicht and "Inhaltsübersicht" in line:
                found_inhaltsubersicht = True
            
            # After finding "Inhaltsübersicht", check for "Anwendungsregelung" or "Schlussformel"
            if found_inhaltsubersicht and not found_cut:
                if "Anwendungsregelung" in line or "Schlussformel" in line:
                    found_cut = True
                    cleaned_lines = []  # Clear the list of lines upon finding these terms
            
            # Clean the line
            cleaned_line, skip_until_number = clean_text(line, skip_until_number)
            if cleaned_line:
                cleaned_lines.append(cleaned_line)

        # Combine sentences into paragraphs with numbered keys after cleaning for each file
        paragraphs = combine_sentences_into_paragraphs_with_keys(cleaned_lines)
        cleaned_data[filename] = paragraphs
    return cleaned_data

# Function to save cleaned data to a JSON file
def save_data_to_json(data, json_filename):
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Main program
if __name__ == "__main__":
    pdf_folder = "data"  # Path to the folder with PDF files
    cleaned_json_filename = "cleaned_texts.json"

    # Extract text from PDF files
    extracted_texts = extract_text_from_pdfs(pdf_folder)

    # Apply cleaning to the extracted text
    cleaned_texts = apply_text_cleaning_with_anlage(extracted_texts)

    # Save the cleaned data to a JSON file
    save_data_to_json(cleaned_texts, cleaned_json_filename)
    print(f"Cleaned data saved to {cleaned_json_filename}")