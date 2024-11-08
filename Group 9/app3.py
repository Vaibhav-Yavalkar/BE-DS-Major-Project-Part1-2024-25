import streamlit as st
import PyPDF2
import google.generativeai as genai
# Initialize the Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    extracted_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text
    return extracted_text

def main():
    st.title("Gemini Document Summarizer")

    # Upload PDF files
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        pdf_texts = []
        for uploaded_file in uploaded_files:
            # Extract text from each PDF
            text = extract_text_from_pdf(uploaded_file)
            pdf_texts.append(text)

        # Join the texts into one string
        combined_text = "\n".join(pdf_texts)

        # Generate summary
        prompt = "Summarize the content of the uploaded PDF files."
        response = model.generate_content([prompt, combined_text])

        st.subheader("Summary:")
        st.write(response.text)

if __name__ == "__main__":
    main()
