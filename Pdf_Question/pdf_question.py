from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from pathlib import Path
import re
import pytesseract
from PIL import Image

class PdfConfigModel:
    def __init__(self):
        pass

    def clean_text(self, text):
        # Remove non-alphanumeric characters and extra whitespaces
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        cleaned_text = ' '.join(cleaned_text.split())
        return cleaned_text

    def get_pdf_text(self, pdf_path):
        with open(pdf_path, "rb") as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                # Extract text using Tesseract from each page
                text += page.extract_text()
        return self.clean_text(text)

    def get_text_chunks(self, text):
        # Adjust chunk_size and chunk_overlap for optimal results
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        chunks = text_splitter.split_text(text)
        return chunks

    def get_vector_store(self, text_chunks):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
        return vector_store

    def get_conversational_chain(self):
        prompt_template = """
        Answer the question as detailed as possible from the provided context, make sure to provide all the d
        provided context just say, "answer is not available in the context", don't provide the wrong answer\n
        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:"""
        # Adjust temperature for desired randomness level
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
        return chain

    def user_input(self, user_question):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        new_db = FAISS.load_local("faiss_index", embeddings)
        docs = new_db.similarity_search(user_question)
        chain = self.get_conversational_chain()
        # Use invoke instead of __call__ to address the deprecation warning
        response = chain.invoke({"input_documents": docs, "question": user_question}, return_only_outputs=True)
        return response

    def main(self, file_path):
        # Use Tesseract for text extraction from PDF
        raw_text = self.get_pdf_text(file_path)
        text_chunks = self.get_text_chunks(raw_text)
        self.get_vector_store(text_chunks)
        print(f"The data from {file_path} is chunked and stored in the vector db")

    def storing_db(self, pdf_files):
        for pdf_file in pdf_files:
            self.main(file_path=pdf_file)

# List of PDF files
pdf_files = [
    Path(r"D:\Rotary club chat bot\Pdf_files\ClubRecognitionSummary.pdf"),
    Path(r"D:\Rotary club chat bot\Pdf_files\Members Rooster .pdf"),
    Path(r"Pdf_files\North Dues.pdf"),
    Path(r'D:\Rotary club chat bot\Pdf_files\The President of rotary club (1).pdf')
]

class pdf_pipeline:
    def __init__(self):
        pass
    def main(self,message):
        data = PdfConfigModel()
        data.storing_db(pdf_files)
        response_text = data.user_input(message)
        return response_text
