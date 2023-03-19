import streamlit as st
from gtts import gTTS
import os
import tempfile
from PyPDF2 import PdfReader
import docx

LANGUAGES = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    # Potentially add more languages here
}

# Get the text to speech
def text_to_speech(text, lang='en', slow=False):
    tts = gTTS(text=text, lang=lang, slow=slow)
    return tts

# Read the pdf
def read_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)

    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()

    return text

# Read the .docx
def read_docx(file):
    doc = docx.Document(file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def main():
    st.title("Accessible Text-to-Speech")

    # Get user input
    text_input_method = st.radio("Select the text input method:", ("Type text", "Upload a document"))
    if text_input_method == "Type text":
        text = st.text_area("Enter the text you want to convert to speech:")
    else:
        file = st.file_uploader("Upload a document (PDF or DOCX):", type=["pdf", "docx"])
        if file:
            if file.type == "application/pdf":
                text = read_pdf(file)
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = read_docx(file)
        else:
            text = ""

    lang = st.selectbox("Select a language:", options=list(LANGUAGES.keys()))
    slow = st.checkbox("Slow speed")

    # Convert the text
    if st.button("Convert Text to Speech"):
        if text:
            tts = text_to_speech(text, LANGUAGES[lang], slow)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name, format="audio/mp3")
        else:
            st.warning("Please enter some text or upload a document to convert.")

if __name__ == '__main__':
    main()
