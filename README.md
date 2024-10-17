
# RAG Pipeline

**RAG Pipeline** is a Retrieval-Augmented Generation (RAG) Pipeline designed for extracting text from PDF documents, vectorizing it, and storing it in a vector database for fast retrieval of relevant data and responses to text queries.

## Key Components

### 1. Text Extraction from PDFs
Using the PyMuPDF library, RAG Pipeline extracts text directly from PDF files. If standard text extraction fails (e.g., the document consists of images), OCR is applied using Tesseract to recognize text from the images.

### 2. Text Preprocessing
The extracted text undergoes several preprocessing steps:
- Removal of unnecessary characters (e.g., page numbers, unwanted hyphens).
- Formatting the text for further vectorization.
- Cleaning the text using regular expressions to improve the quality of the data.

### 3. Text Vectorization
After cleaning, the text is converted into vector representations using the Sentence Transformers model. The text vectors are then stored in FAISS, which enables fast searches for relevant paragraphs based on user queries.

### 4. Query Search
The user can submit a text query, which is vectorized and used to search for relevant text passages in the vector database. The most appropriate sentences or paragraphs containing the required information are returned.

## Running the Project

### Installing Dependencies
Before running the project, ensure you have installed the necessary dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Running the Program
1. Place the PDF files in the \`/data\` folder.
2. Run the script to extract and clean the text:
\`\`\`bash
python src/extract_and_clean.py
\`\`\`
3. Run the main file to vectorize the text and handle queries:
\`\`\`bash
python src/main.py
\`\`\`

## Example Usage

\`\`\`bash
python main.py
\`\`\`

The program will perform the following steps:
1. Load the cleaned data from PDF documents.
2. Vectorize the text.
3. Create a FAISS index for fast search.
4. Answer questions:
    - What is the basic allowance?
    - How are benefits from a direct commitment or support fund taxed?
    - How are payments from direct insurance, pension funds, or pension schemes taxed during the payout phase?

## Conclusion

RAG Pipeline allows for fast extraction and retrieval of relevant text fragments from documents based on text queries, making it useful for analyzing large volumes of documents and generating responses to inquiries.
